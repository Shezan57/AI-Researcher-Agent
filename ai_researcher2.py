# Stepl: Define state
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from typing import Annotated, Literal
from arxiv_tool import arxiv_search
from read_pdf import read_pdf
from write_pdf import render_latex_pdf
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from initial_prompt import INITIAL_PROMPT
from dotenv import load_dotenv
load_dotenv()


class State(TypedDict):
    messages: Annotated[list, add_messages]

# step2 Define ToolNode & Tools
tools = [read_pdf, render_latex_pdf, arxiv_search]
tool_node = ToolNode(tools)

# Step3: setup LLM (only bind tools once)
model = ChatOpenAI(model="gpt-4o", temperature=0.7).bind_tools(tools)


# Setup4: Setup graph
def call_model(state: State):
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}

def should_continue(state: State) -> Literal["tools", END]:
    messages = state["messages"][-1]
    if messages.tool_calls:
        return "tools"
    return END

workflow = StateGraph(State)
workflow.add_node("agent",call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

checkpointer = MemorySaver()
config = {"configurable": {"thread_id": 112}}

graph = workflow.compile(checkpointer=checkpointer)


def print_stream(stream):
    for s in stream:
        messages = s["messages"][-1]
        print(f"Messages recived: {messages.content}...")
        messages.pretty_print()

# while True:
#     user_input = input("User: ")
#     if user_input:
#         messages = [
#             {"role": "system", "content":INITIAL_PROMPT},
#             {"role": "user", "content": user_input}
#         ]
#         input_data = {
#             "messages": messages
#         }
#         print_stream(graph.stream(input_data, config=config, stream_mode="values"))
