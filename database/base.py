# Pydantic
from pydantic import BaseModel, ConfigDict
# SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Mixins
from database.mixins import TimestampMixin, SoftDeleteMixin


# Base class for all SQLAlchemy models
class Base(TimestampMixin, SoftDeleteMixin, DeclarativeBase):
    pass


# Base class for all Pydantic schemas
class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
