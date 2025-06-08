# mcode

🤖 **Терминальная агентная система с поддержкой различных LLM провайдеров**

Мощный CLI чат-интерфейс, который подключается к множеству LLM провайдеров через единый терминальный интерфейс. Включает чат в реальном времени, управление сессиями и расширяемую архитектуру провайдеров.

**Языковые версии:** Русский | [English](README.md)

## 🚀 Установка

### Глобальная установка (Рекомендуется)

```bash
# Клонирование репозитория
git clone https://github.com/bogdan01m/mcode.git
cd mcode

# Глобальная установка с uv
uv tool install .

# Инициализация глобальной конфигурации (создает ~/.mcode/.env)
mcode config init

# Редактируйте глобальную конфигурацию и добавьте ваши API ключи
# Файл конфигурации будет создан в ~/.mcode/.env
```

**Вот и всё!** Теперь вы можете использовать `mcode` из любой директории:

```bash
mcode chat                    # Интерактивный чат с автовыбором провайдера
mcode chat -p ollama "Привет" # Быстрый вопрос с конкретным провайдером
```

### Установка для разработки

```bash
# Клонирование репозитория
git clone https://github.com/bogdan01m/mcode.git
cd mcode

# Установка зависимостей
uv sync

# Использование с uv run (для разработки)
uv run mcode --help
```

## 🔧 Конфигурация

### Глобальная конфигурация (Рекомендуется)

После установки запустите `mcode config init` для создания шаблона глобальной конфигурации в `~/.mcode/.env`. Эта конфигурация будет использоваться из любой директории.

```bash
mcode config init    # Создает ~/.mcode/.env с шаблоном
mcode config list    # Показывает пути к файлам конфигурации
```

Отредактируйте `~/.mcode/.env` и раскомментируйте/настройте ваши API ключи:

```bash
# OpenAI
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
OPENAI_SYSTEM_PROMPT="You are helpful assistant. You are able to use tools"

# Google Gemini
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash-exp
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

### Локальная конфигурация проекта (Опционально)

Вы можете переопределить глобальные настройки для конкретных проектов, создав локальный файл `.env` в директории проекта. Локальная конфигурация имеет приоритет над глобальной.

```bash
# В директории вашего проекта
echo 'OPENAI_MODEL=gpt-4-turbo' > .env
# Это переопределит глобальную настройку OPENAI_MODEL только для этого проекта
```

## 📋 Использование

### Команды чата

```bash
# Интерактивный чат с автовыбором провайдера
mcode chat

# Одиночный запрос с конкретным провайдером
mcode chat -p ollama "Привет, как дела?"

# Чат с пользовательской моделью и системным промптом
mcode chat -p openai -m gpt-4 -s "Ты помощник по кодингу" "Напиши Python функцию"

# Чат без сохранения истории
mcode chat -p ollama --no-history "Быстрый вопрос"
```

### Управление провайдерами

```bash
# Список всех доступных провайдеров
mcode providers list

# Тестирование соединения с провайдером
mcode providers test ollama

# Информация о провайдере
mcode providers info openai
```

### Управление сессиями

```bash
# Список чат-сессий
mcode session list

# Возобновление предыдущей сессии
mcode session resume <session-id>

# Экспорт сессии в файл
mcode session export <session-id> --format markdown
```

### Управление конфигурацией

```bash
# Инициализация глобальной конфигурации
mcode config init

# Показать пути к файлам конфигурации
mcode config list

# Проверить настройки провайдеров
mcode config validate
```

## 🤖 Поддерживаемые провайдеры

| Провайдер | Модели | Статус | Примечания |
|----------|--------|---------|------------|
| **OpenAI** | Все доступные модели провайдера | ✅ Только чат | Полная поддержка tool-calling |
| **Google Gemini** | Все доступные модели провайдера | ✅ Только чат | Полная поддержка tool-calling |
| **Mistral AI** | Все доступные модели провайдера | ✅ Только чат | Полная поддержка tool-calling |
| **Ollama** | Все локально установленные модели | ✅ Только чат | Tool-calling зависит от модели |
| **OpenRouter** | 100+ моделей через единый API | ✅ Только чат | Tool-calling зависит от модели |
| **Custom OpenAI** | Любая OpenAI-совместимая точка | ✅ Только чат | Tool-calling зависит от модели |

> **Примечание по MCP:** При планируемой интеграции MCP протокола могут возникнуть ограничения с моделями, которые не поддерживают tool-calling. Современные модели (GPT-4, Gemini 2.5, Mistral Large) имеют полную поддержку.

### ✨ Возможности

- **🤖 Реальная интеграция с LLM** - Прямые API вызовы ко всем основным провайдерам
- **⚡ Автовыбор провайдера** - Интерактивный выбор провайдера с индикаторами статуса
- **🎨 Красивый терминальный интерфейс** - Поддержка markdown и подсветки синтаксиса
- **🔐 Глобальная конфигурация** - Безопасная настройка на основе окружения с глобальными и локальными конфигурациями
- **📝 Управление сессиями** - Постоянная история чатов с возможностью возобновления и экспорта
- **🚀 Гибкое использование** - Одиночные запросы, интерактивные сессии или пользовательские параметры модели
- **🔧 Расширяемая архитектура** - Factory паттерн для легкого добавления провайдеров
- **📦 Глобальная установка** - Установить один раз, использовать в любом месте системы

## 📁 Структура проекта

```
src/
├── cli/                     # 🖥️  CLI интерфейс
│   ├── commands/           # Команды: chat, providers, session
│   ├── ui/                 # Компоненты терминального UI
│   │   └── chat_engine.py  # Основная функциональность чата
│   └── session/           # Управление сессиями (фреймворк)
├── llms/                   # 🧠 LLM провайдеры
│   └── llm_call/          # Factory паттерн для провайдеров
│       ├── base_provider.py      # Базовый интерфейс провайдера
│       ├── provider_factory.py   # Фабрика и реестр провайдеров
│       ├── env_config.py         # Конфигурация окружения
│       └── llm_providers/        # Реализации отдельных провайдеров
└── mcp/                   # 🔧 MCP интеграция (планируется)
```

## 🛠️ Разработка

```bash
# Форматирование кода
uvx black .

# Линтинг
uvx ruff .

# Запуск демо Factory паттерна (после глобальной установки)
mcode-demo

# Тестирование функциональности чата
mcode chat -p ollama "Привет от разработки!"

# Или использование режима разработки
uv run mcode chat -p ollama "Привет от разработки!"
```

## 🚀 Примеры

### Быстрый старт
```bash
# Установка и инициализация
uv tool install .
mcode config init

# Настройка Ollama (локально) - API ключ не требуется
echo 'OLLAMA_MODEL=qwen3:8b' >> ~/.mcode/.env
mcode chat -p ollama "Объясни квантовые вычисления"
```

### Продвинутое использование
```bash
# Многостадийный диалог с пользовательскими настройками
mcode chat -p openai -m gpt-4 -s "Ты эксперт по Python"
# Затем вводите несколько вопросов интерактивно
```

### Сравнение провайдеров
```bash
# Тестирование одного вопроса на разных провайдерах
mcode chat -p ollama "Напиши Python функцию"
mcode chat -p openai "Напиши Python функцию"
mcode chat -p gemini "Напиши Python функцию"
```
