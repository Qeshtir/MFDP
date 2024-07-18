import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages
from decouple import config
import yaml

locale_path = config("LOCALE_PATH")

with open(locale_path, "r") as file:
    dict_ = yaml.safe_load(file)
dict_ = dict_["nav"]


def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar():
    with st.sidebar:
        st.title(dict_["title"])
        st.write("")
        st.write("")

        if st.session_state.get("logged_in", False):
            st.page_link("pages/profile.py", label=dict_["profile"], icon="🔒")
            st.page_link("pages/history.py", label=dict_["history"], icon="🥇")
            if st.session_state.get("pred_completed", False):
                st.page_link("pages/calc.py", label=dict_["calc"], icon="🎲")

            st.write("")
            st.write("")

            if st.button(dict_["logout"]):
                logout()

        elif get_current_page_name() != "streamlit_app":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("streamlit_app.py")


def logout():
    st.session_state.logged_in = False
    del st.session_state["user_cookie"]
    st.info(dict_["logoutMsg"])
    sleep(0.5)
    st.switch_page("streamlit_app.py")
