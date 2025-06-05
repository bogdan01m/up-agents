

from .base_provider import BaseLLMProvider, ProviderConfig, ProviderType
from .env_config import ProviderEnvLoader


class ProviderFactory:
    """Factory class for creating LLM providers"""

    _providers: dict[ProviderType, type[BaseLLMProvider]] = {}

    @classmethod
    def register_provider(
        cls, provider_type: ProviderType, provider_class: type[BaseLLMProvider]
    ):
        """Register a new provider class"""
        cls._providers[provider_type] = provider_class

    @classmethod
    def create_provider(
        cls, provider_type: ProviderType, config: ProviderConfig
    ) -> BaseLLMProvider:
        """
        Create a provider instance

        Args:
            provider_type: Type of provider to create
            config: Provider configuration

        Returns:
            Provider instance

        Raises:
            ValueError: If provider type is not registered
        """
        if provider_type not in cls._providers:
            raise ValueError(f"Provider type {provider_type.value} is not registered")

        provider_class = cls._providers[provider_type]
        provider = provider_class(config)

        # Validate configuration
        if not provider.validate_config():
            raise ValueError(
                f"Invalid configuration for provider {provider_type.value}"
            )

        return provider

    @classmethod
    def get_available_providers(cls) -> list[ProviderType]:
        """Get list of available provider types"""
        return list(cls._providers.keys())

    @classmethod
    def is_provider_registered(cls, provider_type: ProviderType) -> bool:
        """Check if provider type is registered"""
        return provider_type in cls._providers

    @classmethod
    def create_provider_from_env(
        cls,
        provider_type: ProviderType,
        model_name: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        system_prompt: str | None = None,
    ) -> BaseLLMProvider:
        """
        Create a provider instance using environment configuration with optional overrides

        Args:
            provider_type: Type of provider to create
            model_name: Override model name (optional)
            api_key: Override API key (optional)
            base_url: Override base URL (optional)
            system_prompt: Override system prompt (optional)

        Returns:
            Provider instance

        Raises:
            ValueError: If provider type is not registered or configuration is invalid
        """
        config = ProviderEnvLoader.create_provider_config_from_env(
            provider_type=provider_type,
            model_name=model_name,
            api_key=api_key,
            base_url=base_url,
            system_prompt=system_prompt,
        )

        return cls.create_provider(provider_type, config)


class ProviderRegistry:
    """Registry for managing provider instances"""

    def __init__(self):
        self._providers: dict[str, BaseLLMProvider] = {}

    def register_provider_instance(self, name: str, provider: BaseLLMProvider):
        """Register a provider instance with a name"""
        self._providers[name] = provider

    def get_provider(self, name: str) -> BaseLLMProvider | None:
        """Get provider instance by name"""
        return self._providers.get(name)

    def remove_provider(self, name: str) -> bool:
        """Remove provider instance"""
        if name in self._providers:
            del self._providers[name]
            return True
        return False

    def list_providers(self) -> dict[str, str]:
        """List all registered provider instances"""
        return {name: str(provider) for name, provider in self._providers.items()}

    def clear(self):
        """Clear all registered providers"""
        self._providers.clear()


# Global registry instance
provider_registry = ProviderRegistry()
