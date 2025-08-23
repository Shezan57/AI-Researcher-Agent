import streamlit as st 
from pathlib import Path
from ai_researcher2 import graph, config
from initial_prompt import INITIAL_PROMPT
import logging
from langchain_core.messages import AIMessage
from typing import Generator, Any
from dotenv import load_dotenv
load_dotenv()
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Basic app config
st.set_page_config(page_title="AI Researcher Agent")

st.title("AI Researcher Agent")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    logger.info("Initialized chat history in session state.")
    
if "pdf_path" not in st.session_state:
    st.session_state.pdf_path = None
    logger.info("Initialized pdf_path in session state.")

for message in st.session_state['chat_history']:
    with st.chat_message(message["role"]):
        st.write(message["content"])
    
def _extract_text(content: Any) -> str:
    """Normalize LangChain / OpenAI style content (could be str or list of parts)."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for p in content:
            if isinstance(p, str):
                parts.append(p)
            elif isinstance(p, dict):
                # OpenAI tool-aware responses often have {"type":"text","text":...}
                if p.get("type") == "text" and "text" in p:
                    parts.append(p["text"])
        return "".join(parts)
    return ""

def _stream_ai(chat_input: dict) -> Generator[str, None, str]:
    """Yield incremental assistant text only, skipping tool call messages.

    Returns the full accumulated text at the end (as the generator return value).
    """
    full = ""
    for event in graph.stream(chat_input, config=config, stream_mode="values"):
        msg = event["messages"][-1]
        # Only surface pure assistant content (skip tool messages & tool call placeholders)
        if isinstance(msg, AIMessage):
            text = _extract_text(msg.content).strip()
            if text:
                # Yield only the newly added portion
                new_segment = text[len(full):] if text.startswith(full) else text
                if new_segment:
                    yield new_segment
                full = text
    return full

# chat interface
user_input = st.chat_input("What research topic would you like to explore...")

if user_input:
    user_input = str(user_input).strip()
    logger.info(f"User input received: {user_input}")
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    chat_input = {"messages": [{"role": "system", "content": INITIAL_PROMPT}] + st.session_state.chat_history}
    logger.info("Prepared chat input for the agent.")

    with st.chat_message("assistant"):
        # Stream incremental chunks
        stream = _stream_ai(chat_input)
        accumulated = ""  # will collect via generator iteration
        for chunk in stream:
            st.write(chunk, unsafe_allow_html=False)
            accumulated += chunk
        # After streaming completes, append final assistant message
        st.session_state["chat_history"].append({"role": "assistant", "content": accumulated})
    
    # stream agent response
    # full_response = ""
    # for s in graph.stream(chat_input, config=config, stream_mode="values"):
    #     messages = s["messages"][-1]
        
    #     # Handle tool calls (log only)
    #     if getattr(messages, 'tool_calls', None):
    #         for call in messages.tool_calls:
    #             logger.info(f"Tool called: {call['name']}")

    #     # Handle assistant response
    #     if isinstance(messages, AIMessage) and messages.content:
    #         text_content = messages.content if isinstance(messages.content, str) else str(messages.content)
    #         full_response += text_content+" "
    #         st.chat_message("assistant").write_stream(full_response)

            

    # # Add final response to history
    # if full_response:
    #     st.session_state.chat_history.append({"role": "assistant", "content": full_response})
    #     logger.info("Added assistant response to chat history.")
# show pdf download if available
if st.session_state.pdf_path:
    pdf_path = Path(st.session_state.pdf_path)
    if pdf_path.exists():
        with open(pdf_path, "rb") as f:
            st.download_button(
                "Download PDF",
                f,
                file_name=pdf_path.name,
                mime="application/pdf"
            )
        logger.info(f"PDF available for download: {pdf_path}")
    