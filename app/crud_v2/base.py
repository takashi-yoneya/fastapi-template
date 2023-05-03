import datetime
import math
from enum import Enum
from typing import Any, Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.properties import ColumnProperty
from sqlalchemy.sql import func, select

from app import schemas
from app.exceptions.core import APIException
from app.exceptions.error_messages import ErrorMessage
from app.models.base import Base
from app.schemas.core import PagingQueryIn

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseModel)
ListResponseSchemaType = TypeVar("ListResponseSchemaType", bound=BaseModel)


class CRUDV2Base(
    Generic[
        ModelType,
        ResponseSchemaType,
        CreateSchemaType,
        UpdateSchemaType,
        ListResponseSchemaType,
    ],
):
    def __init__(
        self,
        model: type[ModelType],
        response_schema_class: type[ResponseSchemaType],
        list_response_class: type[ListResponseSchemaType],
    ) -> None:
        self.model = model
        self.response_schema_class = response_schema_class
        self.list_response_class = list_response_class

    def _get_select_columns(self) -> list[ColumnProperty]:
        """ResponseSchemaに含まれるfieldのみをsqlalchemyのselect用のobjectとして返す."""
        schema_columns = list(self.response_schema_class.__fields__.keys())
        mapper = inspect(self.model)
        select_columns = [
            getattr(self.model, attr.key)
            for attr in mapper.attrs
            if isinstance(attr, ColumnProperty) and attr.key in schema_columns
        ]

        return select_columns

    def _filter_model_exists_fields(self, data_dict: dict[str, Any]) -> dict[str, Any]:
        """data_dictを与え、modelに存在するfieldだけをfilterして返す."""
        data_fields = list(data_dict.keys())
        mapper = inspect(self.model)
        exists_data_dict = {}
        for attr in mapper.attrs:
            if isinstance(attr, ColumnProperty) and attr.key in data_fields:
                exists_data_dict[attr.key] = data_dict[attr.key]

        return exists_data_dict

    def _get_order_by_clause(
        self,
        sort_field: Any | Enum,
    ) -> ColumnProperty | None:
        sort_field_value = (
            sort_field.value if isinstance(sort_field, Enum) else sort_field
        )
        mapper = inspect(self.model)
        order_by_clause = [
            attr
            for attr in mapper.attrs
            if isinstance(attr, ColumnProperty) and attr.key == sort_field_value
        ]

        return order_by_clause[0] if order_by_clause else None

    async def get_db_obj_by_id(
        self,
        db: AsyncSession,
        id: Any,
        include_deleted: bool = False,
    ) -> ModelType | None:
        stmt = (
            select(self.model)
            .where(self.model.id == id)
            .execution_options(include_deleted=include_deleted)
        )
        return (await db.execute(stmt)).scalars().first()

    async def get_db_obj_list(
        self,
        db: AsyncSession,
        where_clause: list[Any] | None = None,
        sort_query_in: schemas.SortQueryIn | None = None,
        include_deleted: bool = False,
    ) -> list[ModelType]:
        where_clause = where_clause if where_clause is not None else []
        stmt = select(self.model).where(*where_clause)
        if sort_query_in:
            order_by_clause = self._get_order_by_clause(sort_query_in.sort_field)
            stmt = sort_query_in.apply_to_query(stmt, order_by_clause=order_by_clause)

        db_obj_list = (
            await db.execute(stmt.execution_options(include_deleted=include_deleted))
        ).all()
        return db_obj_list

    async def get_paged_list(
        self,
        db: AsyncSession,
        paging_query_in: PagingQueryIn,
        where_clause: list[Any] | None = None,
        sort_query_in: schemas.SortQueryIn | None = None,
        include_deleted: bool = False,
    ) -> ListResponseSchemaType:
        """Notes
        include_deleted=Trueの場合は、削除フラグ=Trueのデータも返す.
        """
        where_clause = where_clause if where_clause is not None else []
        stmt = (
            select(func.count(self.model.id))
            .where(*where_clause)
            .execution_options(include_deleted=include_deleted)
        )
        total_count = (await db.execute(stmt)).scalar()

        select_columns = self._get_select_columns()
        stmt = select(*select_columns).where(*where_clause)
        if sort_query_in:
            order_by_clause = self._get_order_by_clause(sort_query_in.sort_field)
            stmt = sort_query_in.apply_to_query(stmt, order_by_clause=order_by_clause)
        stmt = stmt.execution_options(include_deleted=include_deleted)
        stmt = paging_query_in.apply_to_query(stmt)
        data = (await db.execute(stmt)).all()

        meta = schemas.PagingMeta(
            total_data_count=total_count,
            current_page=paging_query_in.page,
            total_page_count=int(math.ceil(total_count / paging_query_in.per_page)),
            per_page=paging_query_in.per_page,
        )
        list_response = self.list_response_class(data=data, meta=meta)
        return list_response

    async def create(
        self,
        db: AsyncSession,
        create_schema: CreateSchemaType,
    ) -> ModelType:
        # by_alias=Falseにしないとalias側(CamenCase)が採用されてしまう
        create_dict = jsonable_encoder(create_schema, by_alias=False)
        exists_create_dict = self._filter_model_exists_fields(create_dict)
        db_obj = self.model(**exists_create_dict)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)

        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        update_schema: UpdateSchemaType,
    ) -> ModelType:
        # obj_inでセットされたスキーマをmodelの各カラムにUpdate
        db_obj_dict = jsonable_encoder(db_obj)
        update_dict = update_schema.dict(
            exclude_unset=True,
        )  # exclude_unset=Trueとすることで、未指定のカラムはUpdateしない
        for field in db_obj_dict:
            if field in update_dict:
                setattr(db_obj, field, update_dict[field])

        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, db_obj: ModelType) -> ModelType:
        """論理削除(soft delete)."""
        if not hasattr(db_obj, "deleted_at"):
            raise APIException(ErrorMessage.SOFT_DELETE_NOT_SUPPORTED)
        if db_obj.deleted_at:
            raise APIException(ErrorMessage.ALREADY_DELETED)

        db_obj.deleted_at = datetime.datetime.now(tz=datetime.timezone.utc)
        await db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def real_delete(self, db: AsyncSession, db_obj: ModelType) -> None:
        """実削除(real redele)."""
        await db.delete(db_obj)
        await db.flush()
