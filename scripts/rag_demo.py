from app.rag.embedding import get_embedder
from app.rag.vectorstore import MilvusVectorStore
from app.security.audit import audit_log

def main():
    embedder = get_embedder()
    store = MilvusVectorStore("rag_demo", dim=embedder.dim)

    docs = [
        "Kubernetes uses liveness and readiness probes to manage pod health.",
        "Prometheus scrapes metrics endpoints and stores time-series data.",
        "RAG retrieves relevant chunks before the LLM generates an answer.",
        "Milvus is a vector database supporting HNSW and IVF indexes.",
        "SRE focuses on reliability, observability, and incident response.",
    ]
    sources = [f"doc_{i}" for i in range(len(docs))]

    n = store.insert(docs, embedder.embed(docs), sources)
    audit_log(actor="system", action="rag.ingest", resource="rag_demo",
              status="success", count=n)
    print(f"ingested {n} docs")

    query = "How does Kubernetes check if a container is healthy?"
    hits = store.search(embedder.embed([query])[0], top_k=3)
    print(f"\nQuery: {query}\n")
    for i, h in enumerate(hits, 1):
        print(f"{i}. score={h['score']:.4f} | {h['source']} | {h['text']}")

if __name__ == "__main__":
    main()