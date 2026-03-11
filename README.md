[English](#english) | [中文](#中文)

# SimpleAgent

## English

A lightweight RAG Agent built with LangChain, LangGraph, Chroma, and Streamlit. It combines:

- Agent reasoning and tool selection
- RAG retrieval and grounded answering
- Business tools (weather, user info, external records, report-mode switching)

This README removes any personal or absolute paths. All links are relative, and secrets should be provided via environment variables.

### Features

- Local Chroma vector store for fast experiments
- Supports `txt` and `pdf` documents
- Encrypted PDFs are skipped during indexing
- Middleware-driven dynamic prompt switching for report mode
- Extensible tool layer to integrate real services

### Environment (Conda)

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

### Model & API Key

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

### Prepare Knowledge Data

- Place documents under [data/](data/) (`*.txt`, `*.pdf`)
- Password-protected/encrypted PDFs are not indexed and will be skipped
- Optional demo data for report scenario: place at [data/external/records.csv](data/external/records.csv)

### Start the App

Use the unified entrypoint:

```bash
python main.py
```

This will:

- Preload documents under [data/](data/) into the vector store
- Skip files already indexed via `md5.txt`
- Skip encrypted PDFs that cannot be read
- Launch the Streamlit app automatically

### Build the Vector Store Only (optional)

```bash
python rag/vector_store.py
```

This will:

- Read documents under [data/](data/)
- Split with settings from [config/chroma_config.yaml](config/chroma_config.yaml)
- Write vectors to local Chroma (directory per config)
- Track file hashes in `md5.txt` to avoid re-indexing
- Skip encrypted PDFs that cannot be read

Try some prompts in the UI:

- Knowledge: How do I maintain the robot?
- Troubleshooting: Why is suction getting weaker?
- Report mode: Generate my usage report

The system may:

- Answer directly
- Call `rag_summarize` to retrieve
- Use tools (user/weather/external records)
- Switch to a report-specific prompt when triggered

### Project Tree

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
|-- main.py
`-- README.md
```

### Modules (relative paths)

- [main.py](main.py): Unified startup entry, runs preload first and then launches Streamlit
- [app.py](app.py): Streamlit chat entry and streaming output
- [agent/react_agent.py](agent/react_agent.py): Create agent, register models, tools, middleware
- [agent/tools/agent_tools.py](agent/tools/agent_tools.py): RAG retrieval, weather, user info, external records
- [agent/tools/middle_ware.py](agent/tools/middle_ware.py): Tool monitoring, pre-model logging, report prompt switching
- [rag/rag_service.py](rag/rag_service.py): Retrieval + prompt assembly + LLM summarization
- [rag/vector_store.py](rag/vector_store.py): Load/split/embed/write to Chroma, expose retriever
- [model/factory.py](model/factory.py): Factory for chat and embedding models
- [utils/config_handler.py](utils/config_handler.py): Centralized YAML config loading
- [utils/prompt_loader.py](utils/prompt_loader.py): Read prompts per config

### Config Files

- [config/rag_config.yaml](config/rag_config.yaml): Chat model, embeddings, API key
- [config/chroma_config.yaml](config/chroma_config.yaml): DB dir, k, chunk size, overlap, file types
- [config/prompt_config.yaml](config/prompt_config.yaml): Main/RAG/report prompt paths
- [config/agent_config.yaml](config/agent_config.yaml): External business data path

### Privacy & Security

- Never commit API keys, tokens, personal paths, or sensitive data
- Prefer environment variables; if using local files, ensure they’re git-ignored
- Use relative paths only; avoid exposing usernames or drive info

### FAQ

- Q: Missing dependencies on first run?
  A: Ensure `conda activate simpleagent` and install dependencies.

- Q: Retrieval returns no results?
  A: Place documents under [data/](data/) and rerun `python main.py` or `python rag/vector_store.py`. If a PDF is encrypted, it will be skipped during indexing.

- Q: API key set but still failing?
  A: Verify the current terminal has the env var; restart the shell if needed.

### Development

- Integrate real weather/user/DB services
- Add incremental and delete capabilities to the vector store
- Add tests for prompts/tools/RAG pipeline

---

## 中文

一个基于 LangChain + LangGraph + Chroma + Streamlit 的轻量级 RAG Agent 示例，聚合了：

- Agent 推理与工具选择
- RAG 检索与基于知识的回答
- 业务工具（天气、用户信息、外部记录、报表模式切换等）

本 README 去除了所有本地绝对路径与个人信息，仅使用相对路径与可公开的配置说明。

### 功能特性

- 本地 Chroma 向量库，快速实验友好
- 支持 `txt`/`pdf` 文档检索（加密 PDF 将自动跳过，不会被索引）
- 中间件支持报表模式 Prompt 动态切换
- 工具层可扩展对接真实业务接口

### 环境准备（Conda）

建议使用 Python 3.10 及以上。

1) 创建并激活 Conda 环境

