def chunk_text(
    text: str,
    chunk_size: int = 500, ## why chunksize la 500 ky tu dem xuong overlap roi chunk2
    overlap: int = 100
) -> list[str]:
    if not text: return []
    if overlap >= chunk_size: raise ValueError("overlap always small than chunksize")
    chunks=[]
    start = 0 
    while start < len(text):
        end=start + chunk_size
        chunk= text[start:end].strip()
        if chunk: chunks.append(chunk)
        start += chunk_size - overlap 
    return chunks
