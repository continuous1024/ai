from agno.agent import Agent
from agno.embedder.google import GeminiEmbedder
from agno.knowledge.url import UrlKnowledge
from agno.models.google import Gemini
from agno.models.deepseek import DeepSeek
from agno.models.openrouter import OpenRouter
from agno.models.ollama import Ollama
from agno.tools.reasoning import ReasoningTools
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.embedder.ollama import OllamaEmbedder

# Load Agno documentation in a knowledge base
knowledge = UrlKnowledge(
    urls=["https://docs.agno.com/introduction/agents.md"],
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="agno_docs",
        search_type=SearchType.hybrid,
        embedder=OllamaEmbedder(id="bge-m3", dimensions=1024),
    ),
)

agent = Agent(
    name="Agno Assist",
    # model=Gemini(id="gemini-2.0-flash-exp"),
    # model=Ollama(id="qwen3:4b"),
    # model=OpenRouter(id="gpt-4o"),
    model=DeepSeek(id="deepseek-chat"),
    # reasoning_model=DeepSeek(id="deepseek-reasoner"),
    reasoning=True,
    instructions=[
        "Use tables to display data.",
        "Include sources in your response.",
        "Search your knowledge before answering the question.",
        "Only include the output in your response. No other text.",
    ],
    knowledge=knowledge,
    tools=[ReasoningTools(add_instructions=True)],
    add_datetime_to_instructions=True,
    show_tool_calls=True,
    show_full_reasoning=True,
    markdown=True,
    debug_mode=True
)

if __name__ == "__main__":
    # Load the knowledge base, comment out after first run
    # Set recreate to True to recreate the knowledge base if needed
    agent.knowledge.load(recreate=False)
    agent.print_response(
        "What are Agents?",
        stream=True,
        show_full_reasoning=True,
        stream_intermediate_steps=True,
    )
