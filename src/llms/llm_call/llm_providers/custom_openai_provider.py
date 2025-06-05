
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from ..base_provider import BaseLLMProvider, ProviderConfig, ProviderType


class CustomOpenAILLMProvider(BaseLLMProvider):
    """Custom OpenAI-compatible LLM Provider implementation"""

    @property
    def provider_type(self) -> ProviderType:
        return ProviderType.CUSTOM_OPENAI

    async def get_response(self, query: str) -> str:
        """Get response from custom OpenAI-compatible model"""
        if not self.base_url:
            raise ValueError("Custom OpenAI provider requires base_url to be set")

        model = OpenAIModel(
            model_name=self.model_name,
            provider=OpenAIProvider(base_url=self.base_url, api_key=self.api_key),
        )
        agent = Agent(
            model=model, retries=self.retries, system_prompt=self.system_prompt
        )
        result = await agent.run(query)
        return result.output

    def validate_config(self) -> bool:
        """Validate Custom OpenAI configuration"""
        if not self.model_name:
            return False
        if not self.base_url:
            return False
        return True


async def get_custom_openai_provider_response(
    model_name: str,
    query: str,
    provider_url: str,
    system: str | None = "",
    api_key: str | None = None,
) -> str:
    """
    Legacy function to get custom OpenAI-compatible model response
    `model_name` - model name from custom provider models
    `query` - user query
    `provider_url` - url to connect via api (e.g. "https://api.example.com/v1")
    `system` - system prompt [optional]
    `api key` - provider api key (if required) [optional]
    """
    config = ProviderConfig(
        model_name=model_name,
        api_key=api_key,
        base_url=provider_url,
        system_prompt=system,
    )
    provider = CustomOpenAILLMProvider(config)
    return await provider.get_response(query)
