
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from ..base_provider import BaseLLMProvider, ProviderConfig, ProviderType


class OllamaLLMProvider(BaseLLMProvider):
    """Ollama LLM Provider implementation"""

    @property
    def provider_type(self) -> ProviderType:
        return ProviderType.OLLAMA

    async def get_response(self, query: str) -> str:
        """Get response from Ollama model"""
        base_url = self.base_url or "http://localhost:11434/v1"
        model = OpenAIModel(
            model_name=self.model_name,
            provider=OpenAIProvider(base_url=base_url, api_key=self.api_key),
        )
        agent = Agent(
            model=model, retries=self.retries, system_prompt=self.system_prompt
        )
        result = await agent.run(query)
        return result.output

    def validate_config(self) -> bool:
        """Validate Ollama configuration"""
        if not self.model_name:
            return False
        return True


async def get_ollama_response(
    model_name: str,
    query: str,
    provider_url: str | None = "http://localhost:11434/v1",
    system: str | None = "",
    api_key: str | None = None,
) -> str:
    """
    Legacy function to get Ollama model response
    `model_name` - model name from ollama models
    `query` - user query
    `provider_url` - url to connect via api [optional] (e.g. "http://localhost:11434/v1" by default)
    `system` - system prompt [optional]
    `api key` - provider api key (if required) [optional]
    """
    config = ProviderConfig(
        model_name=model_name,
        api_key=api_key,
        base_url=provider_url,
        system_prompt=system,
    )
    provider = OllamaLLMProvider(config)
    return await provider.get_response(query)
