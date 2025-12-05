# {{ cookiecutter.project_name }}

[![Powered by Kedro](https://img.shields.io/badge/powered_by-kedro-ffc900?logo=kedro)](https://kedro.org)

## How to use this starter

This Kedro starter is intentionally more feature-rich than typical Kedro templates. Instead of a minimal scaffold, 
it provides a complete end-to-end working GenAI support-agent system built with 
`Kedro` and `LangGraph` + LLM tooling, prompt versioning and full DB workflow.

You can use it in two ways:

1. Run the template end-to-end immediately

This project includes a runnable example support-agent — no additional setup required beyond credentials.

```sh
pip install -r requirements.txt
python create_db_and_data.py
kedro run --params user_id=<id>
```

This will launch an interactive agent workflow: Intent Agent → Retrieval → Response Agent → Final output to user

2. Adapt it as a starting point for your own agentic workflow

Each component (agents, prompts, tools, DB, tracing) is documented within the code and below.
We recommend exploring the files inside the project as they inline comments explaining purpose and modification instructions, so you can quickly adapt them to your own use-case.

## Overview

The template implements an automated insurance customer support assistant powered by:
- Intent Detection Agent – classifies queries and handles clarifications
- Response Generation Agent – retrieves knowledge base content, fetches user claims, creates new claims, and generates final responses
- Kedro – manages configuration, datasets, credentials, logging, and reproducibility
- LangGraph – orchestrates the multi-node conversational workflow with stateful agents
- Langfuse/Opik - support prompt and trace tracking

<img src="images/workflow-diagram.png" alt="Workflow design" width="800" height="700">

## Features

### Project Structure

```bash
{{ cookiecutter.repo_name }}/
  ├── create_db_and_data.py                # Seeds demo SQLite DB
  ├── conf/
  │   ├── base/
  │   │   ├── catalog.yml                  # Dataset definitions
  │   │   ├── catalog_genai.yml            # LLM + tracing configuration
  │   │   └── parameters.yml               # Pipeline parameters
  │   └── local/
  │       └── credentials.yml              # API keys & DB connection
  ├── data
  │   ├── intent_detection
  │   │   └── prompts
  │   │       ├── intent_prompt_langfuse.json   # Example intent-classification prompt versioned via Langfuse
  │   │       └── intent_prompt_opik.json       # Example intent-classification prompt versioned via Opik
  │   └── response_generation
  │       └── prompts
  │           ├── response.yml                  # Core agent response template (retrieval + claims + output formatting)
  │           └── tool.txt                      # System prompt describing available tools + function call format
  └── src/{{ cookiecutter.python_package }}/
      ├── datasets/
      │   └── sqlalchemy_dataset.py        # Custom `SQLAlchemyEngineDataset` to create SQLAlchemy engines to perform write operations
      ├── pipelines/
      │   ├── intent_detection/            # LangGraph + Kedro pipeline
      │   └── response_generation/         # LangGraph + Kedro pipeline
      ├── utils.py                         # AgentContext, logging helpers
      └── settings.py                      # Kedro project settings
```

### Database Architecture

This starter ships with a demo SQLite database created using `create_db_and_data.py`. It includes tables for:
- users - Basic user identity for conversation context
- claims - User claim data for read/write interactions
- messages - Stores assistant and user message history
- sessions - Allows multi-turn conversation continuity
- knowledge base docs - Retrieval source documents

Demo database is used with the core `pandas.SQLTableDataset` and `pandas.SQLQueryDataset` to read the user info and retrieve KB question-answer pairs and 
custom `SQLAlchemyEngineDataset` for execution of insert/update queries when tools calling and logging.

**Use the DB setup if you need:**

- stateful agent memory across sessions
- ability to log conversations, tool calls, model outputs
- updating user data (claims, tickets, order records, etc.)
- retrieval-augmented workflows (knowledge base + context)

**You can skip the DB if your system is:**

- pure RAG with no persistent sessions
- read-only knowledge base with no transactional logic
- single-shot response apps (no memory)

To disable it, simply remove or replace SQL datasets and the SQLite connection.

### Prompt Management and TracingPrompt Management and Tracing

This project separates prompt templates by agent type and manages them with Kedro datasets.

- **Intent Detection** - JSON prompts tracked with experimental `LangfusePromptDataset`/ `OpikPromptDataset` integrated with `Langfuse`/`Opik` datasets.
- **Response Generation** - Static `.txt` and `.yml` prompts managed via experimental `LangChainPromptDataset`.

This project also supports observability and tracing with either `Langfuse` or `Opik`:
- `Langfuse` tracing is applied via the experimental `LangfuseTraceDataset` that provides tracing objects based on mode configuration and is set as the default option for the project.
- `Opik` tracing is applied via the experimental `OpikTraceDataset` that provides tracing objects based on mode configuration,
enabling seamless integration with different AI frameworks and direct SDK usage.

For more details see the following datasets:
- [LangfusePromptDataset](https://docs.kedro.org/projects/kedro-datasets/en/kedro-datasets-9.0.0/api/kedro_datasets_experimental/langfuse.LangfusePromptDataset/)
- [OpikPromptDataset](https://docs.kedro.org/projects/kedro-datasets/en/kedro-datasets-9.0.0/api/kedro_datasets_experimental/opik.OpikPromptDataset/)
- [LangChainPromptDataset](https://docs.kedro.org/projects/kedro-datasets/en/kedro-datasets-9.0.0/api/kedro_datasets_experimental/langchain.LangChainPromptDataset/)
- [LangfuseTraceDataset](https://docs.kedro.org/projects/kedro-datasets/en/kedro-datasets-9.0.0/api/kedro_datasets_experimental/langfuse.LangfuseTraceDataset/)
- [OpikTraceDataset](https://docs.kedro.org/projects/kedro-datasets/en/kedro-datasets-9.0.0/api/kedro_datasets_experimental/opik.OpikTraceDataset/)

Only **one** observability provider (`Langfuse` or `Opik`) should be active per run.

## Getting Started

To create a project based on this starter, ensure you have installed Kedro into a virtual environment. Then use the following command:

```sh
pip install kedro
kedro new --starter=support-agent-langgraph
```

After the project is created, navigate to the newly created project directory:

```sh
cd <my-project-name>  # change directory 
```

Install the required dependencies:

```sh
pip install -r requirements.txt
```

Create `conf/local/credentials.yml` and configure credentials:

```yaml
openai:
  api_key: "<openai-api-key>"
  base_url: "<openai-api-base>"

db_credentials:
  # sqlite:////Projects/your-project-name/demo-db.sqlite
  con: "<sqlalchemy-connection-string>"

# Choose ONE observability backend
langfuse_credentials:
  public_key: "<key>"
  secret_key: "<key>"
  host: "<host>"

opik_credentials:
  api_key: "<opik-api-key>"
  workspace: "<workspace>"
  project_name: "<project>"
```

Initialize demo data:
```sh
python create_db_and_data.py
```

The above script creates:

- SQLite DB with user, claim, message, doc, session further used via custom `SQLAlchemyEngineDataset` and core `SQL` datasets
- Example users and synthetic claims
- Knowledge base entries

Start a conversation for a user:

```sh
kedro run --params user_id=3
```

## Conversation Example

```bash
Hi Charlie! 👋 How can I help you today? You can ask me a question, open a new claim, or follow up on the existing one.

================================ Human Message =================================
show me all my claims

================================== Ai Message ==================================
Intent classified: existing_claim_question
Reason: The user is asking to see all their claims, which implies they are inquiring about existing claims.

================================== Ai Message ==================================
Tool Calls: get_user_claims (call_6hZXCx7QZBDx0qPCSosDiZYO) Call ID: call_6hZXCx7QZBDx0qPCSosDiZYO Args: user_id: 3 

================================= Tool Message =================================
Name: get_user_claims [{"id": 1, "title": "Car Accident Claim", "status": "Pending", "problem": "User was involved in a minor car accident and submitted documents.", "solution": null, "created_at": "2025-09-04 14:11:49"}, {"id": 2, "title": "Laptop Damage Claim", "status": "Resolved", "problem": "Laptop stopped working after water damage.", "solution": "Claim approved. User received reimbursement of $800.", "created_at": "2025-09-04 14:11:49"}]

================================== Ai Message ==================================
Thank you for reaching out.

Based on the information we found regarding your issue: You have two claims. The "Car Accident Claim" is currently pending, and the "Laptop Damage Claim" has been resolved with a reimbursement of $800.

If you have any further questions, feel free to ask.
```
