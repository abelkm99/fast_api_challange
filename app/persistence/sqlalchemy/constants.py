from sqlalchemy.orm import registry

MapperRegistry = registry()


def init_mapper():
    from app.persistence.sqlalchemy.models import map_models

    map_models(MapperRegistry)
