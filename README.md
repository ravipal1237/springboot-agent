# Enterprise Spring Boot Codegen Agent (Pro)
LangGraph-based **multi-agent** pipeline that dynamically generates, secures, tests, and validates Spring Boot code using an OpenAI-compatible LLM endpoint (e.g., vLLM, Ollama, llama.cpp proxy).

## Features
- Agents: **Analyzer → Architect → Blueprint → Codegen → Security → Validator (2 repair loops) → QA**
- LLM-driven code generation (entities, repos, services, controllers, DTOs, unit & MockMvc tests)
- Enterprise templates: Spring Boot 3/Java 17, H2 (dev/test), RFC7807 errors, OpenAPI UI, Spotless, SpotBugs, JaCoCo, OWASP Dependency-Check
- Stateless compile (no LangGraph checkpointer requirement)

## Prereqs
- Python 3.12+
- Java 17+, Maven 3.9+
- Local OpenAI-compatible LLM endpoint serving **CodeLlama-7B Instruct** (or better)

## Setup
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

export OPENAI_BASE_URL=http://localhost:11434/v1
export OPENAI_API_KEY=not-needed
export OPENAI_MODEL=codellama:7b-Instruct
```

## Run
```bash
python -m langgraph_agent.orchestrator "Build Customer & Order service with CRUD, pagination, validation, DTOs, RFC7807 errors, and unit + MockMvc tests"
```

Generated app appears at `generated-app-enterprise/`. Run it with:
```bash
cd generated-app-enterprise
mvn spring-boot:run
```
Swagger UI → http://localhost:8080/swagger-ui/index.html  
H2 Console → http://localhost:8080/h2-console  (JDBC: jdbc:h2:mem:demo, user: sa)

> Tip: The first run might trigger the two-step repair loop if the LLM output needs tweaks. Adjust JaCoCo thresholds in `pom.xml` if your model initially falls short.
