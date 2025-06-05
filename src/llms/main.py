import asyncio
import os

import src.llms.llm_call.llm_providers  # noqa: F401
from src.llms.llm_call.base_provider import ProviderConfig, ProviderType
from src.llms.llm_call.env_config import load_dotenv_if_exists
from src.llms.llm_call.provider_factory import ProviderFactory


async def demo_factory_pattern():
    """Демонстрация использования Factory паттерна для LLM провайдеров"""
    print("=== LLM Provider Factory Demo ===\n")

    # Показать доступные провайдеры
    print("Доступные провайдеры:")
    for provider_type in ProviderFactory.get_available_providers():
        print(f"  - {provider_type.value}")
    print()

    # Демонстрация создания провайдера через конфигурацию
    print("1. Создание провайдера через ProviderConfig:")
    config = ProviderConfig(
        model_name="gpt-3.5-turbo",
        api_key="demo-key",
        system_prompt="Ты полезный помощник",
    )

    try:
        openai_provider = ProviderFactory.create_provider(ProviderType.OPENAI, config)
        print(f"Создан провайдер: {openai_provider}")
        print(f"Тип провайдера: {openai_provider.provider_type.value}")
        print()
    except ValueError as e:
        print(f"Ошибка создания провайдера: {e}")

    # Демонстрация создания провайдера из переменных окружения
    print("2. Создание провайдера из переменных окружения:")

    # Установим тестовые переменные окружения
    os.environ["OLLAMA_MODEL"] = "llama2:7b"
    os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434/v1"
    os.environ["OLLAMA_SYSTEM_PROMPT"] = "Ты полезный ассистент из env"

    try:
        ollama_provider = ProviderFactory.create_provider_from_env(ProviderType.OLLAMA)
        print(f"Создан провайдер из env: {ollama_provider}")
        print(f"Модель: {ollama_provider.model_name}")
        print(f"Base URL: {ollama_provider.base_url}")
        print(f"System prompt: {ollama_provider.system_prompt}")
        print()
    except ValueError as e:
        print(f"Ошибка создания провайдера из env: {e}")

    # Демонстрация переопределения параметров
    print("3. Создание провайдера из env с переопределением:")
    try:
        custom_provider = ProviderFactory.create_provider_from_env(
            ProviderType.OLLAMA,
            model_name="llama2:13b",  # переопределяем модель
            system_prompt="Переопределенный system prompt"
        )
        print(f"Создан провайдер с переопределением: {custom_provider}")
        print(f"Модель: {custom_provider.model_name}")
        print(f"System prompt: {custom_provider.system_prompt}")
        print()
    except ValueError as e:
        print(f"Ошибка создания провайдера с переопределением: {e}")

    # Очистим тестовые переменные
    del os.environ["OLLAMA_MODEL"]
    del os.environ["OLLAMA_BASE_URL"]
    del os.environ["OLLAMA_SYSTEM_PROMPT"]


def main():
    # Загружаем .env файл если существует
    if load_dotenv_if_exists():
        print("✅ Загружен .env файл\n")

    print("Демонстрация Factory/Registry паттерна для LLM провайдеров\n")
    asyncio.run(demo_factory_pattern())


if __name__ == "__main__":
    main()
