from agno.agent import Agent, RunResponse  # noqa
from agno.models.google import Gemini
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools

agent = Agent(
  model=Gemini(id="gemini-2.0-flash-exp"),
  tools=[
    ReasoningTools(add_instructions=True),
    YFinanceTools(
        stock_price=True,
        analyst_recommendations=True,
        company_info=True,
        company_news=True,
    ),
  ],
  instructions=[
        "Use tables to display data.",
        "Include sources in your response.",
        "Only include the report in your response. No other text.",
  ],
  markdown=True
)

agent.print_response(
    "写一个 NVDA 的报告，思考过程和结果都要输出中文",
    stream=True,
    show_full_reasoning=True,
    stream_intermediate_steps=True,
)
