from typing import TypedDict
from ..utils.llm import chat
from ..utils.helpers import apply_fenced_drops

class State(TypedDict, total=False):
    spec: str
    repo: str

PROMPT = """Using the SPEC below, generate Spring Boot code under package `com.example.demo` with layers api/app/domain/infra.
Include:
- Entities (JPA, H2 compatible) and repositories
- Services (@Transactional where needed) with business logic
- Controllers (REST) with DTOs, validation, pagination
- Unit tests for services and MockMvc tests for controllers

IMPORTANT OUTPUT FORMAT
Return multiple files as fenced code blocks with explicit path= headers, for example:
```java path=src/main/java/com/example/demo/domain/Customer.java
// code
```
No explanations inside the code fences.
SPEC:
{spec}
"""

def run(state: State) -> State:
    out = chat(PROMPT.format(spec=state['spec']), tokens=3500)
    apply_fenced_drops(out, state['repo'])
    return state
