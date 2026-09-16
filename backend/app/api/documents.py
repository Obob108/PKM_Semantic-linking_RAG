from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentResponse, DocumentUpdate
router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"],
)

@router.post("/", response_model=DocumentResponse)
def create_document(
    document: DocumentCreate,
    db: Session = Depends(get_db)
):
    new_document = Document(
        title=document.title,
        file_path=document.file_path,
        file_type=document.file_type,
        content=document.content
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return new_document


@router.get("/", response_model=list[DocumentResponse])
def read_documents(db: Session = Depends(get_db)):
    return db.query(Document).all()


@router.get("/{document_id}", response_model=DocumentResponse)
def read_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    db_document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if db_document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return db_document

@router.put("/{document_id}", response_model=DocumentResponse)
def update_document(
    document_id: int,
    document: DocumentUpdate,
    db: Session = Depends(get_db)
):
    db_document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )
    if db_document is None: raise HTTPException( status_code=404, detail="Document not found" )
    if document.title is not None:
        db_document.title = document.title
    if document.file_path is not None:
        db_document.file_path = document.file_path
    if document.file_type is not None:
        db_document.file_type = document.file_type
    if document.content is not None:
        db_document.content = document.content

    db.commit()
    db.refresh(db_document)

    return db_document

@router.delete("/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    db_document = db.query(Document).filter(Document.id == document_id).first()

    if db_document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    db.delete(db_document)
    db.commit()

    return {"message": "Document deleted"}