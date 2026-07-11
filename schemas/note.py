# Typing
from typing import Optional

# BaseSchema
from database.base import BaseSchema
# Enums
from enums import OrderEnum, NoteSortEnum


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

    sort: NoteSortEnum = NoteSortEnum.ID
    order: OrderEnum = OrderEnum.DESC
