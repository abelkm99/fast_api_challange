from app.core.domain.commons.entities.base_entity import BaseEnum


class StatusEnum(BaseEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
