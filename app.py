import chainlit as cl
from matplotlib.figure import Figure
from backend.graph import AssistantGraph
import json

graph = AssistantGraph()

def _history_elements():
    qs = cl.user_session.get("questions", [])
    if not qs:
        md = "_No questions yet._"
    else:
        md = "\n".join(f"{i+1}. {q}" for i, q in enumerate(qs[-50:]))
    return [cl.Text(name="Chat History", content=md)]

@cl.on_chat_start
async def on_start():
    cl.user_session.set("questions", [])
    await cl.ElementSidebar.set_title("Chat History")
    await cl.ElementSidebar.set_elements(_history_elements())

@cl.on_message
async def main(message: cl.Message):
    # Update history sidebar
    qs = cl.user_session.get("questions", [])
    qs.append(message.content.strip())
    cl.user_session.set("questions", qs)
    await cl.ElementSidebar.set_elements(_history_elements())

    # Run graph
    state = graph.ask(message.content)
    intent = state.get("intent", "")

    # --- intent-driven display ---
    if intent == "CLARIFY":
        await cl.Message("Please clarify your question.", parent_id=message.id).send()

    elif intent in ("DATA_QUERY", "ADJUST_QUERY"):
        # Show SQL + DataFrame only (no plot)
        if state.get("query"):
            await cl.Message(
                f"**SQL:**\n```sql\n{state['query']}\n```",
                parent_id=message.id
            ).send()

        df = state.get("dataframe")
        if df is not None:
            await cl.Message(
                content="Open **Result** on the left.",   # 👈 added hint
                elements=[cl.Dataframe(name="Result", data=df, display="side")],
                parent_id=message.id
            ).send()

    elif intent in ("VISUALIZE_EXISTING", "ADJUST_PLOT"):
        # Plot only
        plot_obj = state.get("plot")
        if hasattr(plot_obj, "to_dict"):
            await cl.Message(
                content="Open **Chart** on the left.",
                elements=[cl.Plotly(name="Chart", figure=plot_obj, display="side")],
                parent_id=message.id
            ).send()
        elif isinstance(plot_obj, Figure):
            await cl.Message(
                content="Open **Plot** on the left.",
                elements=[cl.Pyplot(name="Plot", figure=plot_obj, display="side")],
                parent_id=message.id
            ).send()
        else:
            await cl.Message("No plot generated.", parent_id=message.id).send()

    elif intent == "VISUALIZE":
        # Full flow: SQL + DF + Plot
        if state.get("query"):
            await cl.Message(
                f"**SQL:**\n```sql\n{state['query']}\n```",
                parent_id=message.id
            ).send()

        df = state.get("dataframe")
        if df is not None:
            await cl.Message(
                content="Open **Result** on the left.",   # 👈 added hint
                elements=[cl.Dataframe(name="Result", data=df, display="side")],
                parent_id=message.id
            ).send()

        plot_obj = state.get("plot")
        if hasattr(plot_obj, "to_dict"):
            await cl.Message(
                content="Open **Chart** on the left.",
                elements=[cl.Plotly(name="Chart", figure=plot_obj, display="side")],
                parent_id=message.id
            ).send()
        elif isinstance(plot_obj, Figure):
            await cl.Message(
                content="Open **Plot** on the left.",
                elements=[cl.Pyplot(name="Plot", figure=plot_obj, display="side")],
                parent_id=message.id
            ).send()
        else:
            await cl.Message("No plot generated.", parent_id=message.id).send()

    else:
        # unknown intent fallback
        await cl.Message("I couldn't determine intent.", parent_id=message.id).send()

    # --- always show state if error ---
    if state.get("error"):
        await cl.Message(
            content="**Conversation State (debug):**\n```json\n"
                    + json.dumps(graph.sessions.get("default", {}), indent=2, default=str)
                    + "\n```",
            parent_id=message.id
        ).send()
