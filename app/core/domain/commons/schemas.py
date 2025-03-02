from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class MetaData:
    total: int
    offset: int
    limit: int
    returned: int

    def kw_param(self):
        return {
            "total": self.total,
            "offset": self.offset,
            "limit": self.limit,
            "returned": self.returned,
        }


@dataclass
class Paginate(Generic[T]):
    items: list[T]
    meta_data: MetaData
