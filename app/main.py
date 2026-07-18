import time, uuid
from fastapi import FastAPI, Request, Response
from app.core.config import get_settings
from app.core.logging import setup_logging, trace_id_var
from app.observability.metrics import REQUEST_COUNT, REQUEST_LATENCY, metrics_payload
from app.api import health

settings = get_settings()
setup_logging(settings.log_level)
app = FastAPI(title=settings.app_name)

@app.middleware("http")
async def observability_mw(request: Request, call_next):
    trace_id = request.headers.get("X-Trace-Id", str(uuid.uuid4()))
    trace_id_var.set(trace_id)
    start = time.time()
    response = await call_next(request)
    REQUEST_COUNT.labels(request.method, request.url.path, response.status_code).inc()
    REQUEST_LATENCY.labels(request.url.path).observe(time.time() - start)
    response.headers["X-Trace-Id"] = trace_id
    return response

@app.get("/metrics")
async def metrics():
    data, content_type = metrics_payload()
    return Response(content=data, media_type=content_type)

app.include_router(health.router)
