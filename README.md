Plot My Prompt

Turn natural-language prompts into data queries and visualizations.
This project parses a user prompt, generates/executes a data query, and returns either a table, a plot, or both—driven by intent classification.

At a glance

Input: a user question/prompt

Processing: intent detection → optional SQL generation → data retrieval → optional plotting

Output: SQL, dataframe preview, and/or charts

Table of Contents

Scope & Goals

Architecture

Key Components

Data Sources

Setup

Run

Usage Examples

Configuration

Project Structure

Roadmap

Contributing

License

Scope & Goals

What it does

Converts a plain-English prompt into:

an SQL query (when applicable)

a tabular result (dataframe)

a visualization (Plotly or Matplotlib)

What it doesn’t (yet) do

Authenticate to external databases out of the box

Guarantee perfect SQL for arbitrary schemas (uses heuristics / LLM logic)

Perform production-grade caching/observability

Goal: fast, explainable prompt→analysis loops for demos, prototyping, and internal data exploration.

Architecture

App entry (app.py)
Orchestrates request handling and UI messaging (e.g., show SQL → show dataframe → show plot).

Backend graph (backend/)

AssistantGraph: state machine/graph that runs the analysis pipeline (intent, query, visualize).

Intent values like CLARIFY, DATA_QUERY, VISUALIZE_EXISTING, VISUALIZE, etc., decide how the UI responds.

Prompts (prompts/)
Reusable system/user prompts (e.g., intent classification, SQL generation, chart spec).

Context (context/)
Schema hints, field descriptions, and helper metadata for better SQL/plot generation.

Local data (northwind.db)
A lightweight SQLite DB (Northwind) for quick end-to-end examples.

Key Components

AssistantGraph (in backend/graph.py)
The “brain” that:

Detects intent from the user message

Builds SQL (when needed)

Executes against the local DB / data source

Builds a Plotly figure or Matplotlib figure when requested

UI messaging (in app.py)

Shows SQL in a code block

Renders Dataframe in a side panel

Renders Plotly or Pyplot charts in a side panel

Falls back with friendly messages on unknown intent or errors

Data Sources

Default: northwind.db (SQLite) included for convenience.

Extend: point to your own SQLite file, or adapt execution to other engines (DuckDB, Postgres, etc.).

TODO: Add instructions if you plan to support other engines.

Setup
Prerequisites

Python 3.10+ (recommended)

(Optional) A virtual environment

Install
git clone git@github.com:raphaelschols/plot-my-prompt.git
cd plot-my-prompt

# Create & activate a virtual env (recommended)
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install deps
pip install -r requirements.txt


If you’ll edit/distribute as a package, you can also:
pip install -e . (uses setup.py)

Run

The app exposes a conversational UI that returns SQL, tables, and charts depending on detected intent.

Option A — Run as a standard Python app
python app.py

Option B — (If using Chainlit)

If app.py is a Chainlit entrypoint, you can run:

# If Chainlit is in requirements.txt, it’s already installed
chainlit run app.py -w


Note: If you see missing logo errors or UI assets not found, ensure your public/ assets and/or chainlit.toml are set correctly.

Usage Examples

Ask questions like:

“Show sales by category for 1997.”

“Top 10 customers by total order value.”

“Plot monthly order count as a line chart.”

“Bar chart of revenue by region, last 12 months.”

What you’ll see

For query-type intents: SQL block + Result dataframe

For visualization intents: Chart/Plot in the sidebar

For ambiguous asks: a clarification prompt

Configuration

Prompts: edit templates in prompts/ to change the tone or logic for intent detection / SQL / plotting.

Context: update context/ with your schema, field aliases, and examples to boost SQL accuracy.

DB Path: point query execution to another SQLite file or backend in the backend graph code.

UI Settings: (if using Chainlit) configure chainlit.toml (logo, name, etc.).

Project Structure
plot-my-prompt/
├─ backend/
│  ├─ graph.py                 # AssistantGraph: core pipeline (intent → query → plot)
│  └─ ...                      # helpers, model wrappers, execution utilities
├─ context/
│  └─ ...                      # schema hints, field descriptions, example mappings
├─ prompts/
│  └─ ...                      # LLM prompts for intent/SQL/visualization
├─ app.py                      # Entry point / UI logic
├─ northwind.db                # Local SQLite demo database
├─ requirements.txt            # Python dependencies
├─ setup.py                    # Packaging config (editable install)
└─ README.md                   # (this file)


If some filenames differ (e.g., backend/graph.py is named slightly differently), adjust path references accordingly.
