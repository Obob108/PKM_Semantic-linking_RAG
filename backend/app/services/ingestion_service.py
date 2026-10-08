from pathlib import Path

from sqlalchemy.orm import Session

from app.models.document import Document
from app.services.parser_service import parse_document
from app.services.chunking_service import chunk_text
from app.services.chunk_service import save_chunks
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService


embedding_service = EmbeddingService()

vector_store = VectorStoreService(
    dimension=1024
)


def ingest_document(
    db: Session,
    file_path: str,
    chunk_size: int = 500,
    overlap: int = 100
):
    # 1. Parse
    text = parse_document(file_path)

    # 2. Chunk
    chunks = chunk_text(
        text,
        chunk_size=chunk_size,
        overlap=overlap
    )

    # 3. Create Document
    path = Path(file_path)

    document = Document(
        title=path.name,
        file_path=file_path,
        file_type=path.suffix.lower().replace(".", ""),
        content=text
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    # 4. Save chunks to SQLite
    saved_chunks = save_chunks(
        db=db,
        document_id=document.id,
        chunks=chunks
    )

    # 5. Create embeddings
    vectors = embedding_service.embed_texts(chunks)

    # 6. Get Chunk IDs
    chunk_ids = [
        chunk.id
        for chunk in saved_chunks
    ]

    # 7. Add vectors to FAISS
    vector_store.add_vectors(
        vectors=vectors,
        chunk_ids=chunk_ids
    )

    # 8. Persist FAISS
    vector_store.save()

    return document, saved_chunks