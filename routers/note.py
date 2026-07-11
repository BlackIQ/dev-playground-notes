# FastAPI & SQLAlchemy
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Dependencies
from dependencies import get_db
# Note Model and Note Schema
from models.note import NoteModel
from schemas.note import Note, NoteRead, NoteQuery, NotesPaginated

# Router
router = APIRouter(
    prefix="/notes",
    tags=["Note"]
)


@router.get("", response_model=NotesPaginated)
async def all_notes(query: NoteQuery = Depends(), db: Session = Depends(get_db)):
    notes = db.query(NoteModel)

    if query.q:
        notes = notes.filter(
            NoteModel.title.contains(query.q) | NoteModel.content.contains(query.q)
        )

    if query.is_pinned is not None:
        notes = notes.filter(
            NoteModel.is_pinned == query.is_pinned
        )

    if query.is_archived is not None:
        notes = notes.filter(
            NoteModel.is_archived == query.is_archived
        )

    offset = (query.page - 1) * query.limit
    limit = query.limit

    total = db.query(NoteModel).count()

    return {
        "total": total,
        "page": query.page,
        "limit": limit,
        "items": notes.offset(offset).limit(limit).all()
    }


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

# Search

# Pagination
