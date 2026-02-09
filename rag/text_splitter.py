def split_text(text: str, chunk_size: int = 900, overlap: int = 120) -> list[str]:
    text = text.replace("\r\n", "\n")
    chunks = []
    i = 0
    while i < len(text):
        end = min(len(text), i + chunk_size)
        chunk = text[i:end]
        chunks.append(chunk)
        i = end - overlap
        if i < 0:
            i = 0
        if end == len(text):
            break
    return [c.strip() for c in chunks if c.strip()]