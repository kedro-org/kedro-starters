# kedro-agentic-workflows

[![Powered by Kedro](https://img.shields.io/badge/powered_by-kedro-ffc900?logo=kedro)](https://kedro.org)

## 🌟 Overview

This project is a reference implementation demonstrating how `LangGraph` and `Kedro` can be combined to build agentic workflows for real-world applications.  

The use case focuses on **Customer Support Automation with Knowledge Base Integration** for an insurance company. It automates insurance customer support by combining intent detection, knowledge base retrieval, and personalized response generation, enabling more accurate and context-aware responses.

### Agentic Workflows
- **Intent Detection:** Classifies queries (general questions, new/existing claims, clarifications) and asks follow-ups if needed.  
- **Response Generation:** Retrieves relevant information from claims and documentation to generate responses, escalating unresolved issues automatically. Tool usage (e.g., KB lookup, claim retrieval/creation) is dynamically determined.

### Kedro + LangGraph
- **Kedro:** Manages data access and credentials, conversation history, sessions, and logs interactions for reproducibility and evaluation.  
- **LangGraph:** Orchestrates workflows, routing between intent detection, clarifications, tool use, and response generation.

### Required Data
- Product FAQs, help articles, and insurance manuals  
- Customer query transcripts (synthetic or anonymized)  
- Historical claims with descriptions, solutions, and statuses

## 🎯 Purpose of the Project

This project demonstrates how to build robust agentic workflows using `LangGraph` and `Kedro`. Specifically, it showcases:

* **Structuring conversational logic** – Breaking down multi-turn conversations into `LangGraph` nodes and agent states.
* **Dynamic tool selection** – Agents autonomously choose the appropriate tool (e.g., knowledge base lookup, claim creation) based on user intent.
* **Memory and state management** – Multi-turn conversation state is persisted using `LangGraph` checkpoints and `Kedro` datasets, enabling context-aware responses.
* **Knowledge base integration** – Claims and internal docs are ingested and used as tools for reasoning.
* **Secure credential handling** – Sensitive information (API keys, DB credentials) is managed securely through `Kedro` configurations.
* **Structured and reproducible outputs** – Agent responses include message content plus metadata, all logged for auditing and reproducibility.
* **Session logging** – Conversations, messages, and tool interactions are persisted to a database for auditing and analysis.
* **Observability and prompt tracking** – Integrates with external tools like `Langfuse` and `Opik` to track prompts, tool usage, and workflow execution.

Together, these elements show how to **combine pipeline orchestration, agentic reasoning, and observability** in a modular, maintainable, and reproducible workflow.

## 🤖 Agentic Workflow Design

### **Intent Detection Agent**
- A **LangGraph stateful agent**.  
- Produces an **intent label** and a **reason summary**.  
- Handles ambiguous queries via clarification loops.  

### **Response Generation Agent**
- Uses context from:  
  - `lookup_docs` – Retrieve KB answers.  
  - `get_user_claims` – Fetch user claim history.  
  - `create_claim` – Create a new claim in the DB.  
- Orchestrated by LangGraph with **conditional routing**.  
- Produces structured `ResponseOutput` with:  
  - Final message for the user  
  - Claim creation flag  
  - Escalation flag

<img src="kedro-agentic-workflows.png" alt="Use case diagram" width="800" height="700">

## 📂 Project Structure

```bash
kedro_agentic_workflows/
  ├── create_db_and_data.py                    # Script to create SQLite DB and seed with demo data
  ├── conf
  │   ├── base
  │   │   ├── catalog.yml                      # Kedro datasets catalog
  │   │   ├── genai-config.yml                 # Configuration for LMMs, prompts and tracing 
  │   │   └── parameters.yml                   # Kedro pipeline parameters (user_id, etc.)
  │   └── local
  │       └── credentials.yml                  # API keys, DB credentials
  ├── data
  │   ├── intent_detection
  │   │   └── prompts                          # Stores intent detection prompts
  │   └── response_generartion
  │       └── prompts                          # Stores response generation prompts
  └── src
      └── kedro_agentic_workflows
          ├── datasets
          │   └── sqlalchemy_dataset.py        # Custom Kedro dataset to create SQLAlchemy engines
          ├── pipelines
          │   ├── intent_detection
          │   │   ├── agent.py                 # IntentDetectionAgent (LangGraph workflow)
          │   │   ├── nodes.py                 # Kedro nodes for intent detection
          │   │   └── pipeline.py              # Kedro pipeline
          │   └── response_generation
          │       ├── agent.py                 # ResponseGenerationAgent (LangGraph workflow)
          │       ├── tools.py                 # Tool builders
          │       ├── nodes.py                 # Kedro nodes for response generation
          │       └── pipeline.py              # Kedro pipeline
          ├── utils.py                         # Shared utilities: AgentContext, KedroAgent, agent message logging
          └── settings.py                      # Global project settings
```

## 🧾 Prompt Management

This project separates prompt templates by agent type and manages them with Kedro datasets.

- **Intent Detection** → JSON prompts tracked with experimental `LangfusePromptDataset`/ `OpikPromptDataset` integrated with `Langfuse`/`Opik` datasets.
- **Response Generation** → Static `.txt` and `.yml` prompts managed via experimental `LangChainPromptDataset`.

### Intent Detection Prompts

Stored under: `data/intent_detection/prompts`

Purpose: Classify user queries into categories (general_question, claim_new, existing_claim_question, clarification) and optionally request clarification when input is ambiguous.

We use experimental Kedro datasets for observability and prompt management:

- `intent_prompt_langfuse.json` stored using [LangfusePromptDataset](https://docs.kedro.org/projects/kedro-datasets/en/kedro-datasets-9.0.0/api/kedro_datasets_experimental/langfuse.LangfusePromptDataset/) that integrates with [Langfuse](https://langfuse.com/).
- `intent_prompt_opik.json` stored using [OpikPromptDataset](https://docs.kedro.org/projects/kedro-datasets/en/kedro-datasets-9.0.0/api/kedro_datasets_experimental/opik.OpikPromptDataset/) that integrates with [Opik](https://www.comet.com/opik).

Both datasets wrap the respective observability platform’s API and allow us to manage prompts, track changes, and enable tracing/evaluation.

By default, the project uses `intent_prompt_langfuse`, but `intent_prompt_opik` can be switched in via catalog configuration and 
updating the pipeline.

```yaml
intent_prompt_langfuse:
  type: kedro_datasets_experimental.langfuse.LangfusePromptDataset
  filepath: data/intent_detection/prompts/intent_prompt_langfuse.json
  prompt_name: "intent-classifier"
  prompt_type: "chat"
  credentials: langfuse_credentials
  sync_policy: local      # local|remote|strict
  mode: langchain         # langchain|sdk

intent_prompt_opik:
  type: kedro_datasets_experimental.opik.OpikPromptDataset
  filepath: data/intent_detection/prompts/intent_prompt_opik.json
  prompt_name: "intent-classifier"
  prompt_type: "chat"
  credentials: opik_credentials
```

**Note**: Only one observability backend (Langfuse or Opik) should be active in a given run, configured via credentials

### Response Generation Prompts

Stored under: `data/response_generation/prompts`

Purpose: Generate personalized responses that combine user context, user claims data and knowledge base content and decide which tools to call to retrieve this content.

Unlike intent detection, these are static templates managed via Kedro’s experimental [LangChainPromptDataset](https://docs.kedro.org/projects/kedro-datasets/en/kedro-datasets-9.0.0/api/kedro_datasets_experimental/langchain.LangChainPromptDataset/):

- `tool.txt` – instruction for tool usage (defines how the LLM should decide when and how to call tools).
- `response.yml` – instruction for response style, tone, and overall reasoning with user-level template, receiving context (intent, claim data, docs) and instructing the model on what to answer.

Example catalog entries:

```yaml
tool_prompt:
  type: kedro_datasets_experimental.langchain.LangChainPromptDataset
  filepath: data/response_generation/prompts/tool.txt
  template: PromptTemplate
  dataset:
    type: text.TextDataset

response_prompt:
  type: kedro_datasets_experimental.langchain.LangChainPromptDataset
  filepath: data/response_generation/prompts/response.yml
  template: ChatPromptTemplate
  dataset:
    type: yaml.YAMLDataset
```

## ✏️ Tracing
This project supports observability and tracing with either `Langfuse` or `Opik`.

- `Langfuse` tracing is applied via the experimental `LangfuseTraceDataset` that provides tracing objects based on mode configuration,
enabling seamless integration with different AI frameworks and direct SDK usage. It is set as the default option for the project.
- `Opik` tracing is applied via the experimental `OpikTraceDataset` that provides tracing objects based on mode configuration,
enabling seamless integration with different AI frameworks and direct SDK usage.

Example catalog entries:

```yaml
intent_tracer_langfuse:
  type: kedro_datasets_experimental.langfuse.LangfuseTraceDataset
  credentials: langfuse_credentials
  mode: langchain    # langchain | openai | sdk

intent_tracer_opik:
  type: kedro_datasets_experimental.opik.OpikTraceDataset
  credentials: opik_credentials
  mode: openai    # langchain | openai | sdk
```

For more details see `conf/base/genai-config.yml` and [docs for `LangfuseTraceDataset`](https://docs.kedro.org/projects/kedro-datasets/en/kedro-datasets-9.0.0/api/kedro_datasets_experimental/langfuse.LangfuseTraceDataset/) and [docs for `OpikTraceDataset`](https://docs.kedro.org/projects/kedro-datasets/en/kedro-datasets-9.0.0/api/kedro_datasets_experimental/opik.OpikTraceDataset/).

`Note:` Only one tracing backend (`Langfuse` or `Opik`) should be active at a time. See `src/kedro_agentic_workflows/pipelines/intent_detection/nodes.py`.

## ⚙️ Project Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-org/kedro-agentic-workflows.git
cd kedro-agentic-workflows
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

### 3. Set Up API Credentials
Create a `credentials.yml` file and place it in the `conf/local/` directory with the following format:
```yaml
# ----------------------------
# OpenAI API credentials
# ----------------------------
openai:
  # Optional: custom API base (default is https://api.openai.com)
  base_url: "<openai-api-base>"
  api_key: "<openai-api-key>"

# ----------------------------
# Database credentials
# ----------------------------
db_credentials:
  # SQLAlchemy connection string, e.g.,
  # sqlite:///demo-db.sqlite or postgresql+psycopg2://user:pass@host:port/dbname
  # sqlite:////Projects/kedro-agentic-workflows/demo-db.sqlite
  con: "<connection-string>"

# ----------------------------
# Observability / Prompt Tracking
# ----------------------------
# NOTE: Only one of Langfuse or Opik should be used at a time.

# Langfuse credentials
langfuse_credentials:
  public_key: "<langfuse-public-key>"
  secret_key: "<langfuse-secret-key>"
  host: "<langfuse-host>"

# Opik credentials
opik_credentials:
  api_key: "<opik-api-key>"
  workspace: "<workspace-name>"
  project_name: "<project-name>"
```

## ▶️ Running the Project

### 1. Create Database and Seed Data
```bash
python create_db_and_data.py
```

This creates:
* A SQLite DB with `user`, `session`, `claim` and `message` and `doc` tables.
* Example users (IDs 1, 2, 3) with claims.
* A knowledge base with Q&A docs - `doc` table.

### 2. Run Kedro Pipeline

Start a conversation for a user:
```bash
kedro run --params user_id=3
```

Pipeline execution flow:

* Intent Detection Pipeline – classify query.
* Response Generation Pipeline – decide tool usage and generate response.

## 💬 Conversation Example

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