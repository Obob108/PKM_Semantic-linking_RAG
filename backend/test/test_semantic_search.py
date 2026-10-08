from app.core.database import SessionLocal
from app.services.semantic_search_service import semantic_search


db = SessionLocal()

query = "Random Forest dựa trên những cây quyết định nào?"

results = semantic_search(
    db=db,
    query=query,
    top_k=5
)

print("=== SEMANTIC SEARCH ===")
print("Query:", query)

for i, result in enumerate(results, start=1):

    print(f"\n--- Result {i} ---")
    print("Chunk ID:", result["chunk_id"])
    print("Document ID:", result["document_id"])
    print("Score:", result["score"])
    print("Content:")
    print(result["content"])


db.close()