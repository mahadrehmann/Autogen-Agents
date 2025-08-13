# file: hello_gemini_autogen_websearch.py
import os
import asyncio
import dotenv
dotenv.load_dotenv()

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console

async def main() -> None:
    # Configure Gemini client
    model_client = OpenAIChatCompletionClient(
        model="gemini-2.0-flash",  # or "gemini-2.5-flash"
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=os.environ["GEMINI_API_KEY"],
        model_info={
            "vision": True,
            "function_calling": True,
            "json_output": True,
            "family": "unknown",
        },
    )

    # Set up Web Surfer agent for real-time web interactions
    web_surfer_agent = MultimodalWebSurfer(
        name="web_surfer",
        model_client=model_client,
    )

    # Optionally, you can have a single agent team or multiple agents
    agent_team = RoundRobinGroupChat([web_surfer_agent], max_turns=3)

    # Launch the task: ask it to search web and present fun fact
    stream = agent_team.run_stream(
        task="Search the web and tell me a fun fact about Karachi."
    )
    await Console(stream)

    # Close the surfer's browser resources when done
    await web_surfer_agent.close()

if __name__ == "__main__":
    asyncio.run(main())

'''
output:
---------- TextMessage (user) ----------
Search the web and tell me a fun fact about Karachi.
---------- MultiModalMessage (web_surfer) ----------
I typed 'fun fact about Karachi' into the browser search bar.

The web browser is open to the page [fun fact about Karachi - Search](https://www.bing.com/search?q=fun+fact+about+Karachi&FORM=QBLH).
The viewport shows 20% of the webpage, and is positioned at the top of the page
The following text is visible in the viewport:

Skip to content
fun fact about KarachiMobileAll
Search
Images
Videos
Maps
Copilot
More
Tools
About 1,270,000 resultsKarachi, the largest city in Pakistan, is a vibrant metropolis known for its rich culture, diverse population, and significant economic role.
Key Facts About Karachi
Population and Diversity: Karachi is the most populous city in Pakistan, with estimates suggesting over 20 million residents. It is a melting pot of cultures, home to various ethnic groups, including Sindhis, Muhajirs, Punjabis, Balochis, and Pashtuns. 2
Historical Significance: Originally founded as a fortified village named Kolachi in the 18th century, Karachi served as the first capital of Pakistan until 1959 when the capital was moved to Islamabad. 2
Economic Hub: Karachi is the financial center of Pakistan, hosting the Pakistan Stock Exchange, which is the largest stock exchange in the country. The city plays a crucial role in the nation’s economy, contributing significantly to trade and commerce. 2
Cultural Landmarks: The Grand Jamiah Mosque, completed in 2021, is the third largest mosque in the world, capable of accommodating around 800,000 worshippers. Additionally, the Quaid-e-Azam's Mausoleum, the resting place of Muhammad Ali Jinnah, the founder of Pakistan, is located in Karachi. 3
Culinary Scene: Karachi is renowned for its diverse and flavorful cuisine, including popular dishes like Biryani, Nihari, and various street foods. The city is often referred to as the food capital of southwestern Asia. 2
Read more
Facts.net
37 Facts About Karachi
Karachi, the vibrant city of Pakistan, is a bustling metropolis that never fails to capture the imagination of locals and visitors alike. With a rich culture, fascinating history, …
millionfacts.co.uk
25 interesting facts about Karachi ᐈ MillionFacts
Karachi, the bustling metropolis of Pakistan, stands as a testament to diversity, resilience, and dynamic growth. Serving as the country’s economic backbone, this city is a melting…
View all
Expert World Travel
https://expertworldtravel.com › karachi-facts
20 Facts About Karachi: Fun & Interesting - Expert World TravelKarachi was the first capital of Pakistan and it made sense since it’s the major trade hub and port for the country. But, Karachi lost its title as the capital of Pakistan when Islamabad became the capital in August of 1967. KarachiCapital of Sindh, PakistanAll images
Karachi is the capital city of the Pakistani province of Sindh. It is the largest and most populous city in Pakistan, and 12th largest globally, with a population of over 20 million. It is situated at the southern …Wikipedia

The following metadata was extracted from the webpage:

{
    "meta_tags": {
        "referrer": "origin-when-cross-origin",
        "SystemEntropyOriginTrialToken": "A7cQcumnCpYMtO5VusikffR0WGYjWyI/y0wN/izvd92Pwty8awTPuPqSlIYk10vLdR6azJGHCZNOtmniRmPY4rwAAABeeyJvcmlnaW4iOiJodHRwczovL3d3dy5iaW5nLmNvbTo0NDMiLCJmZWF0dXJlIjoiTXNVc2VyQWdlbnRMYXVuY2hOYXZUeXBlIiwiZXhwaXJ5IjoxNzY0NzIwMDAwfQ==",
        "ConfidenceOriginTrialToken": "Aqw360MHzRcmtEVv55zzdIWcTk2BBYHcdBAOysNJZP4qkN8M+5vUq36ITHFVst8LiX36KBZJXB8xvyBgdK2z5Q0AAAB6eyJvcmlnaW4iOiJodHRwczovL2JpbmcuY29tOjQ0MyIsImZlYXR1cmUiOiJQZXJmb3JtYW5jZU5hdmlnYXRpb25UaW1pbmdDb25maWRlbmNlIiwiZXhwaXJ5IjoxNzYwNDAwMDAwLCJpc1N1YmRvbWFpbiI6dHJ1ZX0=",
        "og:description": "Intelligent search from Bing makes it easier to quickly find what you\u2019re looking for and rewards you.",
        "og:site_name": "Bing",
        "og:title": "fun fact about Karachi - Bing",
        "og:url": "https://www.bing.com/search?q=fun+fact+about+Karachi&FORM=QBLH",
        "fb:app_id": "3732605936979161",
        "og:image": "http://www.bing.com/sa/simg/facebook_sharing_5.png",
        "og:type": "website",
        "og:image:width": "600",
        "og:image:height": "315"
    }
}

Here is a screenshot of the page.
<image>
---------- TextMessage (web_surfer) ----------

I can answer the question directly from the current page. One fun fact about Karachi is that it is the most populous city in Pakistan, with estimates suggesting over 20 million residents. It is a melting pot of cultures, home to various ethnic groups, including Sindhis, Muhajirs, Punjabis, Balochis, and Pashtuns. Also, Karachi served as the first capital of Pakistan until 1959.

---------- TextMessage (web_surfer) ----------

'''