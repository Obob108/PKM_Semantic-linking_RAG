
import re

from rank_bm25 import BM25Okapi
from sqlalchemy.orm import Session

from app.models.chunk import Chunk


def tokenize(text: str) -> list[str]:
    """Tách văn bản thành các token đơn giản."""
    return re.findall(r"\w+", text.lower(), flags=re.UNICODE)


def bm25_search(
    db: Session,
    query: str,
    top_k: int = 5
) -> list[dict]:
    """Tìm các chunk liên quan đến query bằng BM25."""

    if not query.strip() or top_k <= 0:
        return []

    chunks = db.query(Chunk).all()

    if not chunks:
        return []

    tokenized_corpus = [
        tokenize(chunk.content)
        for chunk in chunks
    ]

    # Loại các chunk không có token.
    valid_pairs = [
        (chunk, tokens)
        for chunk, tokens in zip(chunks, tokenized_corpus)
        if tokens
    ]

    if not valid_pairs:
        return []

    valid_chunks = [pair[0] for pair in valid_pairs]
    tokenized_corpus = [pair[1] for pair in valid_pairs]

    bm25 = BM25Okapi(tokenized_corpus)
    query_tokens = tokenize(query)

    if not query_tokens:
        return []

    scores = bm25.get_scores(query_tokens)

    ranked_positions = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )

    results = []

    for position in ranked_positions:
        score = float(scores[position])

        # Không trả về chunk không khớp từ khóa.
        if score <= 0:
            continue

        chunk = valid_chunks[position]

        results.append({
            "chunk_id": chunk.id,
            "document_id": chunk.document_id,
            "score": score,
            "content": chunk.content
        })

        if len(results) >= top_k:
            break

    return results