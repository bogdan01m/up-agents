from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any


class ProviderType(Enum):
    OPENAI = "openai"
    OLLAMA = "ollama"
    GEMINI = "gemini"
    MISTRAL = "mistral"
    OPENROUTER = "openrouter"
    CUSTOM_OPENAI = "custom_openai"


@dataclass
class ProviderConfig:
    """Configuration for LLM provider"""

    model_name: str
    api_key: str | None = None
    base_url: str | None = None
    system_prompt: str | None = ""
    retries: int = 5
    extra_params: dict[str, Any] | None = None


class BaseLLMProvider(ABC):
    """Abstract base class for all LLM providers"""

    def __init__(self, config: ProviderConfig):
        self.config = config
        self.model_name = config.model_name
        self.api_key = config.api_key
        self.base_url = config.base_url
        self.system_prompt = config.system_prompt
        self.retries = config.retries
        self.extra_params = config.extra_params or {}

    @property
    @abstractmethod
    def provider_type(self) -> ProviderType:
        """Return the provider type"""
        pass

    @abstractmethod
    async def get_response(self, query: str) -> str:
        """
        Get response from the LLM provider

        Args:
            query: User query/prompt

        Returns:
            Response string from the model
        """
        pass

    @abstractmethod
    def validate_config(self) -> bool:
        """
        Validate provider configuration

        Returns:
            True if configuration is valid, False otherwise
        """
        pass

    def __str__(self) -> str:
        return f"{self.provider_type.value}:{self.model_name}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(model={self.model_name})>"
