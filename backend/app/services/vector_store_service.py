from pathlib import Path
import json

import faiss
import numpy as np


class VectorStoreService:

    def __init__(
        self,
        dimension: int,
        index_path: str = "data/index/faiss.index",
        mapping_path: str = "data/index/chunk_ids.json"
    ):
        self.dimension = dimension

        self.index_path = Path(index_path)
        self.mapping_path = Path(mapping_path)

        self.index_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.index = faiss.IndexFlatIP(dimension)

        # FAISS position -> Chunk ID
        self.chunk_ids = []

        # Nếu đã có index thì load
        if self.index_path.exists() and self.mapping_path.exists():
            self.load()

    def add_vectors(
        self,
        vectors: list[list[float]],
        chunk_ids: list[int]
    ):
        if len(vectors) != len(chunk_ids):
            raise ValueError(
                "Số lượng vectors phải bằng số lượng chunk_ids"
            )

        if not vectors:
            return

        vector_array = np.array(
            vectors,
            dtype="float32"
        )

        if vector_array.shape[1] != self.dimension:
            raise ValueError(
                f"Vector dimension phải là {self.dimension}"
            )

        self.index.add(vector_array)

        self.chunk_ids.extend(chunk_ids)

    def search(
        self,
        query_vector: list[float],
        top_k: int = 5
    ):
        if self.index.ntotal == 0:
            return []

        query_array = np.array(
            [query_vector],
            dtype="float32"
        )

        if query_array.shape[1] != self.dimension:
            raise ValueError(
                f"Query vector dimension phải là {self.dimension}"
            )

        scores, positions = self.index.search(
            query_array,
            min(top_k, self.index.ntotal)
        )

        results = []

        for score, position in zip(
            scores[0],
            positions[0]
        ):
            chunk_id = self.chunk_ids[position]

            results.append({
                "chunk_id": chunk_id,
                "score": float(score)
            })

        return results

    def save(self):
        faiss.write_index(
            self.index,
            str(self.index_path)
        )

        with open(
            self.mapping_path,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                self.chunk_ids,
                file,
                ensure_ascii=False,
                indent=2
            )

    def load(self):
        self.index = faiss.read_index(
            str(self.index_path)
        )

        with open(
            self.mapping_path,
            "r",
            encoding="utf-8"
        ) as file:
            self.chunk_ids = json.load(file)

        if self.index.ntotal != len(self.chunk_ids):
            raise ValueError(
                "FAISS index và chunk_ids không khớp"
            )

        if self.index.d != self.dimension:
            raise ValueError(
                f"FAISS dimension phải là {self.dimension}"
            )