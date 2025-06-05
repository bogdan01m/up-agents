from ..base_provider import ProviderType
from ..provider_factory import ProviderFactory
from .custom_openai_provider import CustomOpenAILLMProvider
from .gemini_provider import GeminiLLMProvider
from .mistral_provider import MistralLLMProvider
from .ollama_provider import OllamaLLMProvider
from .openai_provider import OpenAILLMProvider
from .openrouter_provider import OpenRouterLLMProvider

# Register all providers
ProviderFactory.register_provider(ProviderType.OPENAI, OpenAILLMProvider)
ProviderFactory.register_provider(ProviderType.OLLAMA, OllamaLLMProvider)
ProviderFactory.register_provider(ProviderType.GEMINI, GeminiLLMProvider)
ProviderFactory.register_provider(ProviderType.MISTRAL, MistralLLMProvider)
ProviderFactory.register_provider(ProviderType.OPENROUTER, OpenRouterLLMProvider)
ProviderFactory.register_provider(ProviderType.CUSTOM_OPENAI, CustomOpenAILLMProvider)

# Export all classes and functions
__all__ = [
    "OpenAILLMProvider",
    "OllamaLLMProvider",
    "GeminiLLMProvider",
    "MistralLLMProvider",
    "OpenRouterLLMProvider",
    "CustomOpenAILLMProvider",
    "ProviderFactory",
    "ProviderType",
]
