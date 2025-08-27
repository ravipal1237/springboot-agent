# Exposes the compiled graph to LangGraph Studio.
from .orchestrator import app

# LangGraph Studio expects a top-level variable 'graph' or 'app' exporting the compiled graph.
# Start with:  langgraph dev langgraph_agent/studio_app.py --port 8123
