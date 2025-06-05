
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from ..base_provider import BaseLLMProvider, ProviderConfig, ProviderType


class OpenAILLMProvider(BaseLLMProvider):
    """OpenAI LLM Provider implementation"""

    @property
    def provider_type(self) -> ProviderType:
        return ProviderType.OPENAI

    async def get_response(self, query: str) -> str:
        """Get response from OpenAI model"""
        model = OpenAIModel(
            model_name=self.model_name, provider=OpenAIProvider(api_key=self.api_key)
        )
        agent = Agent(
            model=model, retries=self.retries, system_prompt=self.system_prompt
        )
        result = await agent.run(query)
        return result.output

    def validate_config(self) -> bool:
        """Validate OpenAI configuration"""
        if not self.model_name:
            return False
        return True


async def get_openai_response(
    model_name: str,
    query: str,
    system: str | None = "",
    api_key: str | None = None,
) -> str:
    """
    Legacy function to get OpenAI model response
    `model_name` - model name from open ai models
    `query` - user query
    `system` - system prompt [optional]
    `api key` - provider api key (if required) [optional]
    """
    config = ProviderConfig(
        model_name=model_name, api_key=api_key, system_prompt=system
    )
    provider = OpenAILLMProvider(config)
    return await provider.get_response(query)
