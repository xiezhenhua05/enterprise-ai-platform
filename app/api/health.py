from fastapi import APIRouter
from app.core.config import get_settings
from app.rag.vectorstore import MilvusVectorStore

router = APIRouter(tags=["health"])

@router.get("/health")
async def health():
    s = get_settings()
    return {"status": "ok", "app": s.app_name, "env": s.environment}

@router.get("/ready")
async def ready():
    milvus_ok = MilvusVectorStore.ping()
    status = "ready" if milvus_ok else "degraded"
    return {"status": status,
            "deps": {"milvus": "up" if milvus_ok else "down"}}