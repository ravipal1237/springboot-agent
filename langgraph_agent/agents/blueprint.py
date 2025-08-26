import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import TypedDict
from ..utils.helpers import write

TEMPLATES = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=select_autoescape(['xml','yml']))

class State(TypedDict, total=False):
    repo: str
    adr: str

def run(state: State) -> State:
    repo = state.get('repo') or os.path.abspath('generated-app-enterprise')
    state['repo'] = repo
    files = {
        'pom.xml': env.get_template('pom.xml.j2').render(),
        'src/main/resources/application.yml': env.get_template('application.yml.j2').render(),
        'src/main/java/com/example/demo/Application.java': env.get_template('Application.java.j2').render(),
        'src/main/java/com/example/demo/api/GlobalExceptionHandler.java': env.get_template('GlobalExceptionHandler.java.j2').render(),
        'src/main/java/com/example/demo/infra/config/OpenApiConfig.java': env.get_template('OpenApiConfig.java.j2').render(),
        'src/test/java/com/example/demo/SmokeTest.java': env.get_template('SmokeTest.java.j2').render(),
        'README.md': env.get_template('README.md.j2').render(),
        'ADR.md': state.get('adr', '# ADR\n')
    }
    for p, c in files.items():
        write(os.path.join(repo, p), c)
    return state
