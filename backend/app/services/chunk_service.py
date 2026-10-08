from sqlalchemy.orm import Session

from app.models.chunk import Chunk


def save_chunks(
    db: Session,
    document_id: int,
    chunks: list[str]
):
    chunk_objects = []

    for index, content in enumerate(chunks):
        chunk = Chunk(
            document_id=document_id,
            chunk_index=index,
            content=content
        )

        chunk_objects.append(chunk)

    db.add_all(chunk_objects)
    db.commit()

    return chunk_objects