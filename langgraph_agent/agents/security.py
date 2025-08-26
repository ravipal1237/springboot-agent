from typing import TypedDict
import os
from ..utils.llm import chat
from ..utils.helpers import apply_fenced_drops

GLOB_EXT = ('.java', '.yml', '.xml', '.properties')

def _snapshot(repo: str, max_chars: int = 24000) -> str:
    buf, total = [], 0
    for root, _, files in os.walk(repo):
        for f in files:
            if f.endswith(GLOB_EXT):
                path = os.path.join(root, f)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
                        content = fh.read(4000)
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

PROMPT = """You are a senior AppSec engineer. Review the Spring Boot project for **OWASP Top 10** issues:
- Injection, XXE, SSRF, insecure deserialization
- Open CORS / CSRF issues
- Sensitive data exposure (DTOs, logs)
- Input validation, pagination/sorting abuse
- Error handling consistency (RFC7807)

Given the partial code snapshot, return ONLY concrete patches as fenced blocks with `path=` headers (no prose inside code fences). If `pom.xml` needs changes, return the full file.
Snapshot:
{snapshot}
"""

def run(state: State) -> State:
    repo = state['repo']
    snap = _snapshot(repo)
    out = chat(PROMPT.format(snapshot=snap), tokens=3200)
    apply_fenced_drops(out, repo)
    state['security_report'] = 'Security recommendations applied where provided.'
    return state
