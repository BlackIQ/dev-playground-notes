# BaseSchema
from database.base import BaseSchema


# Note Schema
class Note(BaseSchema):
    title: str
    content: str
    is_pinned: bool
    is_archived: bool


class NoteRead(Note):
    id: int
