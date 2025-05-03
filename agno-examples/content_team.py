from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.deepseek import DeepSeek
from agno.models.openrouter import OpenRouter
from agno.models.ollama import Ollama
from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools

# Create individual specialized agents
researcher = Agent(
    name="Researcher",
    role="Expert at finding information",
    tools=[DuckDuckGoTools()],
    # model=Gemini(id="gemini-2.0-flash"),
    # model=Ollama(id="qwen3:4b"),
    model=OpenRouter(id="gpt-4o"),
    # model=DeepSeek(id="deepseek-chat"),
    # model=DeepSeek(id="deepseek-reasoner")
    instructions=[
        "以中文生成回复",
    ],
)

writer = Agent(
    name="Writer",
    role="Expert at writing clear, engaging content",
    # model=Gemini(id="gemini-2.0-flash"),
    # model=Ollama(id="qwen3:4b"),
    model=OpenRouter(id="gpt-4o"),
    # model=DeepSeek(id="deepseek-chat"),
    # model=DeepSeek(id="deepseek-reasoner")
    instructions=[
        "以中文生成回复",
    ],
)

# Create a team with these agents
content_team = Team(
    name="Content Team",
    mode="coordinate",
    members=[researcher, writer],
    instructions=[
        "You are a team of researchers and writers that work together to create high-quality content.",
        "以中文生成回复",
    ],
    # model=Gemini(id="gemini-2.0-flash"),
    # model=Ollama(id="qwen3:4b"),
    model=OpenRouter(id="gpt-4o"),
    # model=DeepSeek(id="deepseek-chat"),
    # model=DeepSeek(id="deepseek-reasoner")
    markdown=True,
)

# Run the team with a task
content_team.print_response("Create a short article about quantum computing")