from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService


# =====================================
# 1. Tạo embeddings
# =====================================

embedding_service = EmbeddingService()

texts = [
    "Random Forest sử dụng nhiều Decision Tree.",
    "Machine Learning là một nhánh của Artificial Intelligence.",
    "Python là một ngôn ngữ lập trình."
]

vectors = embedding_service.embed_texts(texts)


# =====================================
# 2. Tạo vector store
# =====================================

store = VectorStoreService(
    dimension=len(vectors[0])
)

chunk_ids = [75, 76, 77]

store.add_vectors(
    vectors=vectors,
    chunk_ids=chunk_ids
)


print("=== BEFORE SAVE ===")

print(
    "FAISS vectors:",
    store.index.ntotal
)

print(
    "Chunk IDs:",
    store.chunk_ids
)


# =====================================
# 3. Save
# =====================================

store.save()

print("\n=== SAVED ===")

print("FAISS index saved.")
print("Mapping saved.")


# =====================================
# 4. Tạo store mới
# =====================================

loaded_store = VectorStoreService(
    dimension=1024
)

loaded_store.load()


print("\n=== AFTER LOAD ===")

print(
    "FAISS vectors:",
    loaded_store.index.ntotal
)

print(
    "Chunk IDs:",
    loaded_store.chunk_ids
)


# =====================================
# 5. Search sau khi load
# =====================================

query = "Random Forest dựa trên những cây quyết định nào?"

query_vector = embedding_service.embed_text(
    query
)

results = loaded_store.search(
    query_vector=query_vector,
    top_k=3
)


print("\n=== SEARCH AFTER LOAD ===")

for result in results:
    print(
        "Chunk ID:",
        result["chunk_id"],
        "| Score:",
        result["score"]
    )