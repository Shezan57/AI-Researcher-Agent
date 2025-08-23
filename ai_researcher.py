# Step1: Install and import dependencies
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from read_pdf import read_pdf
from write_pdf import render_latex_pdf
from arxiv_tool import arxiv_search
import os
from initial_prompt import INITIAL_PROMPT


# Step2: Set up LLM and tools
tools = [read_pdf, render_latex_pdf, arxiv_search]
llm = ChatOpenAI(model="gpt-4o",temperature=0.7)


# Step3: create ReAct agent graph
graph = create_react_agent(llm, tools)

# Step4: Run the agent with an initial prompt


def print_stream(stream):
    for s in stream:
        messages = s["messages"][-1]
        print(f"Messages recived: {messages.content[:200]}...")
        messages.pretty_print()

while True:
    user_input = input("User: ")
    if user_input:
        messages = [
            {"role": "system", "content":INITIAL_PROMPT},
            {"role": "user", "content": user_input}
        ]
        input_data = {
            "messages": messages
        }
        print_stream(graph.stream(input_data, stream_mode="values"))