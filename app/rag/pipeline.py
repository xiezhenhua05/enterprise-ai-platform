from app.rag.retriever import Retriever
from app.models.provider import get_llm
from app.security.guardrail import check_prompt_injection
from app.security.audit import audit_log

SYSTEM_PROMPT = (
    "You are a precise assistant. Answer ONLY using the provided context. "
    "If the context does not contain the answer, reply exactly: "
    "'I don't have enough information to answer that.' "
    "Always cite sources in the form [source] after each claim."
)

class RAGPipeline:
    def __init__(self, collection: str = "rag_demo"):
        self.retriever = Retriever(collection)
        self.llm = get_llm()

    def answer(self, question: str, top_k: int = 5) -> dict:
        # 1) Security: Block prompt injection attacks.
        if check_prompt_injection(question):
            audit_log(actor="user", action="rag.blocked",
                      resource="rag_query", status="blocked")
            return {"answer": "Request blocked by guardrail.",
                    "sources": [], "blocked": True, "usage": {}}
        # 2) Retrieve relevant documents.
        hits = self.retriever.retrieve(question, top_k=top_k)
        context = "\n\n".join(f"[{h['source']}] {h['text']}" for h in hits)
        # 3) Build the prompt.
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",
             "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ]
        # 4) Generate the response.
        result = self.llm.chat(messages)
        audit_log(actor="user", action="rag.query", resource="rag_query",
                  status="success", tokens=result["usage"].get("total_tokens"))
        return {
            "answer": result["content"],
            "sources": [{"source": h["source"], "score": round(h["score"], 4)}
                        for h in hits],
            "usage": result["usage"],
            "blocked": False,
        }