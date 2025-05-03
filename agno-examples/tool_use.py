from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.deepseek import DeepSeek
from agno.models.openrouter import OpenRouter
from agno.models.ollama import Ollama
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    # model=Gemini(id="gemini-2.0-flash"),
    # model=Ollama(id="qwen3:4b"),
    model=OpenRouter(id="gpt-4o"),
    # model=DeepSeek(id="deepseek-chat"),
    # model=DeepSeek(id="deepseek-reasoner")
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
    debug_mode=True
)
agent.print_response("Whats happening in France? 以中文返回结果", stream=True)