import time
from app.rag.embedding import get_embedder
from app.rag.vectorstore import MilvusVectorStore
from app.observability.metrics import RAG_SEARCH_LATENCY

class Retriever:
    def __init__(self, collection: str = "rag_demo"):
        self.embedder = get_embedder()
        self.store = MilvusVectorStore(collection, dim=self.embedder.dim)

    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        start = time.time()
        q_emb = self.embedder.embed([query])[0]
        hits = self.store.search(q_emb, top_k=top_k)
        RAG_SEARCH_LATENCY.observe(time.time() - start)
        return hits