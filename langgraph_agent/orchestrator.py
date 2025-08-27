import os, sys
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from .agents import analyzer, architect, blueprint, codegen, security, validator, qa_gate
from .utils.logging import setup_logger
from langsmith import Client

# Optional: force project name in case env var is missing
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "springboot-agent")

# Initialize LangSmith client
client = Client()
print(f"🔗 LangSmith tracing enabled. Project: {os.environ['LANGCHAIN_PROJECT']}")

logger = setup_logger("orchestrator")

class S(TypedDict, total=False):
    requirements: str
    spec: str
    adr: str
    repo: str
    build_log: str
    test_log: str
    verdict: str

graph = StateGraph(S)
graph.add_node('analyzer', analyzer.run)
graph.add_node('architect', architect.run)
graph.add_node('blueprint', blueprint.run)
graph.add_node('codegen', codegen.run)
graph.add_node('security', security.run)
graph.add_node('validator', validator.run)
graph.add_node('qa', qa_gate.run)

graph.add_edge(START, 'analyzer')
graph.add_edge('analyzer', 'architect')
graph.add_edge('architect', 'blueprint')
graph.add_edge('blueprint', 'codegen')
graph.add_edge('codegen', 'security')
graph.add_edge('security', 'validator')
graph.add_edge('validator', 'qa')
graph.add_edge('qa', END)

app = graph.compile()

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m langgraph_agent.orchestrator '<requirements>'")
        sys.exit(1)
    req = sys.argv[1]
    state: S = {'requirements': req, 'repo': os.path.abspath('generated-app-enterprise')}

    logger.info("graph:start", extra={"repo": state['repo']})
    for ev in app.stream(state):
        # ev contains node deltas; log compactly
        logger.info("graph:event", extra={k: True for k in ev.keys()})
        print(ev)

    final = app.invoke(state)
    if final.get('adr'):
        os.makedirs(final['repo'], exist_ok=True)
        with open(os.path.join(final['repo'], 'ADR.md'), 'w', encoding='utf-8') as f:
            f.write(final['adr'])
    logger.info("graph:done", extra={"verdict": final.get('verdict'), "repo": final.get('repo')})
    print('\n===== QA VERDICT =====\n', final.get('verdict'))
    print('\nRepo:', final.get('repo'))

if __name__ == '__main__':
    main()
