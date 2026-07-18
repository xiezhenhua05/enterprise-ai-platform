import time
from abc import ABC, abstractmethod
from functools import lru_cache
from app.core.config import get_settings
from app.observability.metrics import EMBEDDING_LATENCY

class BaseEmbedder(ABC):
    dim: int
    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        ...

class LocalBGEEmbedder(BaseEmbedder):
    """本地BGE模型, 归一化输出, 配合Milvus IP=cosine。"""
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)
        self.dim = self.model.get_sentence_embedding_dimension()  # 384

    def embed(self, texts: list[str]) -> list[list[float]]:
        start = time.time()
        vecs = self.model.encode(texts, normalize_embeddings=True)
        EMBEDDING_LATENCY.observe(time.time() - start)
        return vecs.tolist()

class OpenAIEmbedder(BaseEmbedder):
    """Week3可切换。占位, 保持接口一致。"""
    dim = 1536
    def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError("enable in Week3")

@lru_cache
def get_embedder() -> BaseEmbedder:
    # 依赖倒置: 业务代码只依赖 BaseEmbedder, 不关心具体实现
    return LocalBGEEmbedder()