```bash
conda create -n simpleagent python=3.10 -y
conda activate simpleagent
```

2) 安装依赖（推荐）

```bash
pip install -r requirements.txt
```

或一次性安装常用依赖（与本项目匹配）：

```bash
pip install streamlit langchain langgraph langchain-core langchain-community langchain-chroma langchain-text-splitters chromadb pypdf pyyaml dashscope
```

### 模型与密钥配置

本项目默认使用阿里 DashScope 相关模型，配置项见：

- [config/rag_config.yaml](config/rag_config.yaml)

设置 API Key（任选其一）：

- Windows PowerShell：

  ```powershell
  $env:DASHSCOPE_API_KEY = "your_dashscope_api_key"
  ```

- Windows cmd：

  ```cmd
  set DASHSCOPE_API_KEY=your_dashscope_api_key
  ```

- macOS/Linux（bash/zsh）：

  ```bash
  export DASHSCOPE_API_KEY=your_dashscope_api_key
  ```

或在不提交到仓库的前提下，直接在本地修改 [config/rag_config.yaml](config/rag_config.yaml)。请勿将密钥提交到版本库。

### 准备知识库数据

- 将要检索的文档放入 [data/](data/) 目录，支持 `*.txt` 与 `*.pdf`
- 加密 PDF 不会被索引，将自动跳过
- （可选）将演示数据放在 [data/external/records.csv](data/external/records.csv)

### 构建向量库（首次或数据更新后执行）

```bash
python rag/vector_store.py
```

该脚本将：

- 读取 [data/](data/) 下的文档
- 按 [config/chroma_config.yaml](config/chroma_config.yaml) 的参数切分
- 使用本地 Chroma 写入向量库（默认目录见配置）
- 使用 `md5.txt` 记录文件指纹，避免重复索引

### 启动应用

推荐方式（包含预加载并自动启动）：

```bash
python main.py
```

仅启动应用（不预加载向量库）：

```bash
streamlit run app.py
```

浏览器打开的页面中直接对话提问，例如：

- 产品知识问答：如何维护保养扫地机器人？
- 故障排查：吸力变弱可能的原因？
- 报表模式：Generate my usage report

系统会自动决定：

- 直接由模型回答
- 调用 `rag_summarize` 进行检索
- 调用用户/天气/外部记录等工具
- 在报表模式下切换到专用 Prompt

### 目录结构

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
|-- main.py
`-- README.md
```

### 模块说明（相对路径）

- [app.py](app.py)：Streamlit 对话入口，负责聊天记录与流式输出
- [agent/react_agent.py](agent/react_agent.py)：创建 Agent，注册模型、工具和中间件
- [agent/tools/agent_tools.py](agent/tools/agent_tools.py)：RAG 检索、天气、用户信息、外部记录等工具
- [agent/tools/middle_ware.py](agent/tools/middle_ware.py)：工具监控、模型前日志、报表 Prompt 动态切换
- [rag/rag_service.py](rag/rag_service.py)：检索 + Prompt 组装 + LLM 总结
- [rag/vector_store.py](rag/vector_store.py)：加载/切分/向量化/写入 Chroma，并提供 Retriever
- [model/factory.py](model/factory.py)：统一创建聊天与向量模型
- [utils/config_handler.py](utils/config_handler.py)：集中加载 YAML 配置
- [utils/prompt_loader.py](utils/prompt_loader.py)：按配置读取 Prompt 文件

### 配置说明

- [config/rag_config.yaml](config/rag_config.yaml)：聊天模型、Embedding 模型与 API Key
- [config/chroma_config.yaml](config/chroma_config.yaml)：向量库目录、检索条数、分块大小、重叠长度、可加载文件类型等
- [config/prompt_config.yaml](config/prompt_config.yaml)：主 Prompt、RAG Prompt、报表 Prompt 路径
- [config/agent_config.yaml](config/agent_config.yaml)：外部业务数据文件路径

### 隐私与安全建议

- 不在仓库中提交任何 API Key、Token、个人路径或敏感数据
- 优先使用环境变量注入密钥；确需本地配置文件时，请确保该文件被 `.gitignore` 忽略
- 仅使用相对路径描述本地文件，避免暴露用户名和磁盘结构

### 常见问题（FAQ）

- Q: 首次启动报找不到依赖？
  A: 确认已激活 `conda activate simpleagent` 且完成依赖安装。

- Q: 检索不到数据？
  A: 确认已将文档放入 [data/](data/) 并重新执行 `python rag/vector_store.py`。

- Q: API Key 有效但仍报错？
  A: 检查当前终端是否已正确设置环境变量；重启终端再试。

### 开发与扩展

- 接入真实天气/用户中心/业务数据库接口
- 为向量库构建增加增量与删除能力
- 编写 Prompt/Tool/RAG 链路的自动化测试
