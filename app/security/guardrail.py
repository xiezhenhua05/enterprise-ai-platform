import re

INJECTION_PATTERNS = [
    r"ignore (all )?(previous|above) instructions",
    r"disregard .*(rules|instructions|context)",
    r"you are now .*(dan|jailbroken|unrestricted)",
    r"reveal .*(system prompt|instructions)",
    r"print .*(api[_ ]?key|password|secret|token)",
]

def check_prompt_injection(text: str) -> bool:
    low = text.lower()
    return any(re.search(p, low) for p in INJECTION_PATTERNS)