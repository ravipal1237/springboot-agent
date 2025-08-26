from typing import TypedDict

class State(TypedDict, total=False):
    test_log: str
    verdict: str

def run(state: State) -> State:
    log = state.get('test_log','')
    failed = ('BUILD FAILURE' in log) or ('[ERROR]' in log and 'BUILD SUCCESS' not in log)
    state['verdict'] = 'FAIL' if failed else 'PASS'
    return state
