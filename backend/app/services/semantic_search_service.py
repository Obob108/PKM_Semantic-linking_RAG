from sqlalchemy.orm import Session

from app.models.chunk import Chunk
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService


embedding_service = EmbeddingService()

vector_store = VectorStoreService(
    dimension=1024
)


def semantic_search(
    db: Session,
    query: str,
    top_k: int = 5
):
    # 1. Chuyển câu hỏi thành vector
    query_vector = embedding_service.embed_text(query)

    # 2. Tìm vector gần nhất trong FAISS
    vector_results = vector_store.search(
        query_vector=query_vector,
        top_k=top_k
    )

    results = []

    # 3. Lấy chunk tương ứng từ SQLite
    for result in vector_results:

        chunk = db.query(Chunk).filter(
            Chunk.id == result["chunk_id"]
        ).first()

        if chunk is None:
            continue

        results.append({
            "chunk_id": chunk.id,
            "document_id": chunk.document_id,
            "score": result["score"],
            "content": chunk.content
        })

    return results