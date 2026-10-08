from app.services.embedding_service import EmbeddingService


service = EmbeddingService()

texts = [
    "Machine Learning là một nhánh của Artificial Intelligence.",
    "Random Forest sử dụng nhiều Decision Tree.",
    "Python là một ngôn ngữ lập trình."
]


vectors = service.embed_texts(texts)


print("Number of texts:", len(texts))
print("Number of vectors:", len(vectors))

for i, vector in enumerate(vectors):
    print(
        f"Text {i}: "
        f"vector dimension = {len(vector)}"
    )