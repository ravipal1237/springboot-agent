from typing import TypedDict
from ..utils.helpers import run, tail, apply_fenced_drops
from ..utils.llm import chat

class State(TypedDict, total=False):
    repo: str
    build_log: str
    test_log: str

def _attempt(repo: str):
    return run(['mvn','-q','-DskipTests=false','test'], cwd=repo)

def run(state: State) -> State:
    repo = state['repo']
    # First attempt
    code, out, err = _attempt(repo)
    state['build_log'] = out + '\n' + err
    if code == 0:
        state['test_log'] = state['build_log']
        return state

    # Repair #1
    fix1 = chat(f"Build/tests failed. Logs (tail):\n{tail(state['build_log'])}\nReturn ONLY corrected files as fenced blocks with path= headers.", tokens=3000)
    apply_fenced_drops(fix1, repo)
    code2, out2, err2 = _attempt(repo)
    if code2 == 0:
        state['test_log'] = out2 + '\n' + err2
        return state

    # Repair #2
    fix2 = chat(f"Second attempt. Still failing. Latest logs (tail):\n{tail(out2+err2)}\nReturn ONLY corrected files as fenced blocks with path= headers.", tokens=3000)
    apply_fenced_drops(fix2, repo)
    code3, out3, err3 = _attempt(repo)
    state['test_log'] = out3 + '\n' + err3
    return state
