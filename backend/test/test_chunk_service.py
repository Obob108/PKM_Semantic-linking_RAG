from app.core.database import SessionLocal
from app.models.document import Document
from app.services.chunk_service import save_chunks


db = SessionLocal()


# 1. Tạo một document để chunk có document_id
document = Document(
    title="Test Chunk Service",
    file_path="data/documents/test.md",
    file_type="md",
    content="Test document for chunk service."
)

db.add(document)
db.commit()
db.refresh(document)


print("Document ID:", document.id)


# 2. Tạo các chunk giả để test
chunks = [
    "Machine Learning là một nhánh của Artificial Intelligence.",
    "Random Forest sử dụng nhiều Decision Tree.",
    "Random Forest là một ensemble learning method."
]


# 3. Lưu chunks vào database
saved_chunks = save_chunks(
    db=db,
    document_id=document.id,
    chunks=chunks
)


# 4. In kết quả
for chunk in saved_chunks:
    print(
        "Chunk ID:", chunk.id,
        "| Document ID:", chunk.document_id,
        "| Index:", chunk.chunk_index,
        "| Content:", chunk.content
    )


db.close()