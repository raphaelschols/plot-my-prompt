import re
from typing import TypedDict, List, Optional, Callable, Tuple, Literal
import pandas as pd
from langgraph.graph import START, END, StateGraph
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from typing_extensions import Annotated
from langgraph.checkpoint.memory import MemorySaver
from backend.model import init_llm
from backend.error_handling import return_error
from prompts.sql_generator import create_query_prompt, adjust_query_prompt
from prompts.plot_generator import create_plot_prompt, adjust_plot_prompt
from prompts.intend_detection import intent_prompt
from context.database_context import northwind_db_context
import matplotlib.pyplot as plt

# ---------------Setup
model = init_llm()
northwind_sqlite_db = SQLDatabase.from_uri("sqlite:///northwind.db")

INTENT_RE = re.compile(
    r"^(VISUALIZE|DATA_QUERY|ADJUST_QUERY|ADJUST_PLOT|VISUALIZE_EXISTING|CLARIFY)$"
)

class State(TypedDict):
    intent: str
    question: str
    query: str
    dataframe: pd.DataFrame
    answer: str
    plot_function: str
    plot: Optional[object]
    error: dict

class QueryOutput(TypedDict):
    query: Annotated[str, "Syntactically valid SQL query."]

# -----------Nodes

def detect_intent(state: State):

    try:
        has_existing_query = bool(state.get("query"))  # Perhaps remove later
        has_existing_chart = bool(state.get("plot_function"))  # Perhaps remove later

        prompt = intent_prompt.format(
            question=state["question"],
            has_existing_chart=has_existing_chart,
            has_existing_query=has_existing_query,
        )
        output = model.invoke(prompt)  # returns a Message/str depending on your SDK
        label = getattr(output, "content", output).strip().upper()

        if not INTENT_RE.match(label):
            label = "CLARIFY"

        update_state = {"intent": label}

        if label == "CLARIFY":
            update_state["answer"] = (
                "Please clarify your question. I need more specific information to assist you."
            )

        return {"intent": label}

    except Exception as e:
        return {
            "error": return_error(
                stage="detect_intent",
                code="intent_detection_failed",
                exc=e,
            )
        }


def write_query(state: State) -> str:

    if state.get("error"):
        return {}
    
    if state.get("intent") not in ("VISUALIZE", "DATA_QUERY", "ADJUST_QUERY"):
        return {}

    try:
        if state["intent"] in ("VISUALIZE", "DATA_QUERY"):
            prompt = create_query_prompt.format(
                question=state["question"],
                dialect="sqlite",
                top_k=5,
                tables_and_relationship=northwind_db_context,
            )

        elif state["intent"] == "ADJUST_QUERY":
            prev_query = state.get("query")
            if not prev_query:
                # fail fast if no prior query exists
                return {
                    "error": return_error(
                        stage="write_query",
                        code="missing_prior_query",
                        exc=None,
                        detail="Tried to adjust query but no prior query is in state.",
                    )
                }

            prompt = adjust_query_prompt.format(
                dialect="sqlite",
                top_k=5,
                tables_and_relationship=northwind_db_context,
                question=state.get("question", ""),
                existing_query=prev_query,
            )

        output = model.with_structured_output(QueryOutput).invoke(prompt)
        sql = output['query']
        if not sql:
            raise ValueError("Empty SQL from model")
        return {"query": sql}

    except Exception as e:
        return {
            "error": return_error(
                stage="write_query",
                code="query_generation_failed",
                exc=e,
            )
        }

def execute_query(state: State) -> State:
    if state.get("error"): 
        return {}
    if state.get("intent") not in ("VISUALIZE", "DATA_QUERY", "ADJUST_QUERY"):
        return {}
    
    try:
        conn = northwind_sqlite_db._engine.raw_connection() 
        df = pd.read_sql_query(state["query"], conn) 
        conn.close()
        # A tiny auto-answer for DATA_QUERY flows
        if state.get("intent") in ("DATA_QUERY", "ADJUST_QUERY"):
            summary = f"Query returned {len(df)} rows. Showing first 5."
            return {"dataframe": df, "answer": summary}
        return {"dataframe": df}
    
    except Exception as e:
        return {
            "error": return_error(
                stage="execute_query",
                code="query_execution_failed",
                exc=e,
                detail=f"Query: {state.get('query','')}",
            )
        }

def write_plot_function(state: State) -> State:
    if state.get("error"): 
        return {}
    intent = state.get("intent", "")
    if intent not in ("VISUALIZE", "ADJUST_PLOT", "VISUALIZE_EXISTING"):
        return {}
    
    try:
        df = state.get("dataframe")

        if intent in ("VISUALIZE", "VISUALIZE_EXISTING"):
            formatted = create_plot_prompt.format(
                DataFrame=(df.head(5) if df is not None else "None"),
                Question=state.get("question", ""),
            )
        elif intent == "ADJUST_PLOT":
            formatted = adjust_plot_prompt.format(
                DataFrame=(df.head(5) if df is not None else "None"),
                Question=state.get("question", ""),
                ExistingPlotFunction=state.get("plot_function", ""),
            )

        raw = model.invoke(formatted)
        code = getattr(raw, "content", str(raw))

        return {"plot_function": code}

    except Exception as e:
        return {
            "error": return_error(
                stage="write_plot_function",
                code="plot_generation_failed",
                exc=e,
                detail=state.get("question", ""),
            )
        }

def execute_plot_function(state: State) -> str:
    """
    This function executes the generated plot function and returns the plot.
    """
    if state.get("error"): 
        return {}
    intent = state.get("intent", "")
    if intent not in ("VISUALIZE", "ADJUST_PLOT", "VISUALIZE_EXISTING"):
        return {}
    
    try:

        local_vars = {}

        # Execute the plot function code
        exec(state["plot_function"], globals(), local_vars)

        generate_plot = local_vars.get("generate_plot")

        return {
            "plot": (
                generate_plot(state["dataframe"]) if callable(generate_plot) else None
            )
        }
    except Exception as e:
        return {
            "error": return_error(
                stage="execute_plot_function",
                code="plot_execution_failed",
                exc=e,
                detail=f"Plot Function: {state['plot_function']}",
            )
        }

# ---------- Graph & runner ----------
class AssistantGraph: 
    def __init__(self): 
        builder = StateGraph(State).add_sequence(
            [ detect_intent, 
              write_query, 
              execute_query, 
              write_plot_function, 
              execute_plot_function]) 
        builder.add_edge(START, "detect_intent") 
        self.app = builder.compile()
        self.sessions: dict[str, State] = {}
        
    def ask(self, question: str, thread_id: str = "default") -> State: 
        prior = self.sessions.get(thread_id, {})
        inputs = dict(prior)

        # 🟢 If the question changed, clear only the fields that should be recomputed
        if question != prior.get("question"):
            for k in ("intent", "query", "dataframe", "answer", "plot_function", "plot", "error"):
                inputs.pop(k, None)

        inputs["question"] = question
        state = dict(prior)

        # Always clears error state if the question changed
        state.pop("error", None)
        
        for event in self.app.stream(inputs):
            for _, update in event.items():
                if isinstance(update, dict):
                    state.update(update)
                    self.sessions[thread_id] = state

        return state
