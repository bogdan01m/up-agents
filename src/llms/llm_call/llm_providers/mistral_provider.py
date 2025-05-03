from typing import Optional
from pydantic_ai import Agent
from pydantic_ai.models.mistral import MistralModel
from pydantic_ai.providers.mistral import MistralProvider


async def get_mistral_response(
    model_name: str,
    query: str,
    system: Optional[str] = "",
    api_key: Optional[str] = None,
) -> str:
    """
    function to get open ai model response
    `model_name` - model name from open ai models
    `query` - user query
    `system` - system prompt [optional]
    `api key` - provider api key (if required) [optional]
    """
    model = MistralModel(
        model_name=model_name,
        provider=MistralProvider(api_key=api_key),
    )
    agent = Agent(model=model, retries=5, system_prompt=system)
    result = await agent.run(query)
    return result.output
