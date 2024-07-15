from gui.navigation import make_sidebar
import streamlit as st
import httpx
from auth.jwt_handler import verify_access_token
import pandas as pd
from decouple import config

make_sidebar()

st.title("This is your operations history")

st.write("Full list of user interactions with system")


cookies = st.session_state["user_cookie"]
user_id = verify_access_token(cookies)["user"]
bearer = "Bearer " + cookies
header = {"Authorization": bearer}
localhost = config("LOCALHOST_URI")


def get_user_transactions():
    transactions = httpx.get(
        url=localhost + "task/history/" + str(user_id), headers=header
    )
    return transactions.json()


result = get_user_transactions()
if len(result) == 0:
    st.write(
        "Oops, no interactions here! Its time to make some! Proceed to Prediction data tab and make a prediction!"
    )
else:
    df = pd.json_normalize(result)
    st.dataframe(df, hide_index=True)
