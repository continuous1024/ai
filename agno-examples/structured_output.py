from typing import List

from agno.agent import Agent, RunResponse  # noqa
from agno.models.deepseek import DeepSeek
from agno.models.openrouter import OpenRouter
from agno.models.ollama import Ollama
from agno.models.google import Gemini
from pydantic import BaseModel, Field
from rich.pretty import pprint  # noqa


class MovieScript(BaseModel):
    setting: str = Field(
        ..., description="Provide a nice setting for a blockbuster movie."
    )
    ending: str = Field(
        ...,
        description="Ending of the movie. If not available, provide a happy ending.",
    )
    genre: str = Field(
        ...,
        description="Genre of the movie. If not available, select action, thriller or romantic comedy.",
    )
    name: str = Field(..., description="Give a name to this movie")
    characters: List[str] = Field(..., description="Name of characters for this movie.")
    storyline: str = Field(
        ..., description="3 sentence storyline for the movie. Make it exciting!"
    )


movie_agent = Agent(
    # model=Gemini(id="gemini-2.0-flash"),
    # model=Ollama(id="qwen3:4b"),
    model=OpenRouter(id="gpt-4o"),
    # model=DeepSeek(id="deepseek-chat"),
    # model=DeepSeek(id="deepseek-reasoner")
    instructions=[
        "以中文生成回复",
    ],
    description="You help people write movie scripts.",
    response_model=MovieScript,
    debug_mode=True,
)

movie_agent.print_response("中国北京")