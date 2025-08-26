from typing import TypedDict
from ..utils.llm import chat

class State(TypedDict, total=False):
    spec: str
    adr: str

def run(state: State) -> State:
    prompt = f"""Based on the SPEC below, write an ADR-style summary with decisions on:
- Layering (api/app/domain/infra)
- DTO mapping strategy
- Transaction boundaries
- Pagination/sorting approach
- Validation (bean validation)
- Error handling (RFC7807)
- Test strategy (unit + MockMvc)
- Data profile: H2 for dev/test

SPEC:
{state['spec']}

Return markdown (no code).
"""
    state['adr'] = chat(prompt, tokens=1000)
    return state
