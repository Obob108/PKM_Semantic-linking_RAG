from app.core.database import SessionLocal
from app.services.ingestion_service import ingest_document


FILE_PATH = "data/documents/test.md"


db = SessionLocal()

document, chunks = ingest_document(
    db=db,
    file_path=FILE_PATH,
    chunk_size=100,
    overlap=20
)

print("=== DOCUMENT ===")

print("ID:", document.id)
print("Title:", document.title)
print("File type:", document.file_type)


print("\n=== CHUNKS ===")

for chunk in chunks:
    print(
        f"Chunk ID: {chunk.id} | "
        f"Document ID: {chunk.document_id} | "
        f"Index: {chunk.chunk_index}"
    )


print("\n=== INGESTION COMPLETE ===")

db.close()