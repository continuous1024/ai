from doctest import debug
from agno.agent import Agent
from agno.memory.v2 import Memory
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.models.openrouter import OpenRouter
# from agno.models.openai import OpenAIChat
from agno.models.google import Gemini
from agno.playground import Playground, serve_playground_app
from agno.storage.sqlite import SqliteStorage
from agno.team.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.exa import ExaTools
from agno.tools.yfinance import YFinanceTools
from agno.tools.reasoning import ReasoningTools
from agno.tools.thinking import ThinkingTools
from textwrap import dedent
from agno.knowledge.url import UrlKnowledge
from agno.tools.knowledge import KnowledgeTools
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.embedder.ollama import OllamaEmbedder
from agno.models.openrouter import OpenRouter

agent_storage_file: str = "tmp/agents.db"
memory_storage_file: str = "tmp/memory.db"
image_agent_storage_file: str = "tmp/image_agent.db"

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

memory_db = SqliteMemoryDb(table_name="memory", db_file=memory_storage_file)

# No need to set the model, it gets set by the agent to the agent's model
memory = Memory(db=memory_db)

simple_agent = Agent(
    name="Simple Agent",
    role="Answer basic questions",
    agent_id="simple-agent",
    model=Gemini(id="gemini-2.0-flash-exp"),
    storage=SqliteStorage(
        table_name="simple_agent", db_file=agent_storage_file, auto_upgrade_schema=True
    ),
    memory=memory,
    enable_user_memories=True,
    add_history_to_messages=True,
    num_history_responses=5,
    add_datetime_to_instructions=True,
    markdown=True,
)

web_agent = Agent(
    name="Web Agent",
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[DuckDuckGoTools()],
    instructions=["Always include sources"],
    # Store the agent sessions in a sqlite database
    storage=SqliteStorage(table_name="web_agent", db_file=agent_storage_file),
    # Adds the current date and time to the instructions
    add_datetime_to_instructions=True,
    # Adds the history of the conversation to the messages
    add_history_to_messages=True,
    # Number of history responses to add to the messages
    num_history_responses=5,
    # Adds markdown formatting to the messages
    markdown=True,
)

finance_agent = Agent(
    name="Finance Agent",
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)],
    instructions=["Always use tables to display data"],
    storage=SqliteStorage(table_name="finance_agent", db_file=agent_storage_file),
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=True,
)

image_agent = Agent(
    name="Image Agent",
    agent_id="image_agent",
    model=Gemini(id="gemini-2.0-flash-exp"),
    description="You are an AI agent that can generate images.",
    instructions=[
        "Always describe what image was generated.",
    ],
    memory=memory,
    markdown=True,
    enable_user_memories=True,
    add_history_to_messages=True,
    add_datetime_to_instructions=True,
    storage=SqliteStorage(
        table_name="image_agent",
        db_file=image_agent_storage_file,
        auto_upgrade_schema=True,
    ),
)

cot_agent = Agent(
    name="Chain-of-Thought Agent",
    role="Answer basic questions",
    agent_id="cot-agent",
    model=Gemini(id="gemini-2.0-flash-exp"),
    storage=SqliteStorage(
        table_name="cot_agent", db_file=agent_storage_file, auto_upgrade_schema=True
    ),
    add_history_to_messages=True,
    num_history_responses=3,
    add_datetime_to_instructions=True,
    markdown=True,
    reasoning=True,
)

reasoning_tool_agent = Agent(
    name="Reasoning Tool Agent",
    role="Answer basic questions",
    agent_id="reasoning-tool-agent",
    model=Gemini(id="gemini-2.0-flash-exp"),
    storage=SqliteStorage(
        table_name="reasoning_tool_agent",
        db_file=agent_storage_file,
        auto_upgrade_schema=True,
    ),
    add_history_to_messages=True,
    num_history_responses=3,
    add_datetime_to_instructions=True,
    markdown=True,
    tools=[ReasoningTools()],
)

