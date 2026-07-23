import time
from abc import ABC, abstractmethod
from functools import lru_cache
from openai import OpenAI
from app.core.config import get_settings
from app.observability.metrics import LLM_LATENCY, LLM_TOKENS

class BaseLLM(ABC):
    @abstractmethod
    def chat(self, messages: list[dict], **kw) -> dict:
        ...

class OpenAICompatLLM(BaseLLM):
    """Unified OpenAI-compatible interface for OpenAI, vLLM, and Qwen."""
    def __init__(self):
        s = get_settings()
        self.client = OpenAI(
            api_key=s.llm_api_key or "EMPTY",
            base_url=s.llm_base_url or None,
            timeout=30.0,      # Production: Request timeout protection
            max_retries=2,     # Production: Automatic retries
        )
        self.model = s.llm_model

    def chat(self, messages, temperature: float = 0.2, max_tokens: int = 1024) -> dict:
        start = time.time()
        resp = self.client.chat.completions.create(
            model=self.model, messages=messages,
            temperature=temperature, max_tokens=max_tokens,
        )
        LLM_LATENCY.observe(time.time() - start)
        usage = resp.usage
        LLM_TOKENS.labels("prompt").inc(usage.prompt_tokens)
        LLM_TOKENS.labels("completion").inc(usage.completion_tokens)
        return {"content": resp.choices[0].message.content,
                "usage": usage.model_dump()}

@lru_cache
def get_llm() -> BaseLLM:
    return OpenAICompatLLM()