
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider

from ..base_provider import BaseLLMProvider, ProviderConfig, ProviderType


class GeminiLLMProvider(BaseLLMProvider):
    """Gemini LLM Provider implementation"""

    @property
    def provider_type(self) -> ProviderType:
        return ProviderType.GEMINI

    async def get_response(self, query: str) -> str:
        """Get response from Gemini model"""
        model = GeminiModel(
            model_name=self.model_name,
            provider=GoogleGLAProvider(api_key=self.api_key),
        )
        agent = Agent(
            model=model, retries=self.retries, system_prompt=self.system_prompt
        )
        result = await agent.run(query)
        return result.output

    def validate_config(self) -> bool:
        """Validate Gemini configuration"""
        if not self.model_name:
            return False
        return True


async def get_gemini_response(
    model_name: str,
    query: str,
    system: str | None = "",
    api_key: str | None = None,
) -> str:
    """
    Legacy function to get Gemini model response
    `model_name` - model name from gemini models
    `query` - user query
    `system` - system prompt [optional]
    `api key` - provider api key (if required) [optional]
    """
    config = ProviderConfig(
        model_name=model_name, api_key=api_key, system_prompt=system
    )
    provider = GeminiLLMProvider(config)
    return await provider.get_response(query)
