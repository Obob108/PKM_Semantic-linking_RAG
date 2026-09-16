# rule data api input and output 

from datetime import datetime
from pydantic import BaseModel

class DocumentCreate(BaseModel):
    title: str
    file_path: str
    file_type: str
    content: str | None = None

class DocumentResponse(BaseModel):
    id: int
    title: str
    file_path: str
    file_type: str
    content: str | None = None
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
    
class DocumentUpdate(BaseModel):
    title: str | None = None
    file_path: str | None = None
    file_type: str | None = None
    content: str | None = None
    