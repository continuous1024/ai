from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.deepseek import DeepSeek
from agno.models.openrouter import OpenRouter
from agno.models.ollama import Ollama
from agno.models.google import Gemini
from agno.storage.sqlite import SqliteStorage
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    # model=Gemini(id="gemini-2.0-flash"),
    # model=Ollama(id="qwen3:4b"),
    model=OpenRouter(id="gpt-4o"),
    # model=DeepSeek(id="deepseek-chat"),
    # model=DeepSeek(id="deepseek-reasoner")
    storage=SqliteStorage(
        table_name="agent_sessions", db_file="tmp/data.db", auto_upgrade_schema=True
    ),
    tools=[DuckDuckGoTools()],
    instructions=[
        "以中文生成回复",
    ],
    add_history_to_messages=True,
    add_datetime_to_instructions=True,
)
agent.print_response("How many people live in Canada?")
agent.print_response("What is their national anthem?")
agent.print_response("List my messages one by one")