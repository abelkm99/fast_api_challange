import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Table, Text, func
from sqlalchemy.orm import registry, relationship

from app.core.domain.post.entities import PostEntity  # adjust the import path as needed
from app.persistence.sqlalchemy.constants import MapperRegistry
from app.persistence.sqlalchemy.models.serializers import GUID

# Define the posts table
PostTable = Table(
    "posts",
    MapperRegistry.metadata,
    Column("id", GUID(), primary_key=True, default=uuid.uuid4, unique=True, index=True),
    Column("user_id", GUID(), ForeignKey("users.id"), nullable=False),
    Column("text", Text, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
)


def map_post_tables(mapper_registry: registry):
    mapper_registry.map_imperatively(
        PostEntity,
        PostTable,
        properties={
            "id": PostTable.c.id,
            "user_id": PostTable.c.user_id,
            "text": PostTable.c.text,
            "created_at": PostTable.c.created_at,
            "updated_at": PostTable.c.updated_at,
            "user": relationship(
                "UserEntity",
                uselist=False,
                back_populates="posts",
            ),
        },
    )
