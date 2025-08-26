import os
from openai import OpenAI

MODEL = os.getenv('OPENAI_MODEL', 'codellama/CodeLlama-7b-Instruct')
BASE_URL = os.getenv('OPENAI_BASE_URL', 'http://localhost:8000/v1')
API_KEY  = os.getenv('OPENAI_API_KEY', 'not-needed')

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

SYSTEM = (
    'You are a principal Java/Spring engineer. Generate robust Spring Boot 3 (Java 17) code with H2 dev/test, '
    'JPA, Validation, OpenAPI UI, RFC7807 errors, layered architecture (api/app/domain/infra). '
    'ALWAYS return files as fenced blocks with explicit path= headers (no commentary in code blocks).'
)

def chat(user: str, temp: float = 0.2, tokens: int = 2500) -> str:
    r = client.chat.completions.create(
        model=MODEL,
        temperature=temp,
        max_tokens=tokens,
        messages=[{'role':'system','content':SYSTEM},{'role':'user','content':user}]
    )
    return r.choices[0].message.content or ''
