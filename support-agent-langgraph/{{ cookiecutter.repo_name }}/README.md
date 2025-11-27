# {{ cookiecutter.project_name }}

[![Powered by Kedro](https://img.shields.io/badge/powered_by-kedro-ffc900?logo=kedro)](https://kedro.org)

## Overview

This is your new Kedro project, which was generated using `kedro {{ cookiecutter.kedro_version }}`. 
The project is generated based on the `support-agent-langgraph` starter and provides a fully working reference architecture you can adapt for any multi-agent LLM workflow.
It demonstrates how to combine `LangGraph` and `Kedro` to build robust, production-ready agentic workflows.

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
{{ cookiecutter.kedro_version }}/
  ├── create_db_and_data.py                # Seeds demo SQLite DB
  ├── conf/
  │   ├── base/
  │   │   ├── catalog.yml                  # Dataset definitions
  │   │   ├── genai-config.yml             # LLM + tracing configuration
  │   │   └── parameters.yml               # Pipeline parameters
  │   └── local/
  │       └── credentials.yml              # API keys & DB connection
  ├── data/
  │   ├── intent_detection/prompts         # Intent prompts
  │   └── response_generation/prompts      # Response prompts
  └── src/{{ cookiecutter.kedro_version }}/
      ├── datasets/                        # Custom SQLAlchemy dataset
      ├── pipelines/
      │   ├── intent_detection/            # LangGraph + Kedro pipeline
      │   └── response_generation/         # LangGraph + Kedro pipeline
      ├── utils.py                         # AgentContext, logging helpers
      └── settings.py                      # Kedro project settings
```

### Prompt and Tool Management

Prompts for intent detection and response generation stored under `data/…/prompts`.

Managed through experimental Kedro datasets:
- [LangfusePromptDataset](https://docs.kedro.org/projects/kedro-datasets/en/kedro-datasets-9.0.0/api/kedro_datasets_experimental/langfuse.LangfusePromptDataset/)
- [OpikPromptDataset](https://docs.kedro.org/projects/kedro-datasets/en/kedro-datasets-9.0.0/api/kedro_datasets_experimental/opik.OpikPromptDataset/)
- [LangChainPromptDataset](https://docs.kedro.org/projects/kedro-datasets/en/kedro-datasets-9.0.0/api/kedro_datasets_experimental/langchain.LangChainPromptDataset/)

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

Hte above script creates:

- SQLite DB with user, claim, message, doc, session
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

## Rules and guidelines

In order to get the best out of the template:

* Don't remove any lines from the `.gitignore` file we provide
* Make sure your results can be reproduced by following a [data engineering convention](https://docs.kedro.org/en/stable/faq/faq.html#what-is-data-engineering-convention)
* Don't commit data to your repository
* Don't commit any credentials or your local configuration to your repository. Keep all your credentials and local configuration in `conf/local/`

## How to test your Kedro project

Have a look at the file `tests/test_run.py` for instructions on how to write your tests. You can run your tests as follows:

```
pytest
```

You can configure the coverage threshold in your project's `pyproject.toml` file under the `[tool.coverage.report]` section.

## How to work with Kedro and notebooks

> Note: Using `kedro jupyter` or `kedro ipython` to run your notebook provides these variables in scope: `catalog`, `context`, `pipelines` and `session`.
>
> Jupyter, JupyterLab, and IPython are already included in the project requirements by default, so once you have run `pip install -r requirements.txt` you will not need to take any extra steps before you use them.

### Jupyter
To use Jupyter notebooks in your Kedro project, you need to install Jupyter:

```
pip install jupyter
```

After installing Jupyter, you can start a local notebook server:

```
kedro jupyter notebook
```

### JupyterLab
To use JupyterLab, you need to install it:

```
pip install jupyterlab
```

You can also start JupyterLab:

```
kedro jupyter lab
```

### IPython
And if you want to run an IPython session:

```
kedro ipython
```

### How to ignore notebook output cells in `git`
To automatically strip out all output cell contents before committing to `git`, you can use tools like [`nbstripout`](https://github.com/kynan/nbstripout). For example, you can add a hook in `.git/config` with `nbstripout --install`. This will run `nbstripout` before anything is committed to `git`.

> *Note:* Your output cells will be retained locally.

## Package your Kedro project

[Further information about building project documentation and packaging your project](https://docs.kedro.org/en/stable/tutorial/package_a_project.html)
