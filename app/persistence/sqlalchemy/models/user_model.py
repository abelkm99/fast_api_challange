import uuid

from sqlalchemy import Boolean, Column, DateTime, String, Table, false, func
from sqlalchemy.orm import registry, relationship

from app.core.domain.user.entities import (
    UserEntity,
)
from app.persistence.sqlalchemy.constants import MapperRegistry
from app.persistence.sqlalchemy.models.serializers import GUID

UserTable = Table(
    "users",
    MapperRegistry.metadata,
    Column("id", GUID(), primary_key=True, default=uuid.uuid4, unique=True, index=True),
    Column("email_address", String(100), unique=True, nullable=False),
    Column("password", String(1000), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
    Column("is_archived", Boolean, nullable=False, server_default=false()),
    Column("is_activated", Boolean, nullable=False, server_default=false()),
)


def map_user_tables(mapper_registry: registry):
    mapper_registry.map_imperatively(
        UserEntity,
        UserTable,
        properties={
            "id": UserTable.c.id,
            "email_address": UserTable.c.email_address,
            "password": UserTable.c.password,
            "created_at": UserTable.c.created_at,
            "updated_at": UserTable.c.updated_at,
            "is_archived": UserTable.c.is_archived,
            "is_activated": UserTable.c.is_activated,
            "posts": relationship(
                "PostEntity",
                back_populates="user",
                cascade="all, delete",
                passive_deletes=True,
            ),
        },
    )
