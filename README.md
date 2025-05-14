# Translate MCP Server

A translation server based on MCP architecture, supporting multi-language translation and text-to-speech functionality.

## Features

- Support for translation between multiple languages
- Optional text-to-speech functionality
- Built on FastAPI and MCP (Model Control Plane)
- Integration with various large language models using LiteLLM

## Installation

### Prerequisites

- Python 3.12+
- LLM API access for translation (such as OpenAI, Ollama, etc.)
- API access for speech synthesis (such as OpenAI TTS)

### Installation Steps

1. Clone the repository

```bash
git clone https://github.com/yourusername/translate-mcp-server.git
cd translate-mcp-server
```

2. Install dependencies

```bash
uv sync
```

## Configuration

Copy the `.env-example` file and rename it to `.env`, then modify the configuration as needed:

```
API_KEY=xxxx               # API key for the translation model
API_BASE=http://localhost:11434  # API base URL (e.g., when using Ollama)
MODEL='ollama/llama3:latest'     # Model to use
VOICE_API_KEY=sk-xxxx     # API key for voice service (e.g., OpenAI)
VOICE_MODEL='openai/tts-1' # Voice model
MOTHER_LANGUAGE='zh'       # Mother language setting, used for TTS processing logic
```

## Running

### Running locally

```bash
python main.py
```

By default, the server will run at `http://localhost:9988`.

### Running with Docker

```bash
docker network create mcp_network
docker compose up -d
```
By default, the server will run at `http://localhost:30100`.

NOTE: when in container want to access host use `host.docker.internal` instead of `localhost`.

## MCP Usage

```json
{
  "mcpServers": {
    "translate": {
      "url": "http://localhost:9988/mcp"
    }
  }
}
```


## Contributing

Issues and pull requests are welcome!
