from typing import TypedDict
from ..utils.llm import chat
from ..utils.logging import setup_logger
from langsmith import traceable

logger = setup_logger(__name__)

class State(TypedDict, total=False):
    spec: str
    adr: str

@traceable(name="architect")
def run(state: State) -> State:
    logger.info("Architect:start", extra={"stage": "architect"})
    prompt = f"""Write an ADR for architecture decisions (layers, mapping, validation, persistence, RFC7807, observability, security, resilience, testing).

SPEC:
{state['spec']}
"""
    state['adr'] = chat(prompt, tokens=1200)
    logger.info("Architect:done", extra={"stage": "architect"})
    return state
