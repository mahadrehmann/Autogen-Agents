import os
import asyncio
import dotenv
dotenv.load_dotenv()

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Initialize Gemini-compatible model client
model_client = OpenAIChatCompletionClient(
    model="gemini-2.5-flash",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.environ["GEMINI_API_KEY"],
    model_info={
        "function_calling": True,
        "vision": False,
        "json_output": False,
        "family": "gemini",
    },
)

# Tool: fetch weather (mock implementation)
async def get_weather(city: str) -> str:
    return f"The current weather in {city} is 28 °C and sunny."

# Tool: analyze weather description
async def analyze_weather(weather_desc: str) -> str:
    return f"Analysis: '{weather_desc}' suggests perfect weather for outdoor walks."

# Agent that fetches weather
weather_agent = AssistantAgent(
    name="weather_agent",
    model_client=model_client,
    tools=[get_weather],
    system_message="You are a weather assistant. Use get_weather(tool) when asked.",
    reflect_on_tool_use=True,
    model_client_stream=True,
)

# Agent that analyzes weather
analysis_agent = AssistantAgent(
    name="analysis_agent",
    model_client=model_client,
    tools=[analyze_weather],
    system_message="You are an analyst who inspects weather descriptions.",
    reflect_on_tool_use=True,
    model_client_stream=True,
)

# Multi-agent orchestration: agents take turns
agent_team = RoundRobinGroupChat(
    [weather_agent, analysis_agent],  # ← positional list of agents
    max_turns=4,
)


async def main():
    # Prompt: Ask agents to fetch and analyze weather for Peshawar
    await Console(agent_team.run_stream(task="What is the weather in Peshawar, and what does it imply?"))
    await model_client.close()

if __name__ == "__main__":
    asyncio.run(main())

'''
output:
(venv) mahad@mahad-Latitude:~/Desktop/Codes/BlueScarf/Autogen$ python3 mutliagent.py 
/home/mahad/Desktop/Codes/BlueScarf/Autogen/venv/lib/python3.12/site-packages/autogen_ext/models/openai/_openai_client.py:453: UserWarning: Missing required field 'structured_output' in ModelInfo. This field will be required in a future version of AutoGen.
  validate_model_info(self._model_info)
---------- TextMessage (user) ----------
What is the weather in Peshawar, and what does it imply?
---------- ToolCallRequestEvent (weather_agent) ----------
[FunctionCall(id='', arguments='{"city":"Peshawar"}', name='get_weather')]
---------- ToolCallExecutionEvent (weather_agent) ----------
[FunctionExecutionResult(content='The current weather in Peshawar is 28 °C and sunny.', name='get_weather', call_id='', is_error=False)]
---------- ModelClientStreamingChunkEvent (weather_agent) ----------
The weather in Peshawar is currently 28°C and sunny. This implies pleasant conditions, suitable for outdoor activities.
---------- ToolCallRequestEvent (analysis_agent) ----------
[FunctionCall(id='', arguments='{"weather_desc":"The weather in Peshawar is currently 28°C and sunny. This implies pleasant conditions, suitable for outdoor activities."}', name='analyze_weather')]
---------- ToolCallExecutionEvent (analysis_agent) ----------
[FunctionExecutionResult(content="Analysis: 'The weather in Peshawar is currently 28°C and sunny. This implies pleasant conditions, suitable for outdoor activities.' suggests perfect weather for outdoor walks.", name='analyze_weather', call_id='', is_error=False)]
---------- ModelClientStreamingChunkEvent (analysis_agent) ----------
Analysis: 'The weather in Peshawar is currently 28°C and sunny. This implies pleasant conditions, suitable for outdoor activities.' suggests perfect weather for outdoor walks.
---------- ModelClientStreamingChunkEvent (weather_agent) ----------
That's a good analysis! Indeed, 28°C and sunny would be quite pleasant for outdoor walks.
---------- ModelClientStreamingChunkEvent (analysis_agent) ----------
That's great to hear! I'm glad I could provide a helpful analysis.

'''