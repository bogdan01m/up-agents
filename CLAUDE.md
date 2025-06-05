# Claude Instructions for up-agents

## Project Overview
Терминальная агентная система с поддержкой различных LLM провайдеров (исключая Anthropic) и MCP протокола для инструментов.

## Development Environment

### Package Management
- Используется **uv** для управления Python зависимостями из корня проекта
- Команды: `uv add <package>`, `uv run <script>`, `uv sync`
- CLI команда: `uv run up-agents` или `uv run python -m src.llms.main`

### Code Quality
- **Linting**: `uvx ruff .`
- **Formatting**: `uvx black .`
- Всегда запускать перед коммитами

### Git Integration
- Доступен **GitHub CLI** для работы с репозиторием
- Команды: `gh pr create`, `gh issue list`, etc.

## Project Structure
```
src/
├── llms/                    # LLM провайдеры (уже существует)
│   └── llm_call/
│       └── llm_providers/   # Конкретные провайдеры
├── cli/                     # Терминальный интерфейс (планируется)
├── mcp/                     # MCP интеграция (планируется)
└── config/                  # Конфигурация (планируется)
```

## Security
- **ЗАПРЕЩЕНО** открывать или читать .env файлы
- API ключи только через переменные окружения

## LLM Providers
Поддерживаемые провайдеры:
- OpenAI (GPT-4, GPT-3.5)
- Google Gemini
- Mistral AI
- Ollama (локальные модели)
- OpenRouter
- Custom - любой open ai совместимый (например vllm или sglang)

## Architecture Patterns
- **Factory/Registry pattern** для LLM провайдеров (реализован):
  - Базовый интерфейс `BaseLLMProvider`
  - Фабрика `ProviderFactory` для создания провайдеров
  - Реестр `ProviderRegistry` для управления экземплярами
  - Автоматическая регистрация провайдеров через `__init__.py`
- MCP протокол для расширяемости инструментов (планируется)
- Чистый терминальный интерфейс без встроенных инструментов (планируется)