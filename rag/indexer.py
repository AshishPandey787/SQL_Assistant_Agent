import os
import json
import numpy as np
import faiss

from rag.text_splitter import split_text
from llm.azure_openai import embed

KB_DIR = "knowledge_base"
INDEX_DIR = "rag_index"
DOCSTORE_PATH = os.path.join(INDEX_DIR, "docstore.json")
FAISS_PATH = os.path.join(INDEX_DIR, "faiss.index")

def build_index():
    os.makedirs(INDEX_DIR, exist_ok=True)

    documents = []
    for fn in os.listdir(KB_DIR):
        path = os.path.join(KB_DIR, fn)
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                raw = f.read()
            for chunk in split_text(raw):
                documents.append({"source": fn, "text": chunk})

    texts = [d["text"] for d in documents]
    vectors = embed(texts)
    vec = np.array(vectors, dtype="float32")

    index = faiss.IndexFlatIP(vec.shape[1])  # cosine if normalized; use dot product
    # Normalize for cosine similarity
    faiss.normalize_L2(vec)
    index.add(vec)

    faiss.write_index(index, FAISS_PATH)
    with open(DOCSTORE_PATH, "w", encoding="utf-8") as f:
        json.dump(documents, f, ensure_ascii=False, indent=2)

    print(f"Indexed {len(documents)} chunks.")
    print(f"Saved: {FAISS_PATH}, {DOCSTORE_PATH}")

if __name__ == "__main__":
    build_index()