from typing import TypedDict
from ..utils.logging import setup_logger
from langsmith import traceable

logger = setup_logger(__name__)

class State(TypedDict, total=False):
    test_log: str
    verdict: str

@traceable(name="qa")
def run(state: State) -> State:
    log = state.get('test_log','')
    failed = ('BUILD FAILURE' in log) or ('[ERROR]' in log and 'BUILD SUCCESS' not in log)
    state['verdict'] = 'FAIL' if failed else 'PASS'
    logger.info("QA:verdict", extra={"stage": "qa", "verdict": state['verdict']})
    return state
