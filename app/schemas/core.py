from enum import Enum
from typing import Any

from fastapi import Query
from humps import camel
from pydantic import BaseModel, validator
from sqlalchemy import desc


def to_camel(string: str) -> str:
    return camel.case(string)


class BaseSchema(BaseModel):
    # @validator("*", pre=True)
    # def cast_someone(cls, v):
    #     '''
    #     全ての項目に対して、pre処理を行いたい場合の例
    #     '''
    #     if isinstance(v, Any):
      # @validator("*", pre=True)
    # def split_comma(cls, v):
    #     '''
    #     カンマでsplitする例
    #     '''
    #     if isinstance(v, str):
      class Config:
        """# キャメルケース　<-> スネークケースの自動変換
        pythonではスネークケースを使用するが、Javascriptではキャメルケースを使用する場合が多いため
        変換する必要がある.
        """

        alias_generator = to_camel
        allow_population_by_field_name = True


class PagingMeta(BaseSchema):
    current_page: int
    total_page_count: int
    total_data_count: int
    per_page: int


class PagingQueryIn(BaseSchema):
    page: int = Query(1)
    per_page: int = Query(30)

    @validator("page")
    def validate_page(cls, v: int) -> int:
        return 1 if not v >= 1 else v

    @validator("per_page")
    def validate_per_page(cls, v: int) -> int:
        return 30 if not v >= 1 else v

    def get_offset(self) -> int:
        return (
            (self.page - 1) * self.per_page
            if self.page >= 1 and self.per_page >= 1
            else 0
        )

    def apply_to_query(self, query: Any) -> Any:
        offset = self.get_offset()
        return query.offset(offset).limit(self.per_page)


class SortDirectionEnum(Enum):
    asc: str = "asc"
    desc: str = "desc"


class SortQueryIn(BaseSchema):
    sort_field: Any | None = Query(None)
    direction: SortDirectionEnum = Query(SortDirectionEnum.asc)

    def apply_to_query(self, query: Any, order_by_clause: Any | None = None) -> Any:
        if not order_by_clause:
            return query

        if self.direction == SortDirectionEnum.desc:
            return query.order_by(desc(order_by_clause))
        else:
            return query.order_by(order_by_clause)


class FilterQueryIn(BaseSchema):
    sort: str = Query(None)
    direction: str = Query(None)
    start: int | None = Query(None)
    end: int | None = Query(None)

    @validator("direction")
    def validate_direction(cls, v: str) -> str:
        if not v:
            return "asc"
        if v not in ["asc", "desc"]:
            msg = "asc or desc only"
            raise ValueError(msg)
        return v

    def validate_allowed_sort_column(self, allowed_columns: list[str]) -> bool:
        if not self.sort:
            return True
        return self.sort in allowed_columns
