from typing import TypedDict
import subprocess
from ..utils.helpers import tail, apply_fenced_drops, ts
from ..utils.logging import setup_logger
from ..utils.llm import chat
from langsmith import traceable

logger = setup_logger(__name__)

class State(TypedDict, total=False):
    repo: str
    build_log: str
    test_log: str


def _attempt(repo: str):
    # Run spotless:apply
    proc1 = subprocess.run(
        ['mvn', '-q', '-DskipTests=true', 'spotless:apply'],
        cwd=repo,
        capture_output=True,
        text=True
    )

    # Run full verify
    proc2 = subprocess.run(
        ['mvn', '-q', '-DskipTests=false', 'verify'],
        cwd=repo,
        capture_output=True,
        text=True
    )

    return proc2.returncode, proc2.stdout, proc2.stderr


@traceable(name="validator")
def run(state: State) -> State:
    logger.info("Validator:start", extra={"stage": "validator"})
    repo = state['repo']
    code, out, err = _attempt(repo)
    state['build_log'] = (out or '') + '\n' + (err or '')

    if code == 0:
        state['test_log'] = state['build_log']
        logger.info("Validator:success", extra={"stage": "validator"})
        return state

    # Repair #1
    fix1 = chat(
        f"[{ts()}] Build/tests failed. Logs (tail):\n{tail(state['build_log'])}\n"
        f"Return ONLY corrected files as fenced blocks with path= headers.",
        tokens=3400
    )
    apply_fenced_drops(fix1, repo)
    code2, out2, err2 = _attempt(repo)
    if code2 == 0:
        state['test_log'] = (out2 or '') + '\n' + (err2 or '')
        logger.info("Validator:repaired", extra={"stage": "validator", "attempt": 1})
        return state

    # Repair #2
    fix2 = chat(
        f"[{ts()}] Second attempt. Still failing. Latest logs (tail):\n{tail(out2+err2)}\n"
        f"Return ONLY corrected files as fenced blocks with path= headers.",
        tokens=3400
    )
    apply_fenced_drops(fix2, repo)
    code3, out3, err3 = _attempt(repo)
    state['test_log'] = (out3 or '') + '\n' + (err3 or '')
    logger.info("Validator:done", extra={"stage": "validator", "attempt": 2, "exit_code": code3})
    return state
