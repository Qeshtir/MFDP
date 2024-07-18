import streamlit as st
import extra_streamlit_components as stx
import httpx
from navigation import make_sidebar
from decouple import config
import yaml

locale_path = config("LOCALE_PATH")

with open(locale_path, "r") as file:
    dict_ = yaml.safe_load(file)
dict_ = dict_["stApp"]

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
    res = httpx.post(url=localhost + "user/signup", json=data)
    return res


st.title(dict_["title"])
st.subheader(dict_["subHeader"])
st.image(image="gui/bank.jpg")

tab1, tab2 = st.tabs([dict_["loginTab"], dict_["registerTab"]])

with tab1:
    st.write(dict_["login"])
    st.write(dict_["loginNew"])
    username = st.text_input(dict_["username"])
    password = st.text_input(dict_["password"], type="password")

    if st.button(dict_["loginButton"], type="primary"):
        result = password_entered()
        if result.status_code in [401, 404]:
            error_desc = result.json()["detail"]
            st.write(f"{error_desc}")
        else:
            val = result.json()["access_token"]
            cookie_manager.set("access_token", val, max_age=600)
            st.session_state.logged_in = True
            st.success(dict_["loginSuccess"])
            st.session_state["user_cookie"] = cookie_manager.get(cookie="access_token")

            st.switch_page("pages/profile.py")

with tab2:
    st.write(dict_["registerBase"])
    st.write(dict_["registerApi"])
    st.write(dict_["registerExist"])
    firstname = st.text_input(dict_["regName"])
    lastname = st.text_input(dict_["regLastName"])
    login = st.text_input(dict_["regLogin"])
    p_assword = st.text_input(dict_["regPassword"])

    if st.button(dict_["registerButton"], type="primary"):
        result = create_user()
        if result.status_code == 200:
            message = result.json()
            st.write(message["message"])
        else:
            message = result.json()
            st.write(message)
