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
export OPENAI_MODEL=codellama:7b-instruct
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


-------------------


# Enterprise Spring Boot Codegen Agent (Ultra+)
LangGraph-based multi-agent pipeline with **LangSmith tracing**, **JSON logging**, **LangGraph Studio** UI, and production-grade Spring Boot scaffolding.

## 🔐 Env Vars
- **LLM** (choose one)
  - OpenAI: `OPENAI_API_KEY`, `OPENAI_MODEL=gpt-4o-mini`
  - Ollama: `OPENAI_BASE_URL=http://localhost:11434/v1`, `OPENAI_MODEL=codellama:7b-instruct`, `OPENAI_API_KEY=not-needed`
- **LangSmith**
  - `LANGCHAIN_TRACING_V2=true`
  - `LANGCHAIN_API_KEY=...`
  - `LANGSMITH_PROJECT=enterprise-agent`
- **Tracing export (Spring)**
  - `OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318`
- **API security (Spring)**
  - `API_KEY=your-dev-key`

## 🛠 Setup
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## ▶ Run the Agent (with streaming + JSON logs)
```bash
export LANGCHAIN_TRACING_V2=true
export LANGSMITH_PROJECT=enterprise-agent
export LANGCHAIN_API_KEY=YOUR_LANGSMITH_KEY

# LLM config here ...

python -m langgraph_agent.orchestrator "Build Customer & Order service with CRUD, pagination, validation, DTOs, RFC7807 errors, and unit + MockMvc tests"
```

## 🌐 Run with LangGraph Studio (Web UI)
```bash
# Start Studio against this app
langgraph dev langgraph_agent/studio_app.py --port 8123
# Open http://localhost:8123
```

## 🚀 Generated Spring Boot App
Once the run completes:
```bash
cd generated-app-enterprise
mvn -q -DskipTests=true spotless:apply
mvn spring-boot:run
```
- Swagger UI → http://localhost:8080/swagger-ui/index.html
- Prometheus metrics → http://localhost:8080/actuator/prometheus
- Health → http://localhost:8080/actuator/health
- H2 Console → http://localhost:8080/h2-console (jdbc:h2:mem:demo, user=sa)


-------------

export LLM_PROVIDER=groq
export OPENAI_API_KEY=your_groq_api_key
export OPENAI_MODEL=llama3-70b-8192
