[English](./README.md) | [中文](./README_zh.md)

# SimpleAgent

A lightweight RAG Agent built with LangChain, LangGraph, Chroma, and Streamlit. It combines:

- Agent reasoning and tool selection
- RAG retrieval and grounded answering
- Business tools (weather, user info, external records, report-mode switching)

This README removes any personal or absolute paths. All links are relative, and secrets should be provided via environment variables.

## Features

- Local Chroma vector store for fast experiments
- Supports `txt` and `pdf` documents
- Middleware-driven dynamic prompt switching for report mode
- Extensible tool layer to integrate real services

## Environment (Conda)

Recommended Python 3.10+.

1) Create and activate Conda env

```bash
conda create -n simpleagent python=3.10 -y
conda activate simpleagent
```

2) Install dependencies (recommended)

```bash
pip install -r requirements.txt
```

Or install a matching set explicitly:

```bash
pip install streamlit langchain langgraph langchain-core langchain-community langchain-chroma langchain-text-splitters chromadb pypdf pyyaml dashscope
```

## Model & API Key

DashScope model settings are defined in:

- [config/rag_config.yaml](config/rag_config.yaml)

Provide the API key in one of the following ways:

- Windows PowerShell:

  ```powershell
  $env:DASHSCOPE_API_KEY = "your_dashscope_api_key"
  ```

- Windows cmd:

  ```cmd
  set DASHSCOPE_API_KEY=your_dashscope_api_key
  ```

- macOS/Linux (bash/zsh):

  ```bash
  export DASHSCOPE_API_KEY=your_dashscope_api_key
  ```

Alternatively, edit [config/rag_config.yaml](config/rag_config.yaml) locally (do not commit secrets).

## Prepare Knowledge Data

- Place documents under [data/](data/) (`*.txt`, `*.pdf`)
- Demo data for report scenario: [data/external/records.csv](data/external/records.csv)

## Build the Vector Store (first time or after updates)

```bash
python rag/vector_store.py
```

This will:

- Read documents under [data/](data/)
- Split with settings from [config/chroma_config.yaml](config/chroma_config.yaml)
- Write vectors to local Chroma (directory per config)
- Track file hashes in `md5.txt` to avoid re-indexing

## Run the App

```bash
streamlit run app.py
```

Try some prompts in the UI:

- Knowledge: How do I maintain the robot?
- Troubleshooting: Why is suction getting weaker?
- Report mode: Generate my usage report

The system may:

- Answer directly
- Call `rag_summarize` to retrieve
- Use tools (user/weather/external records)
- Switch to a report-specific prompt when triggered

## Project Tree

```text
SimpleAgent/
|-- agent/
|   |-- react_agent.py
|   `-- tools/
|       |-- agent_tools.py
|       `-- middle_ware.py
|-- config/
|   |-- agent_config.yaml
|   |-- chroma_config.yaml
|   |-- prompt_config.yaml
|   `-- rag_config.yaml
|-- data/
|   |-- *.txt / *.pdf
|   `-- external/records.csv
|-- model/
|   `-- factory.py
|-- prompts/
|   |-- main_prompt.txt
|   |-- rag_summarize.txt
|   `-- report_prompt.txt
|-- rag/
|   |-- rag_service.py
|   `-- vector_store.py
|-- utils/
|   |-- config_handler.py
|   |-- file_handler.py
|   |-- logger_handler.py
|   |-- path_tool.py
|   `-- prompt_loader.py
|-- app.py
`-- README.md
```

## Modules (relative paths)

- [app.py](app.py): Streamlit chat entry and streaming output
- [agent/react_agent.py](agent/react_agent.py): Create agent, register models, tools, middleware
- [agent/tools/agent_tools.py](agent/tools/agent_tools.py): RAG retrieval, weather, user info, external records
- [agent/tools/middle_ware.py](agent/tools/middle_ware.py): Tool monitoring, pre-model logging, report prompt switching
- [rag/rag_service.py](rag/rag_service.py): Retrieval + prompt assembly + LLM summarization
- [rag/vector_store.py](rag/vector_store.py): Load/split/embed/write to Chroma, expose retriever
- [model/factory.py](model/factory.py): Factory for chat and embedding models
- [utils/config_handler.py](utils/config_handler.py): Centralized YAML config loading
- [utils/prompt_loader.py](utils/prompt_loader.py): Read prompts per config

## Config Files

- [config/rag_config.yaml](config/rag_config.yaml): Chat model, embeddings, API key
- [config/chroma_config.yaml](config/chroma_config.yaml): DB dir, k, chunk size, overlap, file types
- [config/prompt_config.yaml](config/prompt_config.yaml): Main/RAG/report prompt paths
- [config/agent_config.yaml](config/agent_config.yaml): External business data path

## Privacy & Security

- Never commit API keys, tokens, personal paths, or sensitive data
- Prefer environment variables; if using local files, ensure they’re git-ignored
- Use relative paths only; avoid exposing usernames or drive info

## FAQ

- Q: Missing dependencies on first run?
  A: Ensure `conda activate simpleagent` and install dependencies.

- Q: Retrieval returns no results?
  A: Place documents under [data/](data/) and rerun `python rag/vector_store.py`.

- Q: API key set but still failing?
  A: Verify the current terminal has the env var; restart the shell if needed.

## Development

- Integrate real weather/user/DB services
- Add incremental and delete capabilities to the vector store
- Add tests for prompts/tools/RAG pipeline
