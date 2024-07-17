import streamlit as st
import extra_streamlit_components as stx
import httpx
from navigation import make_sidebar
from decouple import config

make_sidebar()


def get_manager():
    return stx.CookieManager()


cookie_manager = get_manager()
localhost = config("LOCALHOST_URI")


def password_entered():
    data = {
        "grant_type": "",
        "username": username,
        "password": password,
        "client_id": "",
        "client_secret": "",
    }
    res = httpx.post(url=localhost + "user/signin", data=data)
    return res


def create_user():
    data = {
        "firstname": firstname,
        "lastname": lastname,
        "login": login,
        "password": p_assword,
        "role": "user",
    }
    res = httpx.post(url=localhost+ "user/signup", json=data)
    return res


st.title("Welcome to the Default Default app. The default app for predicting default.")
st.image(image="gui/bank.jpg")

tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    st.write(f"Please log in to continue.")
    st.write("If you don't have a user, tap Register tab and proceed.")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Sign in", type="primary"):
        result = password_entered()
        if result.status_code in [401, 404]:
            error_desc = result.json()["detail"]
            st.write(f"{error_desc}")
        else:
            val = result.json()["access_token"]
            cookie_manager.set("access_token", val, max_age=600)
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
            st.session_state["user_cookie"] = cookie_manager.get(cookie="access_token")

            st.switch_page("pages/profile.py")

with tab2:
    st.write(f"Please register a new user to continue, if you dont have one already.")
    st.write("You can create a demo user with swagger api.")
    st.write("If you already have a user, tap Login tab and proceed.")
    firstname = st.text_input("Firstname")
    lastname = st.text_input("Lastname")
    login = st.text_input("Login (try to make it unique)")
    p_assword = st.text_input("Password")

    if st.button("Sign up", type="primary"):
        result = create_user()
        if result.status_code == 200:
            message = result.json()
            st.write(message["message"])
        else:
            message = result.json()
            st.write(message)
