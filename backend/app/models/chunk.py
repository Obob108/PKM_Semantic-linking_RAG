from sqlalchemy import Column, Integer, Text, ForeignKey  
from app.core.database import Base
class Chunk(Base):
    __tablename__ = "chunks"
    id = Column(Integer, primary_key=True, index= True)
    document_id = Column( Integer, ForeignKey ("documents.id"), nullable=False)
    chunk_index= Column(Integer, nullable=False)
    content=Column(Text, nullable=False)
    chunk_index= Column(Integer, nullable= False)
    content= Column(Text, nullable= False)