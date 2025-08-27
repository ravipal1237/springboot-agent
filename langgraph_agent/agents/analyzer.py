from typing import TypedDict
from ..utils.llm import chat
from ..utils.logging import setup_logger
from langsmith import traceable

logger = setup_logger(__name__)

class State(TypedDict, total=False):
    requirements: str
    spec: str

@traceable(name="analyzer")
def run(state: State) -> State:
    logger.info("Analyzer:start", extra={"stage": "analyzer"})
    req = state.get('requirements', '')
    prompt = f"""Analyze requirements and produce a SPEC with:
# Domain Model
# API Endpoints
# Validation Rules
# Business Logic
# Non-Functional (logging/metrics/tracing/security/resilience/errors)
# Assumptions & Open Questions

Requirements:
{req}
"""
    state['spec'] = chat(prompt, tokens=1500)
    logger.info("Analyzer:done", extra={"stage": "analyzer"})
    return state
