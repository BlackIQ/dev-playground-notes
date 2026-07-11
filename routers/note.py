# FastAPI & SQLAlchemy
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Dependencies
from dependencies import get_db
# Note Model and Note Schema
from models.note import NoteModel
from schemas.note import Note, NoteRead

# Router
router = APIRouter(
    prefix="/notes",
    tags=["Note"]
)


# Get all notes
@router.get("", response_model=list[NoteRead])
async def all_notes(db: Session = Depends(get_db)):
    return db.query(NoteModel).all()


# Get one note
@router.get("/{note_id}", response_model=NoteRead)
async def get_note(note_id: int, db: Session = Depends(get_db)):
    item = db.get(NoteModel, note_id)

    if not item:
        raise HTTPException(status_code=404, detail="Note note found")

    return item


# Create note
@router.post("", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
async def create_note(note: Note, db: Session = Depends(get_db)):
    db_item = NoteModel(**note.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


# Update note
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


# Delete note
@router.delete("/{note_id}", response_model=NoteRead, status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int, db: Session = Depends(get_db)):
    item = db.get(NoteModel, note_id)

    if not item:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(item)
    db.commit()

    return None

# Search
