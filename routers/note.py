# FastAPI & SQLAlchemy
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

# Dependencies
from dependencies import get_db
# Enums
from enums import NoteSortEnum, OrderEnum
# Note Model and Note Schema
from models.note import NoteModel
from schemas.note import Note, NoteRead, NoteQuery

# Router
router = APIRouter(
    prefix="/notes",
    tags=["Note"]
)

SORT_COLUMNS = {
    NoteSortEnum.ID: NoteModel.id,
    NoteSortEnum.TITLE: NoteModel.title,
    NoteSortEnum.CONTENT: NoteModel.content,
}

FILTER_COLUMNS = {
    "is_pinned": NoteModel.is_pinned,
    "is_archived": NoteModel.is_archived,
}

SEARCH_COLUMNS = [
    NoteModel.title,
    NoteModel.content,
]


@router.get("", response_model=list[NoteRead])
async def all_notes(query: NoteQuery = Depends(), db: Session = Depends(get_db)):
    notes = db.query(NoteModel)

    # Search
    if query.q:
        notes = notes.filter(
            or_(*[
                column.ilike(f"%{query.q}%")
                for column in SEARCH_COLUMNS
            ])
        )

    # Filter
    for field, column in FILTER_COLUMNS.items():
        value = getattr(query, field, None)

        if value is not None:
            notes = notes.filter(column == value)

    # Sort
    sort_column = SORT_COLUMNS[query.sort]

    notes = notes.order_by(
        sort_column.asc()
        if query.order == OrderEnum.ASC
        else sort_column.desc()
    )

    return notes.all()


@router.get("/{note_id}", response_model=NoteRead)
async def get_note(note_id: int, db: Session = Depends(get_db)):
    item = db.get(NoteModel, note_id)

    if not item:
        raise HTTPException(status_code=404, detail="Note note found")

    return item


@router.post("", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
async def create_note(note: Note, db: Session = Depends(get_db)):
    db_item = NoteModel(**note.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


@router.put("/{note_id}", response_model=NoteRead)
async def update_note(note_id: int, note: Note, db: Session = Depends(get_db)):
    item = db.get(NoteModel, note_id)

    if not item:
        raise HTTPException(status_code=404, detail="Note not found")

    for key, value in note.model_dump().items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)

    return item


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int, db: Session = Depends(get_db)):
    item = db.get(NoteModel, note_id)

    if not item:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(item)
    db.commit()

    return None
