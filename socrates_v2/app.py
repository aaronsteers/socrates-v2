"""This is the Streamlit app file for Socrates v2.

Invoke locally with:
    poetry run streamlit run socrates_v2/app.py

"""

import streamlit as st
import time

from socrates_v2 import ai

st.title("Socrates v2 :brain:")
st.warning(":construction_worker: Socrates v2 is a work in progress.")

st.text_input(
    "What is your question?",
    value="What is the meaning of life?"
)
ask = st.button("Ask")
if ask:
    with st.spinner("Thinking..."):
        # Wait for half of a second...
        time.sleep(0.5)
        pass
    with st.container():
        st.write("Answer:")
        st.write("42")
