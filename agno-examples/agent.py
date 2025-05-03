from agno.agent import Agent, RunResponse  # noqa
from agno.models.google import Gemini
from agno.models.deepseek import DeepSeek
from agno.models.openrouter import OpenRouter
from agno.models.ollama import Ollama
from agno.tools.file import FileTools
from agno.tools.docker import DockerTools

agent = Agent(
  # model=Gemini(id="gemini-2.0-flash"),
  # model=Ollama(id="qwen3:4b"),
  # model=OpenRouter(id="gpt-4o"),
  model=DeepSeek(id="deepseek-chat"),
  # model=DeepSeek(id="deepseek-reasoner")
  name="Agent",
  instructions=[
    "你是全能助手，你可以做任何事",
    "You are a Docker management assistant that can perform various Docker operations.",
    "You can manage containers, images, volumes, and networks.",
    "以中文生成回复",
  ],
  tools=[
    ReasoningTools(add_instructions=True),
    DuckDuckGoTools(),
    DockerTools(
      enable_container_management=True,
      enable_image_management=True,
      enable_volume_management=True,
      enable_network_management=True,
    ),
  ],
  add_datetime_to_instructions=True,
  show_full_reasoning=True,
  show_tool_calls=True,
  markdown=True,
  debug_mode=True
)
agent.print_response(
  "List all alluxio running Docker containers", 
  show_full_reasoning=True,
  stream_intermediate_steps=True,
  stream=True
)
agent.print_response("Whats happening in France?", stream=True)
# Get the response in a variable
# run: RunResponse = agent.run("Share a 2 sentence horror story")
# print(run.content)

# Print the response in the terminal
# agent.print_response("Share a 2 sentence happy story", stream=True)
# agent.print_response("What is the most advanced LLM currently? Save the answer to a file.", stream=True)
