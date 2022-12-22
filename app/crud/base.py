import datetime
import math
from typing import Any, Generic, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session, query

from app import schemas
from app.core.database import Base
from app.exceptions.core import APIException
from app.exceptions.error_messages import ErrorMessage
from app.schemas.core import PagingQueryIn

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseModel)
ListResponseSchemaType = TypeVar("ListResponseSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType, ListResponseSchemaType]):
    def __init__(self, model: Type[ModelType], list_response_class: Type[ListResponseSchemaType]):
        self.model = model
        self.list_response_class = list_response_class

    def get(
        self,
        db: Session,
        id: Any,
        include_deleted: bool = False,
    ) -> Optional[ModelType]:
        # for field in response_schema.dict():

        # for field in response_schema.dict():
        #     if field in self.model.__dict__:
        #         setattr(self.model, field, update_dict[field])
        # if not select_query:
        #     query = db.query(self.model)
        # else:
        #     query = db.query(*select_query)
        query = db.query(self.model)

        return query.filter(self.model.id == id).execution_options(include_deleted=include_deleted).first()

    def get_list(
        self,
        db: Session,
        filtered_query: Optional[query.Query] = None,
        return_deleted_data: bool = False,
    ) -> List[ModelType]:
        if filtered_query:
            query = filtered_query
        else:
            query = db.query(self.model)

        return query.all()

    def get_paged_list(
        self,
        db: Session,
        paging: PagingQueryIn,
        filtered_query: Optional[query.Query] = None,
    ) -> ListResponseSchemaType:
        """
        Notes:
            filtered_queryにフィルタ済のqueryを渡すとページングした結果を返す
            return_deleted_data=Trueの場合は、削除フラグ=Trueのデータも返す
        """
        # offset = (page - 1) * per_page if page and page >= 1 else 0

        if filtered_query:
            query = filtered_query
        else:
            query = self.model

        # list_response = self.list_response.copy()
        total_data_count = query.count()
        query = paging.set_paging_query(query)
        data = query.all()
        meta = schemas.PagingMeta(
            total_data_count=total_data_count,
            current_page=paging.page,
            total_page_count=int(math.ceil(total_data_count / paging.per_page)),
        )
        list_response = self.list_response_class(data=data, meta=meta)
        return list_response

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        # by_alias=Falseにしないとalias側(CamenCase)が採用されてしまう
        obj_in_data = jsonable_encoder(obj_in, by_alias=False)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)

        return db_obj

    def update(self, db: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        # obj_inでセットされたスキーマをmodelの各カラムにUpdate
        db_obj_dict = jsonable_encoder(db_obj)
        update_dict = obj_in.dict(exclude_unset=True)  # exclude_unset=Trueとすることで、未指定のカラムはUpdateしない
        for field in db_obj_dict:
            if field in update_dict:
                setattr(db_obj, field, update_dict[field])

        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: ModelType) -> ModelType:
        if db_obj.deleted_at:
            raise APIException(ErrorMessage.ALREADY_DELETED)
        db_obj.deleted_at = datetime.datetime.now()
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj
