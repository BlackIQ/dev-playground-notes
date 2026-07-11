# BaseSchema
# Typing
from typing import Optional

from database.base import BaseSchema


# Note Schema
class Note(BaseSchema):
    title: str
    content: str
    is_pinned: bool
    is_archived: bool


class NoteRead(Note):
    id: int


# Query String Schema
class NoteQuery(BaseSchema):
    q: Optional[str] = None

    is_pinned: Optional[bool] = None
    is_archived: Optional[bool] = None

    sort: Optional[str] = None
    order: Optional[str] = "desc"

    page: int = 1
    limit: int = 20
