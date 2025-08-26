from typing import TypedDict
from ..utils.llm import chat

class State(TypedDict, total=False):
    requirements: str
    spec: str

def run(state: State) -> State:
    req = state.get('requirements', '')
    prompt = f"""Analyze the following requirement and produce a concise SPEC.

Requirement:
{req}

Return EXACTLY this markdown structure (no code):
# Domain Model
- Entities (name, fields, types, constraints)
- Relationships

# API Endpoints
- Path, method, request DTO, response DTO, status codes, pagination & sorting

# Validation Rules
- DTO-level annotations

# Non-Functional
- Logging, errors (RFC7807), testing outline

# Assumptions & Open Questions
"""
    state['spec'] = chat(prompt, tokens=1200)
    return state
