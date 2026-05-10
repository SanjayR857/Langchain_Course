from dotenv import load_dotenv

load_dotenv()

from langchain.tools import tool
from typing import Dict, Any
from tavily import TavilyClient

tavily_client = TavilyClient()

@tool
def web_search(query: str) -> Dict[str, Any]:

    """Search the web for information"""

    return tavily_client.search(query)

system_prompt = """

You are a personal chef. The user will give you a list of ingredients they have left over in their house.

Using the web search tool, search the web for recipes that can be made with the ingredients they have.

Return recipe suggestions and eventually the recipe instructions to the user, if requested.

"""

from langchain.agents import create_agent

import os 
from langchain_openai import AzureChatOpenAI

model = AzureChatOpenAI(
    azure_deployment=os.getenv("OPENAI_DEFAULT_DEPLOYMENT"),  # or your deployment
    api_version="2025-04-01-preview",  # or your api version
    azure_endpoint=os.getenv("OPENAI_ENDPOINT"),  # or your endpoint
)

agent = create_agent(
    model=model,
    tools=[web_search],
    system_prompt=system_prompt
)