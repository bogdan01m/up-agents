# up-agents

🤖 **Терминальная агентная система с поддержкой различных LLM провайдеров**

Полноценный CLI чат-интерфейс, который подключается к множеству LLM провайдеров через единый терминальный интерфейс.

**Языковые версии:** Русский | [English](README.md)

## 🚀 Установка

```bash
# Клонирование репозитория
git clone https://github.com/bogdan01m/up-agents.git
cd up-agents

# Установка зависимостей
uv sync

# Настройка переменных окружения
cp .env.example .env
# Отредактируйте .env файл, добавив ваши API ключи
```

## 🔧 Настройка

Настройте ваши LLM провайдеры, заполнив `.env` файл:

```bash
# OpenAI
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4-nano
OPENAI_SYSTEM_PROMPT="You are helpful assistant. You are able to use tools"

# Google Gemini
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
GEMINI_SYSTEM_PROMPT="You are helpful assistant. You are able to use tools"

# Mistral AI
MISTRAL_API_KEY=your_mistral_api_key_here
MISTRAL_MODEL=mistral-large-latest
MISTRAL_SYSTEM_PROMPT="You are helpful assistant. You are able to use tools"

# Ollama (локальный сервер)
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=qwen3:8b
OLLAMA_SYSTEM_PROMPT="You are helpful assistant. You are able to use tools"

# OpenRouter
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=mistralai/devstral-small:free
OPENROUTER_SYSTEM_PROMPT="You are helpful assistant. You are able to use tools"

# Пользовательский OpenAI-совместимый API
CUSTOM_OPENAI_API_KEY=your_custom_api_key_here
CUSTOM_OPENAI_BASE_URL=https://your-custom-endpoint.com/v1
CUSTOM_OPENAI_MODEL=your-model-name
CUSTOM_OPENAI_SYSTEM_PROMPT="You are helpful assistant. You are able to use tools"
```

## 📋 Использование

### Команды чата

```bash
# Интерактивный чат с автовыбором провайдера
uv run up-agents chat

# Одиночный запрос с конкретным провайдером
uv run up-agents chat -p ollama "Привет, как дела?"

# Чат с пользовательской моделью и системным промптом
uv run up-agents chat -p openai -m gpt-4 -s "Ты помощник по кодингу" "Напиши Python функцию"

# Чат без сохранения истории
uv run up-agents chat -p ollama --no-history "Быстрый вопрос"
```

### Управление провайдерами

```bash
# Список всех доступных провайдеров
uv run up-agents providers list

# Тестирование соединения с провайдером
uv run up-agents providers test ollama

# Информация о провайдере
uv run up-agents providers info openai
```

### Управление сессиями

```bash
# Список чат-сессий
uv run up-agents session list

# Возобновление предыдущей сессии
uv run up-agents session resume <session-id>

# Экспорт сессии в файл
uv run up-agents session export <session-id> --format markdown
```

### Конфигурация

```bash
# Показать текущую конфигурацию
uv run up-agents config list

# Проверить настройки провайдеров
uv run up-agents config validate
```

## 🤖 Поддерживаемые провайдеры

| Провайдер | Модели | Статус |
|----------|--------|---------|
| **OpenAI** | GPT-4, GPT-3.5-turbo, GPT-4-nano | ✅ Готов к продакшну |
| **Google Gemini** | gemini-2.5-flash, gemini-pro | ✅ Готов к продакшну |
| **Mistral AI** | mistral-large-latest, mistral-medium | ✅ Готов к продакшну |
| **Ollama** | llama2, qwen3, codellama и др. | ✅ Готов к продакшну |
| **OpenRouter** | 100+ моделей через единый API | ✅ Готов к продакшну |
| **Custom OpenAI** | Любая OpenAI-совместимая точка | ✅ Готов к продакшну |

### ✨ Возможности

- **Реальная интеграция с LLM** - Прямые API вызовы ко всем провайдерам
- **Автовыбор провайдера** - Интерактивный выбор провайдера
- **Красивый терминальный интерфейс** - Поддержка markdown форматирования
- **Настройка через окружение** - Безопасная настройка через `.env`
- **Управление сессиями** - История чатов и возобновление
- **Гибкое использование** - Одиночные запросы или интерактивные сессии

## 📁 Структура проекта

```
src/
├── cli/                     # CLI интерфейс
│   ├── commands/           # Команды: chat, providers, session
│   ├── ui/                 # Терминальный UI
│   └── session/           # Управление сессиями
├── llms/                   # LLM провайдеры
│   └── llm_call/          # Factory паттерн для провайдеров
└── mcp/                   # MCP интеграция (планируется)
```

## 🛠️ Разработка

```bash
# Форматирование кода
uvx black .

# Линтинг
uvx ruff .

# Запуск демо Factory паттерна
uv run up-agents-demo

# Тестирование чата
uv run up-agents chat -p ollama "Привет от разработки!"
```

## 🚀 Примеры

### Быстрый старт
```bash
# Настройка Ollama (локально) - API ключ не требуется
echo 'OLLAMA_MODEL=qwen3:8b' >> .env
uv run up-agents chat -p ollama "Объясни квантовые вычисления"
```

### Продвинутое использование
```bash
# Многостадийный диалог с пользовательскими настройками
uv run up-agents chat -p openai -m gpt-4 -s "Ты эксперт по Python"
# Затем вводите несколько вопросов интерактивно
```

### Сравнение провайдеров
```bash
# Тестирование одного вопроса на разных провайдерах
uv run up-agents chat -p ollama "Напиши Python функцию"
uv run up-agents chat -p openai "Напиши Python функцию"
uv run up-agents chat -p gemini "Напиши Python функцию"
```
