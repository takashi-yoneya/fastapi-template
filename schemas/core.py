from typing import Optional, List
from pydantic import BaseModel, validator
from fastapi import Query


class PagingMeta(BaseModel):
    current_page: int
    total_page_count: int
    total_data_count: int


class PagingQueryIn(BaseModel):
    page: int = Query(1)
    per_page: int = Query(30)  
    
    @validator("page")
    def validate_page(cls, v):
         return 1 if not v >= 1 else v
     
    @validator("per_page")
    def validate_per_page(cls, v):
         return 30 if not v >= 1 else v
    
    def get_offset(self):
        return (self.page-1) * self.per_page if self.page >= 1 and self.per_page >= 1 else 0
      
    def set_paging_query(self, query):
        offset = self.get_offset()
        return query.offset(offset).limit(self.per_page)