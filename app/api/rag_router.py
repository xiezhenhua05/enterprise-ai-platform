from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.rag.pipeline import RAGPipeline

router = APIRouter(prefix="/rag", tags=["rag"])

_pipeline: RAGPipeline | None = None
def get_pipeline() -> RAGPipeline:
    global _pipeline
    if _pipeline is None:            # Lazy loading: Initialize on the first request.
        _pipeline = RAGPipeline()
    return _pipeline

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    top_k: int = Field(5, ge=1, le=20)

class QueryResponse(BaseModel):
    answer: str
    sources: list
    blocked: bool = False
    usage: dict = {}

@router.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest):
    result = get_pipeline().answer(req.question, req.top_k)
    return QueryResponse(**result)