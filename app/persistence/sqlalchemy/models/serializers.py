import uuid
from typing import Any

from pydantic import TypeAdapter
from sqlalchemy import TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import CHAR


class PydanticSerializer(TypeDecorator):
    impl = JSONB
    cache_ok = True

    def __init__(self, schema, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.schema = schema

    def process_bind_param(self, value, dialect):
        if value is None:
            return None  # Allow None values
        return TypeAdapter(self.schema).dump_python(value, mode="json")

    def process_result_value(self, value, dialect):
        if value is None:
            return None  # Allow None values
        return self.schema(**value)


class GUID(TypeDecorator):
    """Platform-independent GUID type.
    For MySQL, stores UUID as a 32-character hexadecimal string.
    """

    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if not isinstance(value, uuid.UUID):
            value = uuid.UUID(value)
        # Store UUID as a 32-character hex string
        return value.hex

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        return uuid.UUID(value)


def is_instance_of_schema(value: Any, schema: Any) -> bool:
    return isinstance(value, schema)
