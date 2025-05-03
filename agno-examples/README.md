# ago

uv venv --python 3.12
source .venv/bin/activate

uv pip install -U "agno[aws]" agno openai google-genai yfinance pylance lancedb tantivy ollama openai duckduckgo-search yfinance sqlalchemy 'fastapi[standard]' newspaper4k lxml_html_clean exa_py httpx
export GOOGLE_API_KEY=xxx

uv run python playground.py
