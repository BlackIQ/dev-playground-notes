# SQLAlchemy & Pydantic
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import DeclarativeBase


# Base class for all SQLAlchemy models
class Base(DeclarativeBase):
    pass


# Base class for all Pydantic schemas
class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
