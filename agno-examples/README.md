# ago

uv venv --python 3.12
source .venv/bin/activate

uv pip install -U "agno[aws]" agno openai google-genai yfinance pylance lancedb tantivy ollama
uv pip install -U openai duckduckgo-search yfinance sqlalchemy 'fastapi[standard]' agno exa_py
export GOOGLE_API_KEY=xxx

uv run python playground.py
