import os
import asyncio
import dotenv
dotenv.load_dotenv()

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Define your Gemini-compatible model client
model_client = OpenAIChatCompletionClient(
    model="gemini-2.5-flash",  # Use Gemini model (e.g., 2.0-flash or 2.5-flash)
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.environ["GEMINI_API_KEY"],
    model_info={
        "function_calling": True,   # allow tool/function calls
        "vision": False,            # no vision needed for weather
        "json_output": False,
        "family": "gemini",
    },
)

# Simple weather tool function
async def get_weather(city: str) -> str:
    return f"The weather in {city} is likely sunny and 73°F (fictional for demo)."

# Define the assistant agent with the tool and streaming enabled
agent = AssistantAgent(
    name="weather_agent",
    model_client=model_client,
    tools=[get_weather],
    system_message="You are a helpful assistant that can fetch the weather by calling the provided function.",
    reflect_on_tool_use=True,
    model_client_stream=True,
)

async def main() -> None:
    # Run the agent and stream response to console
    await Console(agent.run_stream(task="What is the weather in Peshawar?"))
    await model_client.close()

if __name__ == "__main__":
    asyncio.run(main())
