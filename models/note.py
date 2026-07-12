# SQLAlchemy ORM
from sqlalchemy.orm import Mapped, mapped_column

# BaseModel & Mixins
from database import Base


# Note Model
class NoteModel(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )
    title: Mapped[str] = mapped_column(
        nullable=False
    )
    content: Mapped[str] = mapped_column(
        nullable=False
    )
    is_pinned: Mapped[bool] = mapped_column(
        default=False,
        nullable=False
    )
    is_archived: Mapped[bool] = mapped_column(
        default=False,
        nullable=False
    )
