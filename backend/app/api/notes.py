from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 

from app.core.database import get_db
from app.models.note import Note 
from app.schemas.note import NoteCreate, NoteResponse , NoteUpdate

router = APIRouter(
    prefix="/api/notes",
    tags=["Notes"],
)

@router.post("/", response_model=NoteResponse)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    new_note = Note(
        title=note.title,
        content=note.content
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


@router.get("/", response_model=list[NoteResponse])
def read_notes(db: Session = Depends(get_db)):
    return db.query(Note).all()


@router.get("/{note_id}", response_model=NoteResponse)
def read_note(note_id: int, db: Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.id == note_id).first()

    if not db_note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    return db_note

@router.put("/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, note: NoteUpdate, db: Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    if note.title is not None:
        db_note.title = note.title
    if note.content is not None:
        db_note.content = note.content

    db.commit()
    db.refresh(db_note)
    return db_note


@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(db_note)
    db.commit()
    return {"message": "Note deleted"}
    