from fastapi import FastAPI

from app.core.database import engine, Base
from app.models.document import Document
from app.models.note import Note
from app.api.notes import router as note_router 
from app.api.documents import router as document_router 

Base.metadata.create_all(bind=engine)



app = FastAPI( 
    title="PKM System",
    version="1.0"
)
app.include_router(document_router)
app.include_router(note_router)
@app.get("/health")
def health_check():
        return{
            "status":"ok",
            "message": "PKM backend is running"
        }