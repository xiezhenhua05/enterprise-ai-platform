from fastapi import APIRouter
from app.core.config import get_settings
router = APIRouter(tags=["health"])
@router.get("/health")
async def health():
    s = get_settings()
    return {"status": "ok", "app": s.app_name, "env": s.environment}
@router.get("/ready")
async def ready():
    # Week2起在此检查 Redis / Milvus 连接
    return {"status": "ready", "deps": {"redis": "pending", "milvus": "pending"}}
