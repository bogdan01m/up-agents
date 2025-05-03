from typing import Optional
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider


async def get_custom_openrouter_provider_response(
    model_name: str,
    query: str,
    system: Optional[str] = "",
    api_key: Optional[str] = None,
) -> str:
    """
    function to get open ai model response
    `model_name` - model name from custom provider models
    `query` - user query
    `system` - system prompt [optional]
    `api key` - provider api key (if required) [optional]
    """
    model = OpenAIModel(
        model_name=model_name,
        provider=OpenAIProvider(
            base_url="https://openrouter.ai/api/v1", api_key=api_key
        ),
    )
    agent = Agent(model=model, retries=5, system_prompt=system)
    result = await agent.run(query)
    return result.output
