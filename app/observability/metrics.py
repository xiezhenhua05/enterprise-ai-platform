from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests",["method", "endpoint", "status"],)
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "HTTP request latency",["endpoint"],)
EMBEDDING_LATENCY = Histogram("embedding_duration_seconds", "Embedding computation latency")
RAG_SEARCH_LATENCY = Histogram("rag_search_duration_seconds", "Vector search latency")
LLM_LATENCY = Histogram("llm_duration_seconds", "LLM call latency")
LLM_TOKENS = Counter("llm_tokens_total", "LLM token usage", ["type"])

def metrics_payload():
    return generate_latest(), CONTENT_TYPE_LATEST