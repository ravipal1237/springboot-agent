import os

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
BASE_URL = os.getenv("OPENAI_BASE_URL", None)
API_KEY = os.getenv("OPENAI_API_KEY", None)

# Which provider to use: "groq" | "ollama" | "openai"
PROVIDER = os.getenv("LLM_PROVIDER", "openai")

client = None

if PROVIDER == "groq":
    # Groq client (fast inference for LLaMA models)
    from groq import Groq
    if not API_KEY:
        raise ValueError("Missing GROQ API key. Set OPENAI_API_KEY.")
    client = Groq(api_key=API_KEY)

elif PROVIDER == "ollama":
    # Local Ollama runs OpenAI-compatible API at localhost:11434
    from openai import OpenAI
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

else:
    # Default: OpenAI / Azure / any OpenAI-compatible API
    from openai import OpenAI
    if BASE_URL:
        client = OpenAI(base_url=BASE_URL, api_key=API_KEY or "not-needed")
    else:
        client = OpenAI(api_key=API_KEY)

SYSTEM = (
    "You are a principal Java/Spring engineer. Generate robust Spring Boot 3 (Java 17) code with H2 dev/test, "
    "JPA, Validation, OpenAPI UI, RFC7807 errors, layered architecture (api/app/domain/infra). "
    "Instrument code with SLF4J logging (JSON via Logback), Micrometer metrics, and Micrometer Tracing MDC. "
    "Use MapStruct for DTO mapping, Resilience4j for service resiliency. "
    "ALWAYS return files as fenced blocks with explicit path= headers (no commentary in code blocks)."
)


def chat(user: str, temp: float = 0.2, tokens: int = 2500) -> str:
    """Run chat completion against Groq, Ollama, or OpenAI-compatible API."""
    if PROVIDER == "groq":
        # Groq client has a slightly different API structure
        r = client.chat.completions.create(
            model=MODEL,  # e.g., "llama3-70b-8192"
            temperature=temp,
            max_tokens=tokens,
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": user},
            ],
        )
          # Handle both OpenAI and Groq response object styles
        if hasattr(r.choices[0].message, "content"):
            return r.choices[0].message.content or ""
        elif isinstance(r.choices[0].message, dict):
            return r.choices[0].message.get("content", "")
        else:
            raise ValueError(f"Unexpected response format: {r}")

    else:
        # Works for OpenAI and Ollama (both OpenAI-compatible)
        r = client.chat.completions.create(
            model=MODEL,
            temperature=temp,
            max_tokens=tokens,
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": user},
            ],
        )
          # Handle both OpenAI and Groq response object styles
        if hasattr(r.choices[0].message, "content"):
            return r.choices[0].message.content or ""
        elif isinstance(r.choices[0].message, dict):
            return r.choices[0].message.get("content", "")
        else:
            raise ValueError(f"Unexpected response format: {r}")
