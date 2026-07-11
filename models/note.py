# SQLAlchemy DataTypes
from sqlalchemy import Column, Integer, String, Boolean

# BaseModel
from database.base import Base


# Note Model
class NoteModel(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    is_pinned = Column(Boolean, nullable=False)
    is_archived = Column(Boolean, nullable=False)
