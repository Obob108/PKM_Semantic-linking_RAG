from app.core.database import SessionLocal
from app.models.document import Document
from app.services.parser_service import parse_document
from app.services.chunking_service import chunk_text
from app.services.chunk_service import save_chunks


FILE_PATH = "data/documents/test.md"


db = SessionLocal()


# 1. Đọc file
text = parse_document(FILE_PATH)

print("=== PARSED TEXT ===")
print(text)


# 2. Chia text thành chunks
chunks = chunk_text(
    text,
    chunk_size=100,
    overlap=20
)

print("\n=== CHUNKS ===")

for index, chunk in enumerate(chunks):
    print(f"\nChunk {index}:")
    print(chunk)


# 3. Tạo Document
document = Document(
    title="test.md",
    file_path=FILE_PATH,
    file_type="md",
    content=text
)

db.add(document)
db.commit()
db.refresh(document)


print("\nDocument ID:", document.id)


# 4. Lưu chunks vào database
saved_chunks = save_chunks(
    db=db,
    document_id=document.id,
    chunks=chunks
)


print("\n=== SAVED CHUNKS ===")

for chunk in saved_chunks:
    print(
        f"Chunk ID: {chunk.id} | "
        f"Document ID: {chunk.document_id} | "
        f"Index: {chunk.chunk_index}"
    )


db.close()