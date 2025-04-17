# from agno.agent import Agent, RunResponse
# from agno.models.deepseek import DeepSeek

# agent = Agent(model=DeepSeek(), markdown=True)

# # Print the response in the terminal
# agent.print_response("Share a 2 sentence horror story.")
from agno.agent import Agent, RunResponse  # noqa
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools

agent = Agent(
  model=Gemini(id="gemini-2.0-flash-exp"),
  tools=[YFinanceTools(stock_price=True)],
  instructions=[
      "Use tables to display data.",
      "Only include the table in your response. No other text.",
  ],
  markdown=True
)

# Get the response in a variable
# run: RunResponse = agent.run("Share a 2 sentence horror story")
# print(run.content)

# Print the response in the terminal
# agent.print_response("Share a 2 sentence happy story", stream=True)
agent.print_response("What is the stock price of Apple?", stream=True)
