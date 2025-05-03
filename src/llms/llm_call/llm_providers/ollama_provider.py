from typing import Optional
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider


async def get_ollama_response(
    model_name: str,
    query: str,
    provider_url: Optional[str] = "http://localhost:11434/v1",
    system: Optional[str] = "",
    api_key: Optional[str] = None,
) -> str:
    """
    function to get open ai model response
    `model_name` - model name from ollama models
    `query` - user query
    `provider_url` - url to connect via api [optional] (e.g. "http://localhost:11434/v1" by default)
    `system` - system prompt [optional]
    `api key` - provider api key (if required) [optional]
    """
    model = OpenAIModel(
        model_name=model_name,
        provider=OpenAIProvider(base_url=provider_url, api_key=api_key),
    )
    agent = Agent(model=model, retries=5, system_prompt=system)
    result = await agent.run(query)
    return result.output
