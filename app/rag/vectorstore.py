import logging
from pymilvus import (
    connections, utility, Collection,
    CollectionSchema, FieldSchema, DataType,
)
from app.core.config import get_settings

logger = logging.getLogger("rag.vectorstore")

class MilvusVectorStore:
    def __init__(self, collection_name: str, dim: int):
        s = get_settings()
        connections.connect(alias="default", host=s.milvus_host, port=s.milvus_port)
        self.collection_name = collection_name
        self.dim = dim
        self.collection = self._ensure_collection()

    def _ensure_collection(self) -> Collection:
        if utility.has_collection(self.collection_name):
            return Collection(self.collection_name)
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=512),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=self.dim),
        ]
        schema = CollectionSchema(fields, description="RAG document chunks")
        coll = Collection(self.collection_name, schema)
        coll.create_index(
            field_name="embedding",
            index_params={
                "index_type": "HNSW",
                "metric_type": "IP",   # 归一化后 IP=cosine
                "params": {"M": 16, "efConstruction": 200},
            },
        )
        logger.info(f"created collection {self.collection_name} dim={self.dim}")
        return coll

    def insert(self, texts: list[str], embeddings: list[list[float]], sources: list[str]) -> int:
        # 字段顺序对应非auto_id字段: text, source, embedding
        self.collection.insert([texts, sources, embeddings])
        self.collection.flush()
        return len(texts)

    def search(self, query_embedding: list[float], top_k: int = 5) -> list[dict]:
        self.collection.load()
        results = self.collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param={"metric_type": "IP", "params": {"ef": 64}},
            limit=top_k,
            output_fields=["text", "source"],
        )
        return [
            {"text": h.entity.get("text"), "source": h.entity.get("source"),
             "score": float(h.distance)}
            for h in results[0]
        ]

    @staticmethod
    def ping() -> bool:
        try:
            s = get_settings()
            connections.connect(alias="health", host=s.milvus_host, port=s.milvus_port)
            ok = utility.get_server_version(using="health") is not None
            return ok
        except Exception:
            return False