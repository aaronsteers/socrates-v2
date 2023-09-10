import os
import random

import streamlit as st

from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import ConversationChain
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory

from socrates_v2 import llm

@st.cache_resource
def get_personality() -> llm.SocratesAI:
    """Get the LLM to use."""
    return llm.YodaAI()

@st.cache_resource
def get_opening_prompt():
    return random.choice(get_personality().PROMPTS)

@st.cache_resource
def create_chain() -> ConversationChain:
    memory = ConversationBufferMemory()
    openai_llm = OpenAI(
        model_name=llm.OPENAI_MODEL,
        temperature=llm.TEMPERATURE,
        streaming=True,
    )
    chain = ConversationChain(
        llm=openai_llm,
        memory=memory,
        verbose=True,
        prompt=get_personality().prompt_template,
    )
    return chain

def show_debug():
    with st.sidebar:
        debug_enabled = st.checkbox(
            "Show debug info",
            key="show_debug",
            value=True,
        )
        if debug_enabled:
            with st.container():
                st.subheader("Session state:")
                st.code(str(st.session_state.__dict__), language="json")
                st.subheader("Cache:")
                st.code(str(st.cache_resource.__dict__), language="json")
                st.subheader("History:")
                st.code(str(st.session_state.messages), language="json")

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
    """Method to configure OpenAI API key."""
    openai_api_key = ""
    if "OPENAI_API_KEY" in os.environ:
        openai_api_key = os.environ['OPENAI_API_KEY']

    with st.sidebar:
        openai_api_key = st.sidebar.text_input(
            label="OpenAI API Key",
            type="password",
            value=openai_api_key,
            placeholder="sk-..."
            )
        st.info("Obtain your key from this link: https://platform.openai.com/account/api-keys")

    if openai_api_key:
        st.session_state['OPENAI_API_KEY'] = openai_api_key
        os.environ['OPENAI_API_KEY'] = openai_api_key
    else:
        st.error("Please add your OpenAI API key in the sidebar to continue.")
        st.stop()
    return openai_api_key
