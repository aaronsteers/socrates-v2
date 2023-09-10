"""This is the Streamlit app file for Socrates v2.

Invoke locally with:
    poetry run streamlit run socrates_v2/app.py
"""

import streamlit as st

from socrates_v2 import chat_utils

st.set_page_config(page_title="Socrates 2.0", page_icon=":brain:")
st.title("Socrates 2.0 :brain:")

st.warning(":construction_worker: Socrates 2.0 is a work in progress.")

class SocratesChatbot:

    def __init__(self):
        chat_utils.configure_openai_api_key()

    @chat_utils.enable_chat_history
    def main(self):
        chain = chat_utils.create_chain()
        user_query = st.chat_input(placeholder="")
        if user_query:
            chat_utils.display_msg(user_query, 'user')
            with st.chat_message("assistant"):
                st_cb = chat_utils.StreamHandler(st.empty())
                response = chain.run(user_query, callbacks=[st_cb])
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )


if __name__ == "__main__":
    obj = SocratesChatbot()
    obj.main()
