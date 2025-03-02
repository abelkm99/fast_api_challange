from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class MetaDataSchema(BaseModel):
    total: int
    offset: int
    limit: int
    returned: int


class PaginateSchema(BaseModel, Generic[T]):
    items: list[T]
    meta_data: MetaDataSchema


class LimitOffset(BaseModel):
    limit: int = 10
    offset: int = 0
