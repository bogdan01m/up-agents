
from pydantic_ai import Agent
from pydantic_ai.models.mistral import MistralModel
from pydantic_ai.providers.mistral import MistralProvider

from ..base_provider import BaseLLMProvider, ProviderConfig, ProviderType


class MistralLLMProvider(BaseLLMProvider):
    """Mistral LLM Provider implementation"""

    @property
    def provider_type(self) -> ProviderType:
        return ProviderType.MISTRAL

    async def get_response(self, query: str) -> str:
        """Get response from Mistral model"""
        model = MistralModel(
            model_name=self.model_name,
            provider=MistralProvider(api_key=self.api_key),
        )
        agent = Agent(
            model=model, retries=self.retries, system_prompt=self.system_prompt
        )
        result = await agent.run(query)
        return result.output

    def validate_config(self) -> bool:
        """Validate Mistral configuration"""
        if not self.model_name:
            return False
        return True


async def get_mistral_response(
    model_name: str,
    query: str,
    system: str | None = "",
    api_key: str | None = None,
) -> str:
    """
    Legacy function to get Mistral model response
    `model_name` - model name from mistral models
    `query` - user query
    `system` - system prompt [optional]
    `api key` - provider api key (if required) [optional]
    """
    config = ProviderConfig(
        model_name=model_name, api_key=api_key, system_prompt=system
    )
    provider = MistralLLMProvider(config)
    return await provider.get_response(query)
