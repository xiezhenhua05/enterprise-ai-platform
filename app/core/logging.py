import json, logging, sys
from contextvars import ContextVar

trace_id_var: ContextVar[str] = ContextVar("trace_id", default="-")

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
        "ts": self.formatTime(record),
        "level": record.levelname,
        "logger": record.name,
        "msg": record.getMessage(),
        "trace_id": trace_id_var.get(),
        }
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload)

def setup_logging(level: str = "INFO") -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level)
