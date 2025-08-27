from typing import TypedDict
from ..utils.llm import chat
from ..utils.helpers import apply_fenced_drops
from ..utils.logging import setup_logger
from langsmith import traceable

logger = setup_logger(__name__)

class State(TypedDict, total=False):
    spec: str
    repo: str

PROMPT = """Using the SPEC below, generate Spring Boot code under package `com.example.demo` with layers api/app/domain/infra.
REQUIREMENTS:
- Entities (JPA, H2 compatible) + repositories
- Services (@Transactional, Resilience4j: @Retry, @CircuitBreaker, timeouts)
- Controllers (REST) with DTOs, validation (@Valid), pagination, sorting
- DTO mapping via MapStruct
- Security: honor API-key security (no sensitive data in logs)
- Observability: SLF4J loggers; log start/end & key decisions; use Micrometer MeterRegistry (counters/timers)
- Tracing: use MDC correlationId
- Tests: unit tests (services) + MockMvc (controllers), happy + negative
IMPORTANT OUTPUT FORMAT: fenced code blocks with headers like
```java path=src/main/java/com/example/demo/domain/Customer.java
// code
```
SPEC:
{spec}
"""

@traceable(name="codegen")
def run(state: State) -> State:
    logger.info("Codegen:start", extra={"stage": "codegen"})
    out = chat(PROMPT.format(spec=state['spec']), tokens=3800)
    apply_fenced_drops(out, state['repo'])
    logger.info("Codegen:done", extra={"stage": "codegen"})
    return state
