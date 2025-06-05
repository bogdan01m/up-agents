import os
from dataclasses import dataclass

from .base_provider import ProviderConfig, ProviderType


@dataclass
class EnvProviderConfig:
    """Provider configuration loaded from environment variables"""

    provider_type: ProviderType
    model_name: str | None = None
    api_key: str | None = None
    base_url: str | None = None
    system_prompt: str | None = None
    retries: int = 5


class ProviderEnvLoader:
    """Utility class for loading provider configuration from environment variables"""

    # Environment variable mappings for each provider
    ENV_MAPPINGS = {
        ProviderType.OPENAI: {
            "api_key": ["OPENAI_API_KEY", "OPENAI_KEY"],
            "model_name": ["OPENAI_MODEL", "OPENAI_MODEL_NAME"],
            "base_url": ["OPENAI_BASE_URL"],
            "system_prompt": ["OPENAI_SYSTEM_PROMPT"],
        },
        ProviderType.OLLAMA: {
            "api_key": ["OLLAMA_API_KEY", "OLLAMA_KEY"],
            "model_name": ["OLLAMA_MODEL", "OLLAMA_MODEL_NAME"],
            "base_url": ["OLLAMA_BASE_URL", "OLLAMA_URL"],
            "system_prompt": ["OLLAMA_SYSTEM_PROMPT"],
        },
        ProviderType.GEMINI: {
            "api_key": ["GEMINI_API_KEY", "GOOGLE_API_KEY", "GEMINI_KEY"],
            "model_name": ["GEMINI_MODEL", "GEMINI_MODEL_NAME"],
            "base_url": ["GEMINI_BASE_URL"],
            "system_prompt": ["GEMINI_SYSTEM_PROMPT"],
        },
        ProviderType.MISTRAL: {
            "api_key": ["MISTRAL_API_KEY", "MISTRAL_KEY"],
            "model_name": ["MISTRAL_MODEL", "MISTRAL_MODEL_NAME"],
            "base_url": ["MISTRAL_BASE_URL"],
            "system_prompt": ["MISTRAL_SYSTEM_PROMPT"],
        },
        ProviderType.OPENROUTER: {
            "api_key": ["OPENROUTER_API_KEY", "OPENROUTER_KEY"],
            "model_name": ["OPENROUTER_MODEL", "OPENROUTER_MODEL_NAME"],
            "base_url": ["OPENROUTER_BASE_URL"],
            "system_prompt": ["OPENROUTER_SYSTEM_PROMPT"],
        },
        ProviderType.CUSTOM_OPENAI: {
            "api_key": ["CUSTOM_OPENAI_API_KEY", "CUSTOM_API_KEY"],
            "model_name": ["CUSTOM_OPENAI_MODEL", "CUSTOM_MODEL"],
            "base_url": ["CUSTOM_OPENAI_BASE_URL", "CUSTOM_BASE_URL"],
            "system_prompt": ["CUSTOM_OPENAI_SYSTEM_PROMPT"],
        },
    }

    @classmethod
    def _get_env_value(cls, env_keys: list[str]) -> str | None:
        """Get environment variable value, trying multiple keys"""
        for key in env_keys:
            value = os.getenv(key)
            if value:
                return value
        return None

    @classmethod
    def load_from_env(cls, provider_type: ProviderType) -> EnvProviderConfig:
        """Load provider configuration from environment variables"""
        if provider_type not in cls.ENV_MAPPINGS:
            raise ValueError(f"No environment mapping found for provider {provider_type.value}")

        mapping = cls.ENV_MAPPINGS[provider_type]

        config = EnvProviderConfig(provider_type=provider_type)

        # Load configuration from environment
        config.api_key = cls._get_env_value(mapping.get("api_key", []))
        config.model_name = cls._get_env_value(mapping.get("model_name", []))
        config.base_url = cls._get_env_value(mapping.get("base_url", []))
        config.system_prompt = cls._get_env_value(mapping.get("system_prompt", []))

        # Try to load retries from environment
        retries_str = os.getenv("LLM_RETRIES", "5")
        try:
            config.retries = int(retries_str)
        except ValueError:
            config.retries = 5

        return config

    @classmethod
    def to_provider_config(
        cls,
        env_config: EnvProviderConfig,
        override_model_name: str | None = None,
        override_api_key: str | None = None,
        override_base_url: str | None = None,
        override_system_prompt: str | None = None,
    ) -> ProviderConfig:
        """Convert EnvProviderConfig to ProviderConfig with optional overrides"""
        return ProviderConfig(
            model_name=override_model_name or env_config.model_name or "",
            api_key=override_api_key or env_config.api_key,
            base_url=override_base_url or env_config.base_url,
            system_prompt=override_system_prompt or env_config.system_prompt or "",
            retries=env_config.retries,
        )

    @classmethod
    def create_provider_config_from_env(
        cls,
        provider_type: ProviderType,
        model_name: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        system_prompt: str | None = None,
    ) -> ProviderConfig:
        """Create ProviderConfig by loading from env and applying overrides"""
        env_config = cls.load_from_env(provider_type)
        return cls.to_provider_config(
            env_config,
            override_model_name=model_name,
            override_api_key=api_key,
            override_base_url=base_url,
            override_system_prompt=system_prompt,
        )


def load_dotenv_if_exists():
    """Load .env file if it exists"""
    from dotenv import load_dotenv
    env_file = os.path.join(os.getcwd(), ".env")
    if os.path.exists(env_file):
        load_dotenv(env_file)
        return True
    return False
