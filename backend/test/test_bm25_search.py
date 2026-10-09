

from app.core.database import SessionLocal
from app.services.bm25_service import bm25_search

db = SessionLocal()

try:
    query = "Random Forest Decision Tree"

    results = bm25_search(
        db=db,
        query=query,
        top_k=5
    )

    print("=== BM25 SEARCH ===")
    print("Query:", query)

    for i, result in enumerate(results, start=1):
        print(f"\n--- Result {i} ---")
        print("Chunk ID:", result["chunk_id"])
        print("Document ID:", result["document_id"])
        print("Score:", result["score"])
        print("Content:", result["content"])
finally:
    db.close()