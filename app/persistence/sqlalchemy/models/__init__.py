from sqlalchemy.orm import registry

from app.persistence.sqlalchemy.models.user_model import map_user_tables


def map_models(mapper_registry: registry):
    map_user_tables(mapper_registry)
    return mapper_registry
