# file: hello_gemini_autogen.py
import os
import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

import dotenv
dotenv.load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

async def main():
    # 1) Configure Gemini via its OpenAI-compatible endpoint
    model_client = OpenAIChatCompletionClient(
        model="gemini-2.0-flash",  # or "gemini-2.5-flash"
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=os.environ["GEMINI_API_KEY"],  # set this in your shell
        # Optional model hints (handy for non-OpenAI backends)
        model_info={
            "vision": True,
            "function_calling": True,
            "json_output": False,
            "family": "unknown",
        },
    )

    # 2) Wrap the client in an AutoGen AssistantAgent
    assistant = AssistantAgent(
        name="helper",
        model_client=model_client,
        system_message="You are a concise assistant."
    )

    # 3) Run a tiny task
    result = await assistant.run(task="Say 'Hello, world!' and tell me a dark joke.")
    print("---------Answer----------")  # prints the assistant’s reply
    print(result)  # prints the assistant’s reply


if __name__ == "__main__":
    asyncio.run(main())

'''
output:
---------Answer----------
messages=[TextMessage(id='51...714', source='user', models_usage=None, metadata={}, created_at=datetime.datetime(2025, 8, 13, 19, 46, 59, 297318, tzinfo=datetime.timezone.utc), content="Say 'Hello, world!' and tell me a dark joke.", type='TextMessage'), TextMessage(id='a73...38da7', source='helper', models_usage=RequestUsage(prompt_tokens=19, completion_tokens=20), metadata={}, created_at=datetime.datetime(2025, 8, 13, 19, 47, 1, 304821, tzinfo=datetime.timezone.utc), content="Hello, world!\n\nWhy don't scientists trust atoms? Because they make up everything!\n", type='TextMessage')] stop_reason=None
'''