from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService


# -------------------------
# 1. Embedding service
# -------------------------

embedding_service = EmbeddingService()


texts = [
    "Random Forest sử dụng nhiều Decision Tree.",
    "Machine Learning là một nhánh của Artificial Intelligence.",
    "Python là một ngôn ngữ lập trình."
]


vectors = embedding_service.embed_texts(texts)


print("=== EMBEDDINGS ===")
print("Number of vectors:", len(vectors))
print("Dimension:", len(vectors[0]))


# -------------------------
# 2. FAISS
# -------------------------

vector_store = VectorStoreService(
    dimension=len(vectors[0])
)


# Giả lập Chunk IDs trong SQLite
chunk_ids = [75, 76, 77]


vector_store.add_vectors(
    vectors=vectors,
    chunk_ids=chunk_ids
)


print("\n=== FAISS ===")

print(
    "Number of vectors in FAISS:",
    vector_store.index.ntotal
)


# -------------------------
# 3. Query
# -------------------------

query = "Random Forest dựa trên những cây quyết định nào?"


query_vector = embedding_service.embed_text(
    query
)


results = vector_store.search(
    query_vector=query_vector,
    top_k=3
)


print("\n=== SEARCH RESULTS ===")

for result in results:
    print(
        "Chunk ID:",
        result["chunk_id"],
        "| Score:",
        result["score"]
    )