thinking_tool_agent = Agent(
    name="Thinking Tool Agent",
    agent_id="thinking_tool_agent",
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[ThinkingTools(add_instructions=True), YFinanceTools(enable_all=True)],
    instructions=dedent("""\
        You are a seasoned Wall Street analyst with deep expertise in market analysis! 📊

        Follow these steps for comprehensive financial analysis:
        1. Market Overview
           - Latest stock price
           - 52-week high and low
        2. Financial Deep Dive
           - Key metrics (P/E, Market Cap, EPS)
        3. Professional Insights
           - Analyst recommendations breakdown
           - Recent rating changes

        4. Market Context
           - Industry trends and positioning
           - Competitive analysis
           - Market sentiment indicators

        Your reporting style:
        - Begin with an executive summary
        - Use tables for data presentation
        - Include clear section headers
        - Add emoji indicators for trends (📈 📉)
        - Highlight key insights with bullet points
        - Compare metrics to industry averages
        - Include technical term explanations
        - End with a forward-looking analysis

        Risk Disclosure:
        - Always highlight potential risk factors
        - Note market uncertainties
        - Mention relevant regulatory concerns\
    """),
    add_datetime_to_instructions=True,
    show_tool_calls=True,
    markdown=True,
    stream_intermediate_steps=True,
    storage=SqliteStorage(
        table_name="thinking_tool_agent",
        db_file=agent_storage_file,
        auto_upgrade_schema=True,
    ),
)

knowledge_base = UrlKnowledge(
    urls=["https://docs.agno.com"],
    # Use LanceDB as the vector database and store embeddings in the `agno_docs` table
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="agno_docs",
        search_type=SearchType.hybrid,
        embedder=OllamaEmbedder(id="openhermes"),
    ),
)
knowledge_agent = Agent(
    agent_id="knowledge_agent",
    name="Knowledge Agent",
    model=OpenRouter(id="gpt-4o"),
    knowledge=knowledge_base,
    search_knowledge=True,
    read_chat_history=True,
    show_tool_calls=True,
    markdown=True,
    storage=SqliteStorage(
        table_name="knowledge_agent",
        db_file=agent_storage_file,
        auto_upgrade_schema=True,
    ),
    debug_mode=True,
)

reasoning_finance_team = Team(
    name="Reasoning Finance Team",
    mode="coordinate",
    model=Gemini(id="gemini-2.0-flash-exp"),
    members=[
        web_agent,
        finance_agent,
    ],
    tools=[ReasoningTools(add_instructions=True)],
    team_id="reasoning_finance_team",
    debug_mode=True,
    instructions=[
        "Only output the final answer, no other text.",
        "Use tables to display data",
    ],
    markdown=True,
    show_members_responses=True,
    enable_agentic_context=True,
    add_datetime_to_instructions=True,
    success_criteria="The team has successfully completed the task.",
    storage=SqliteStorage(
        table_name="reasoning_finance_team",
        db_file=agent_storage_file,
        auto_upgrade_schema=True,
    ),
)

research_agent = Agent(
    name="Research Agent",
    role="Research agent",
    model=Gemini(id="gemini-2.0-flash-exp"),
    instructions=["You are a research agent"],
    tools=[DuckDuckGoTools(), ExaTools()],
    agent_id="research_agent",
    memory=memory,
    enable_user_memories=True,
)

research_team = Team(
    name="Research Team",
    description="A team of agents that research the web",
    members=[research_agent, simple_agent],
    model=Gemini(id="gemini-2.0-flash-exp"),
    mode="coordinate",
    team_id="research_team",
    success_criteria=dedent("""\
        A comprehensive research report with clear sections and data-driven insights.
    """),
    instructions=[
        "You are the lead researcher of a research team! 🔍",
    ],
    memory=memory,
    enable_user_memories=True,
    add_datetime_to_instructions=True,
    show_tool_calls=True,
    markdown=True,
    enable_agentic_context=True,
    storage=SqliteStorage(
        table_name="research_team",
        db_file=agent_storage_file,
        auto_upgrade_schema=True,
        mode="team",
    ),
)


app = Playground(
    agents=[
      simple_agent,
      image_agent,
      web_agent,
      finance_agent,
      cot_agent,
      knowledge_agent,
      reasoning_tool_agent,
      thinking_tool_agent,
    ],
    teams=[reasoning_finance_team, research_team],
).get_app()

if __name__ == "__main__":
    serve_playground_app("playground:app", reload=True)
