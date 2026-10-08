from sentence_transformers import SentenceTransformer


MODEL_NAME = "BAAI/bge-m3"


class EmbeddingService:

    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)

    def embed_text(self, text: str):
        if not text:
            return []

        vector = self.model.encode(
            text,
            normalize_embeddings=True
        )

        return vector.tolist()

    def embed_texts(self, texts: list[str]):
        if not texts:
            return []

        vectors = self.model.encode(
            texts,
            normalize_embeddings=True
        )

        return vectors.tolist()