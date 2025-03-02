import enum
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, TypeVar

E = TypeVar("E", bound="BaseEnum")


def get_current_time():
    return datetime.now(tz=UTC)


@dataclass(kw_only=True)
class TimeStampedEntity:
    """A base class for entities with created_at and updated_at fields
    Attributes:
        created_at (datetime): The entity creation time
        updated_at (datetime): The entity update time
    """

    created_at: datetime = field(default_factory=get_current_time)
    updated_at: datetime = field(default_factory=get_current_time)


@dataclass(kw_only=True)
class UUIDEntity:
    """A base class for entities with a UUID as the primary key
    Attributes:
        id (uuid.UUID): The entity id
    """

    id: uuid.UUID = field(default_factory=uuid.uuid4)

    # # user the id as a hash
    def __hash__(self):
        return hash(str(self.id))

    # # use the id for equal comparison
    def __eq__(self, other):
        return str(self.id) == str(other.id)


@dataclass(kw_only=True)
class IDEntity:
    """A base class for entities with an integer as the primary key
    Attributes:
        id (int): The entity id

    """

    id: int

    # # user the id as a hash
    def __hash__(self):
        return hash(self.id)

    # # use the id for equal comparison
    def __eq__(self, other):
        return self.id == other.id


@dataclass(kw_only=True)
class BaseEntity(TimeStampedEntity, UUIDEntity):
    pass


@dataclass(kw_only=True)
class BaseEntityID(TimeStampedEntity, IDEntity):
    """A base class for entities with an integer as the primary key
    Attributes:
        id (int): The entity id
        created_at (datetime): The entity creation time
        updated_at (datetime): The entity update time
    """


class BaseEnum(enum.Enum):
    def __composite_values__(self):
        return (self.value,)

    @classmethod
    def get_value(cls: type[E], value: Any) -> E:
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"{cls.__name__} not found for value: {value}")
