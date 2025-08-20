# Plot My Prompt

Turn natural-language prompts into data queries and visualizations.  
This project parses a user prompt, generates/executes a data query, and returns either a table, a plot, or both—driven by intent classification.

---

## 📌 At a glance
- **Input:** natural-language question  
- **Processing:** intent detection → SQL (optional) → data retrieval → visualization (optional)  
- **Output:** SQL, dataframe, and/or charts  

---

## 🎯 Scope & Goals

- Convert a plain-English prompt into:  
  - **SQL query**  
  - **Tabular result**  
  - **Visualization** (Plotly / Matplotlib)  

👉 Goal: fast, explainable prompt→analysis loops for demos, prototyping, and exploration.  

---

## 🏗 Architecture

- **`app.py`** → orchestrates request handling and UI  
- **`backend/graph.py`** → state machine for intent, query, visualization  
- **`prompts/`** → prompt templates for intent, SQL, charts  
- **`context/`** → schema hints and metadata  
- **`northwind.db`** → demo SQLite database  

---

## ⚙️ Setup

**Prerequisites:** Python 3.10+, virtual environment recommended  

```bash
git clone git@github.com:raphaelschols/plot-my-prompt.git
cd plot-my-prompt

python setup.py

▶️ Run
chainlit run app.py

💡 Example Prompts

“Top 10 customers by total order value.”

“Plot monthly order count as a line chart.”

pip install -r requirements.txt
