from typing import TypedDict
import os
from ..utils.llm import chat
from ..utils.helpers import apply_fenced_drops
from ..utils.logging import setup_logger
from langsmith import traceable

logger = setup_logger(__name__)
GLOB_EXT = ('.java', '.yml', '.xml', '.properties')

def _snapshot(repo: str, max_chars: int = 32000) -> str:
    buf, total = [], 0
    for root, _, files in os.walk(repo):
        for f in files:
            if f.endswith(GLOB_EXT):
                path = os.path.join(root, f)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
                        content = fh.read(5000)
                    entry = f"\n--- FILE: {os.path.relpath(path, repo)} ---\n" + content
                    if total + len(entry) > max_chars:
                        return ''.join(buf)
                    buf.append(entry); total += len(entry)
                except Exception:
                    continue
    return ''.join(buf)

class State(TypedDict, total=False):
    repo: str
    security_report: str

PROMPT = """Act as an AppSec engineer. Review the project for OWASP Top 10 risks and production readiness.
Patch by returning ONLY fenced code blocks with path= headers (no prose).

Project snapshot:
{snapshot}
"""

@traceable(name="security")
def run(state: State) -> State:
    logger.info("Security:start", extra={"stage": "security"})
    repo = state['repo']
    out = chat(PROMPT.format(snapshot=_snapshot(repo)), tokens=3300)
    apply_fenced_drops(out, repo)
    state['security_report'] = 'Security patches applied (if provided).'
    logger.info("Security:done", extra={"stage": "security"})
    return state
