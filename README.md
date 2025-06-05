# up-agents

🤖 **Terminal agent system with support for various LLM providers**

A fully functional CLI chat interface that connects to multiple LLM providers through a unified terminal experience.

**Language versions:** [Русский](README.ru.md) | English

## 🚀 Installation

```bash
# Clone repository
git clone https://github.com/bogdan01m/up-agents.git
cd up-agents

# Install dependencies
uv sync

# Setup environment variables
cp .env.example .env
# Edit .env file and add your API keys
```

## 🔧 Configuration

Configure your LLM providers by filling the `.env` file:

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

# Ollama (local server)
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=qwen3:8b
OLLAMA_SYSTEM_PROMPT="You are helpful assistant. You are able to use tools"

# OpenRouter
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=mistralai/devstral-small:free
OPENROUTER_SYSTEM_PROMPT="You are helpful assistant. You are able to use tools"

# Custom OpenAI-compatible API
CUSTOM_OPENAI_API_KEY=your_custom_api_key_here
CUSTOM_OPENAI_BASE_URL=https://your-custom-endpoint.com/v1
CUSTOM_OPENAI_MODEL=your-model-name
CUSTOM_OPENAI_SYSTEM_PROMPT="You are helpful assistant. You are able to use tools"
```

## 📋 Usage

### Chat Commands

```bash
# Interactive chat with auto-provider selection
uv run up-agents chat

# Single query with specific provider
uv run up-agents chat -p ollama "Hello, how are you?"

# Chat with custom model and system prompt
uv run up-agents chat -p openai -m gpt-4 -s "You are a coding assistant" "Write a Python function"

# Chat without saving history
uv run up-agents chat -p ollama --no-history "Quick question"
```

### Provider Management

```bash
# List all available providers
uv run up-agents providers list

# Test provider connection
uv run up-agents providers test ollama

# Get provider information
uv run up-agents providers info openai
```

### Session Management

```bash
# List chat sessions
uv run up-agents session list

# Resume a previous session
uv run up-agents session resume <session-id>

# Export session to file
uv run up-agents session export <session-id> --format markdown
```

### Configuration

```bash
# Show current configuration
uv run up-agents config list

# Validate provider settings
uv run up-agents config validate
```

## 🤖 Supported Providers

| Provider | Models | Status |
|----------|--------|---------|
| **OpenAI** | GPT-4, GPT-3.5-turbo, GPT-4-nano | ✅ Production ready |
| **Google Gemini** | gemini-2.5-flash, gemini-pro | ✅ Production ready |
| **Mistral AI** | mistral-large-latest, mistral-medium | ✅ Production ready |
| **Ollama** | llama2, qwen3, codellama, etc. | ✅ Production ready |
| **OpenRouter** | 100+ models via unified API | ✅ Production ready |
| **Custom OpenAI** | Any OpenAI-compatible endpoint | ✅ Production ready |

### ✨ Features

- **Real LLM Integration** - Direct API calls to all providers
- **Auto Provider Selection** - Interactive provider chooser
- **Rich Terminal UI** - Beautiful formatting with markdown support
- **Environment Configuration** - Secure `.env` based setup
- **Session Management** - Chat history and resumption
- **Flexible Usage** - Single queries or interactive chat sessions

## 📁 Project Structure

```
src/
├── cli/                     # 🖥️  CLI interface
│   ├── commands/           # Chat, providers, session commands
│   ├── ui/                 # Rich terminal UI components
│   │   └── chat_engine.py  # Core chat functionality
│   └── session/           # Session management (framework)
├── llms/                   # 🧠 LLM providers
│   └── llm_call/          # Factory pattern for providers
│       ├── base_provider.py      # Base provider interface
│       ├── provider_factory.py   # Provider factory & registry
│       ├── env_config.py         # Environment configuration
│       └── llm_providers/        # Individual provider implementations
└── mcp/                   # 🔧 MCP integration (planned)
```

## 🛠️ Development

```bash
# Code formatting
uvx black .

# Linting
uvx ruff .

# Run factory pattern demo
uv run up-agents-demo

# Test chat functionality
uv run up-agents chat -p ollama "Hello from development!"
```

## 🚀 Examples

### Quick Start
```bash
# Set up Ollama (local) - no API key required
echo 'OLLAMA_MODEL=qwen3:8b' >> .env
uv run up-agents chat -p ollama "Explain quantum computing"
```

### Advanced Usage
```bash
# Multi-turn conversation with custom settings
uv run up-agents chat -p openai -m gpt-4 -s "You are a Python expert"
# Then type multiple questions interactively
```

### Provider Comparison
```bash
# Test same question across providers
uv run up-agents chat -p ollama "Write a Python function"
uv run up-agents chat -p openai "Write a Python function"
uv run up-agents chat -p gemini "Write a Python function"
```