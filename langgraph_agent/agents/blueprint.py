import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import TypedDict
from ..utils.helpers import write
from ..utils.logging import setup_logger
from langsmith import traceable

logger = setup_logger(__name__)

TEMPLATES = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=select_autoescape(['xml','yml']))

class State(TypedDict, total=False):
    repo: str
    adr: str

@traceable(name="blueprint")
def run(state: State) -> State:
    logger.info("Blueprint:start", extra={"stage": "blueprint"})
    repo = state.get('repo') or os.path.abspath('generated-app-enterprise')
    state['repo'] = repo
    files = {
        'pom.xml': env.get_template('pom.xml.j2').render(),
        'src/main/resources/application.yml': env.get_template('application.yml.j2').render(),
        'src/main/resources/logback-spring.xml': env.get_template('logback-spring.xml.j2').render(),
        'src/main/java/com/example/demo/Application.java': env.get_template('Application.java.j2').render(),
        'README.md': env.get_template('README.md.j2').render(),
        'ADR.md': state.get('adr','')
    }
    for p, c in files.items():
        write(os.path.join(repo, p), c)
    logger.info("Blueprint:done", extra={"stage": "blueprint", "repo": repo})
    return state
