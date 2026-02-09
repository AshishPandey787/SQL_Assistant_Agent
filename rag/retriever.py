import os
import json
import numpy as np
import faiss
from core.config import settings
from llm.azure_openai import embed

INDEX_DIR = "rag_index"
DOCSTORE_PATH = os.path.join(INDEX_DIR, "docstore.json")
FAISS_PATH = os.path.join(INDEX_DIR, "faiss.index")

class Retriever:
    def __init__(self):
        self.index = faiss.read_index(FAISS_PATH)
        with open(DOCSTORE_PATH, "r", encoding="utf-8") as f:
            self.docs = json.load(f)

    def retrieve(self, query: str, top_k: int | None = None) -> str:
        k = top_k or settings.RAG_TOP_K
        qv = np.array(embed([query]), dtype="float32")
        faiss.normalize_L2(qv)
        scores, ids = self.index.search(qv, k)

        selected = []
        for idx in ids[0]:
            if idx == -1:
                continue
            selected.append(self.docs[idx])

        context = "\n\n".join(
            [f"[source={d['source']}]\n{d['text']}" for d in selected]
        )
        return context[: settings.MAX_CONTEXT_CHARS]