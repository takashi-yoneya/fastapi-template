import datetime
import math
from typing import Any, Generic, List, Optional, Type, TypeVar

from fastapi import Query
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload, query

import schemas
from core.database import Base
from exceptions.core import APIException
from exceptions.error_messages import ErrorMessage
from schemas.core import PagingQueryIn

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ListResponseSchemaType = TypeVar("ListResponseSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType, ListResponseSchemaType]):

    DELETE_FLG_LIST = [
        {"column": "disabled", "enable_value": False},
        {"column": "delete", "enable_value": False},
        {"column": "disable", "enable_value": False},
        {"column": "deleted", "enable_value": False},
        {"column": "deleted_at", "enable_value": None},
        {"column": "disabled_at", "enable_value": None},
    ]

    def __init__(self, model: Type[ModelType], list_response: ListResponseSchemaType):
        self.model = model
        self.list_response = list_response

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

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

        # 削除フラグの処理(DELETE_FLG_COLUMN_NAMESのいずれかに当てはまるカラムがあれば、=Falseでfilterする)
        if not return_deleted_data:
            for delete_flg in self.DELETE_FLG_LIST:
                delete_flg_column_obj = getattr(self.model, delete_flg.get("column"), None)
                if delete_flg_column_obj:
                    query = query.filter(delete_flg_column_obj == delete_flg.get("enable_value"))
                    break

        return query.all()

    def get_paged_list(
        self,
        db: Session,
        paging: PagingQueryIn,
        filtered_query: Optional[query.Query] = None,
        return_deleted_data: bool = False,
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

        # 削除フラグの処理(DELETE_FLG_COLUMN_NAMESのいずれかに当てはまるカラムがあれば、=Falseでfilterする)
        if not return_deleted_data:
            for delete_flg in self.DELETE_FLG_LIST:
                delete_flg_column_obj = getattr(self.model, delete_flg["column"], None)
                if delete_flg_column_obj:
                    query = query.filter(delete_flg_column_obj == delete_flg["enable_value"])
                    break

        # list_response = self.list_response.copy()
        total_data_count = query.count()
        query = paging.set_paging_query(query)
        data = query.all()
        meta = schemas.PagingMeta(
            total_data_count=total_data_count,
            current_page=paging.page,
            total_page_count=int(math.ceil(total_data_count / paging.per_page)),
        )
        self.list_response.data = data
        self.list_response.meta = meta
        return self.list_response

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType):
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

    def delete(self, db: Session, db_obj: ModelType):
        if db_obj.deleted_at:
            raise APIException(ErrorMessage.ALREADY_DELETED.make_error())
        db_obj.deleted_at = datetime.datetime.now()
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj
