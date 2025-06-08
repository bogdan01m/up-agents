# mcode

🤖 **Terminal agent system with support for various LLM providers**

A powerful CLI chat interface that connects to multiple LLM providers through a unified terminal experience. Features real-time chat, session management, and extensible provider architecture.

**Language versions:** [Русский](README.ru.md) | English

## 🚀 Installation

### Global Installation (Recommended)

```bash
# Clone repository
git clone https://github.com/bogdan01m/mcode.git
cd mcode

# Install globally with uv
uv tool install .

# Initialize global configuration (creates ~/.mcode/.env)
mcode config init

# Edit global config and add your API keys
# The config file will be created at ~/.mcode/.env
```

**That's it!** Now you can use `mcode` from anywhere:

```bash
mcode chat                    # Interactive chat with auto-provider selection
mcode chat -p ollama "Hello" # Quick question with specific provider
```

### Development Installation

```bash
# Clone repository
git clone https://github.com/bogdan01m/mcode.git
cd mcode

# Install dependencies
uv sync

# Use with uv run (for development)
uv run mcode --help
```

## 🔧 Configuration

### Global Configuration (Recommended)

After installation, run `mcode config init` to create a global configuration template at `~/.mcode/.env`. This config will be used from any directory.

```bash
mcode config init    # Creates ~/.mcode/.env with template
mcode config list    # Shows config file locations
```

Edit `~/.mcode/.env` and uncomment/configure your API keys:

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

### Local Project Configuration (Optional)

You can override global settings for specific projects by creating a local `.env` file in your project directory. Local configuration takes precedence over global configuration.

```bash
# In your project directory
echo 'OPENAI_MODEL=gpt-4-turbo' > .env
# This will override the global OPENAI_MODEL setting for this project only
```

## 📋 Usage

### Chat Commands

```bash
# Interactive chat with auto-provider selection
mcode chat

# Single query with specific provider
mcode chat -p ollama "Hello, how are you?"

# Chat with custom model and system prompt
mcode chat -p openai -m gpt-4 -s "You are a coding assistant" "Write a Python function"

# Chat without saving history
mcode chat -p ollama --no-history "Quick question"
```

### Provider Management

```bash
# List all available providers
mcode providers list

# Test provider connection
mcode providers test ollama

# Get provider information
mcode providers info openai
```

### Session Management

```bash
# List chat sessions
mcode session list

# Resume a previous session
mcode session resume <session-id>

# Export session to file
mcode session export <session-id> --format markdown
```

### Configuration Management

```bash
# Initialize global configuration
mcode config init

# Show configuration file paths
mcode config list

# Validate provider settings
mcode config validate
```

## 🤖 Supported Providers

| Provider | Models | Status | Notes |
|----------|--------|---------|-------|
| **OpenAI** | All available provider models | ✅ Chat-only | Full tool-calling support |
| **Google Gemini** | All available provider models | ✅ Chat-only | Full tool-calling support |
| **Mistral AI** | All available provider models | ✅ Chat-only | Full tool-calling support |
| **Ollama** | All locally installed models | ✅ Chat-only | Tool-calling depends on model |
| **OpenRouter** | 100+ models via unified API | ✅ Chat-only | Tool-calling depends on model |
| **Custom OpenAI** | Any OpenAI-compatible endpoint | ✅ Chat-only | Tool-calling depends on model |

> **MCP Note:** With planned MCP protocol integration, there may be limitations with models that don't support tool-calling. Modern models (GPT-4, Gemini 2.5, Mistral Large) have full support.

### ✨ Features

- **🤖 Real LLM Integration** - Direct API calls to all major providers
- **⚡ Auto Provider Selection** - Interactive provider chooser with status indicators
- **🎨 Rich Terminal UI** - Beautiful formatting with markdown and syntax highlighting
- **🔐 Global Configuration** - Secure environment-based setup with global and local configs
- **📝 Session Management** - Persistent chat history with resume and export capabilities
- **🚀 Flexible Usage** - Single queries, interactive sessions, or custom model parameters
- **🔧 Extensible Architecture** - Factory pattern for easy provider addition
- **📦 Global Installation** - Install once, use anywhere on your system

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

# Run factory pattern demo (after global install)
mcode-demo

# Test chat functionality
mcode chat -p ollama "Hello from development!"

# Or use development mode
uv run mcode chat -p ollama "Hello from development!"
```

## 🚀 Examples

### Quick Start
```bash
# Install and initialize
uv tool install .
mcode config init

# Set up Ollama (local) - no API key required
echo 'OLLAMA_MODEL=qwen3:8b' >> ~/.mcode/.env
mcode chat -p ollama "Explain quantum computing"
```

### Advanced Usage
```bash
# Multi-turn conversation with custom settings
mcode chat -p openai -m gpt-4 -s "You are a Python expert"
# Then type multiple questions interactively
```

### Provider Comparison
```bash
# Test same question across providers
mcode chat -p ollama "Write a Python function"
mcode chat -p openai "Write a Python function"
mcode chat -p gemini "Write a Python function"
```