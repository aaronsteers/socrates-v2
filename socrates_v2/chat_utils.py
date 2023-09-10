import os
import random

import streamlit as st

from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import ConversationChain
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory

OPENAI_MODEL = "gpt-3.5-turbo"
PROMPTS = [
    "What truth do you seek today?",
    "With which thought shall we engage this day?"
]

@st.cache_resource
def get_opening_prompt():
    return random.choice(PROMPTS)

@st.cache_resource
def create_chain() -> ConversationChain:
    memory = ConversationBufferMemory()
    llm = OpenAI(model_name=OPENAI_MODEL, temperature=0, streaming=True)
    chain = ConversationChain(llm=llm, memory=memory, verbose=True)
    return chain

class StreamHandler(BaseCallbackHandler):
    """Callback handler to stream the response from the chatbot."""
    
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(self.text)

# decorator
def enable_chat_history(func):
    if os.environ.get("OPENAI_API_KEY"):
        # to clear chat history after switching chat threads
        thread_id = func.__qualname__
        if "thread_id" not in st.session_state:
            st.session_state["thread_id"] = thread_id

        if st.session_state["thread_id"] != thread_id:
            st.cache_resource.clear()
            if "thread_id" in st.session_state:
                del st.session_state["thread_id"]
            if "messages" in st.session_state:
                del st.session_state["messages"]
        
        opening_prompt = get_opening_prompt()

        # to show chat history on ui
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": opening_prompt}]

        for msg in st.session_state["messages"]:
            st.chat_message(msg["role"]).write(msg["content"])

    def execute(*args, **kwargs):
        func(*args, **kwargs)

    return execute

def display_msg(msg, author):
    """Method to display message on the UI.

    Args:
        msg (str): message to display
        author (str): author of the message -user/assistant
    """
    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)

def configure_openai_api_key():
    if "OPENAI_API_KEY" not in os.environ:
        with st.sidebar:
            openai_api_key = st.sidebar.text_input(
                label="OpenAI API Key",
                type="password",
                value=st.session_state['OPENAI_API_KEY'] if 'OPENAI_API_KEY' in st.session_state else '',
                placeholder="sk-..."
                )
            st.info("Obtain your key from this link: https://platform.openai.com/account/api-keys")
    else:
        openai_api_key = os.environ["OPENAI_API_KEY"]

    if openai_api_key:
        st.session_state['OPENAI_API_KEY'] = openai_api_key
        os.environ['OPENAI_API_KEY'] = openai_api_key
    else:
        st.error("Please add your OpenAI API key in the sidebar to continue.")
        st.stop()
    return openai_api_key
