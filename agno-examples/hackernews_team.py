from typing import List

from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.deepseek import DeepSeek
from agno.models.openrouter import OpenRouter
from agno.models.ollama import Ollama
from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.hackernews import HackerNewsTools
from agno.tools.newspaper4k import Newspaper4kTools
from pydantic import BaseModel

class Article(BaseModel):
    title: str
    summary: str
    reference_links: List[str]


hn_researcher = Agent(
    name="HackerNews Researcher",
    # model=Gemini(id="gemini-2.0-flash"),
    # model=Ollama(id="qwen3:4b"),
    model=OpenRouter(id="gpt-4o"),
    # model=DeepSeek(id="deepseek-chat"),
    # model=DeepSeek(id="deepseek-reasoner")
    instructions=[
        "以中文生成回复",
    ],
    role="Gets top stories from hackernews.",
    tools=[HackerNewsTools()],
)

web_searcher = Agent(
    name="Web Searcher",
    # model=Gemini(id="gemini-2.0-flash"),
    # model=Ollama(id="qwen3:4b"),
    model=OpenRouter(id="gpt-4o"),
    # model=DeepSeek(id="deepseek-chat"),
    # model=DeepSeek(id="deepseek-reasoner")
    instructions=[
        "以中文生成回复",
    ],
    role="Searches the web for information on a topic",
    tools=[DuckDuckGoTools()],
    add_datetime_to_instructions=True,
)

article_reader = Agent(
    name="Article Reader",
    role="Reads articles from URLs.",
    tools=[Newspaper4kTools()],
    # model=Gemini(id="gemini-2.0-flash"),
    # model=Ollama(id="qwen3:4b"),
    model=OpenRouter(id="gpt-4o"),
    # model=DeepSeek(id="deepseek-chat"),
    # model=DeepSeek(id="deepseek-reasoner")
    instructions=[
        "以中文生成回复",
    ],
)

hackernews_team = Team(
    name="HackerNews Team",
    mode="coordinate",
    # model=Gemini(id="gemini-2.0-flash"),
    # model=Ollama(id="qwen3:4b"),
    model=OpenRouter(id="gpt-4o"),
    # model=DeepSeek(id="deepseek-chat"),
    # model=DeepSeek(id="deepseek-reasoner")
    members=[hn_researcher, web_searcher, article_reader],
    instructions=[
        "First, search hackernews for what the user is asking about.",
        "Then, ask the article reader to read the links for the stories to get more information.",
        "Important: you must provide the article reader with the links to read.",
        "Then, ask the web searcher to search for each story to get more information.",
        "Finally, provide a thoughtful and engaging summary.",
        "以中文生成回复",
    ],
    response_model=Article,
    show_tool_calls=True,
    markdown=True,
    debug_mode=True,
    show_members_responses=True,
)

# Run the team
report = hackernews_team.run(
    "What are the top stories on hackernews?"
).content

print(f"Title: {report.title}")
print(f"Summary: {report.summary}")
print(f"Reference Links: {report.reference_links}")