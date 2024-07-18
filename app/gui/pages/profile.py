import httpx
import streamlit as st
from auth.jwt_handler import verify_access_token
from gui.navigation import make_sidebar
import pandas as pd
from decouple import config
import yaml

locale_path = config("LOCALE_PATH")

with open(locale_path, "r") as file:
    dict_ = yaml.safe_load(file)
dict_ = dict_["profile"]

make_sidebar()

st.title(dict_["title"])

cookies = st.session_state["user_cookie"]
user_id = verify_access_token(cookies)["user"]
bearer = "Bearer " + cookies
header = {"Authorization": bearer}
localhost = config("LOCALHOST_URI")
data_path = config("DATA_PATH")


def df_entered():
    data = {
        "userid": user_id,
        "dataset": {
            "bureau_AMT_CREDIT_SUM_min": bureau_AMT_CREDIT_SUM_min,
            "prev_SELLERPLACE_AREA_min": prev_SELLERPLACE_AREA_min,
            "AMT_INCOME_TOTAL": AMT_INCOME_TOTAL,
            "prev_AMT_DOWN_PAYMENT_mean": prev_AMT_DOWN_PAYMENT_mean,
            "prev_WEEKDAY_APPR_PROCESS_START_SATURDAY_count_norm": prev_WEEKDAY_APPR_PROCESS_START_SATURDAY_count_norm,
            "bureau_AMT_CREDIT_SUM_DEBT_max": bureau_AMT_CREDIT_SUM_DEBT_max,
            "bureau_DAYS_CREDIT_UPDATE_mean": bureau_DAYS_CREDIT_UPDATE_mean,
            "bureau_DAYS_CREDIT_UPDATE_max": bureau_DAYS_CREDIT_UPDATE_max,
            "prev_NAME_GOODS_CATEGORY_Furniture_count_norm": prev_NAME_GOODS_CATEGORY_Furniture_count_norm,
            "bureau_DAYS_ENDDATE_FACT_max": bureau_DAYS_ENDDATE_FACT_max,
            "AMT_REQ_CREDIT_BUREAU_QRT": AMT_REQ_CREDIT_BUREAU_QRT,
            "OWN_CAR_AGE": OWN_CAR_AGE,
            "bureau_DAYS_CREDIT_ENDDATE_max": bureau_DAYS_CREDIT_ENDDATE_max,
            "prev_CNT_PAYMENT_mean": prev_CNT_PAYMENT_mean,
            "BASEMENTAREA_AVG": BASEMENTAREA_AVG,
            "LANDAREA_AVG": LANDAREA_AVG,
            "bureau_AMT_CREDIT_SUM_DEBT_min": bureau_AMT_CREDIT_SUM_DEBT_min,
            "FLAG_OWN_CAR": FLAG_OWN_CAR,
            "ORGANIZATION_TYPE_Self-employed": ORGANIZATION_TYPE_Self_employed,
            "FLOORSMIN_AVG": FLOORSMIN_AVG,
            "FLOORSMAX_AVG": FLOORSMAX_AVG,
            "DAYS_BIRTH": DAYS_BIRTH,
            "NONLIVINGAREA_AVG": NONLIVINGAREA_AVG,
            "APARTMENTS_AVG": APARTMENTS_AVG,
            "HOUSETYPE_MODE_block of flats": HOUSETYPE_MODE_block_of_flats,
            "EXT_SOURCE_2": EXT_SOURCE_2,
            "NONLIVINGAPARTMENTS_AVG": NONLIVINGAPARTMENTS_AVG,
            "YEARS_BUILD_AVG": YEARS_BUILD_AVG,
            "COMMONAREA_AVG": COMMONAREA_AVG,
            "YEARS_BEGINEXPLUATATION_AVG": YEARS_BEGINEXPLUATATION_AVG,
            "EXT_SOURCE_1": EXT_SOURCE_1,
            "EXT_SOURCE_3": EXT_SOURCE_3,
        },
    }
    res = httpx.post(url=localhost + "df/add/", json=data, headers=header)
    return res.json()


def create_task():
    user_df = df_entered()["id"]
    st.session_state["user_df"] = user_df
    data = {"userid": user_id, "user_df_id": user_df, "status": "created"}
    res = httpx.post(url=localhost + "task/execute/", json=data, headers=header)
    return res


def get_prediction():
    user_df = st.session_state["user_df"]
    res = httpx.get(url=localhost + "df/get/" + str(user_df))
    return res


# Initialize session state
if "first_form_completed" not in st.session_state:
    st.session_state["first_form_completed"] = False

with st.form("df enter"):
    st.subheader(dict_["subHeader"])

    st.write(dict_["userData"]["desc"])
    st.caption(dict_["userData"]["caption"])

    AMT_INCOME_TOTAL = st.number_input(
        label=dict_["userData"]["AMT_INCOME_TOTAL"]["label"],
        value=261000.0,
        min_value=0.1,
        help=dict_["userData"]["AMT_INCOME_TOTAL"]["help"],
    )
    FLAG_OWN_CAR = st.number_input(
        label=dict_["userData"]["FLAG_OWN_CAR"]["label"],
        value=1.0,
        min_value=0.0,
        max_value=1.0,
        step=1.0,
        help=dict_["userData"]["FLAG_OWN_CAR"]["help"],
    )
    OWN_CAR_AGE = st.number_input(
        label=dict_["userData"]["OWN_CAR_AGE"]["label"],
        value=8.0,
        min_value=0.0,
        help=dict_["userData"]["OWN_CAR_AGE"]["help"],
    )
    ORGANIZATION_TYPE_Self_employed = st.number_input(
        label=dict_["userData"]["ORGANIZATION_TYPE_Self_employed"]["label"],
        value=0.0,
        min_value=0.0,
        max_value=1.0,
        step=1.0,
        help=dict_["userData"]["ORGANIZATION_TYPE_Self_employed"]["help"],
    )
    DAYS_BIRTH = st.number_input(
        label=dict_["userData"]["DAYS_BIRTH"]["label"],
        value=-16499,
        min_value=-43800,
        max_value=-6570,
        step=1,
        help=dict_["userData"]["DAYS_BIRTH"]["help"],
    )
    HOUSETYPE_MODE_block_of_flats = st.number_input(
        label=dict_["userData"]["HOUSETYPE_MODE_block_of_flats"]["label"],
        value=1.0,
        min_value=0.0,
        max_value=1.0,
        step=1.0,
        help=dict_["userData"]["HOUSETYPE_MODE_block_of_flats"]["help"],
    )

    st.write(dict_["userDataCalc"]["desc"])
    st.caption(dict_["userDataCalc"]["caption"])

    st.write(dict_["userDataCalc"]["bkiDesc"])

    AMT_REQ_CREDIT_BUREAU_QRT = st.number_input(
        label=dict_["userDataCalc"]["AMT_REQ_CREDIT_BUREAU_QRT"]["label"],
        value=0.0,
        step=1.0,
        min_value=0.0,
        help=dict_["userDataCalc"]["AMT_REQ_CREDIT_BUREAU_QRT"]["help"],
    )

    st.write(dict_["userDataCalc"]["houseDesc"])

    BASEMENTAREA_AVG = st.number_input(
        label=dict_["userDataCalc"]["BASEMENTAREA_AVG"]["label"],
        value=0.092500,
        min_value=0.0,
        format="%.6f",
    )
    LANDAREA_AVG = st.number_input(
        label=dict_["userDataCalc"]["LANDAREA_AVG"]["label"],
        value=0.127900,
        min_value=0.0,
        format="%.6f",
    )
    FLOORSMIN_AVG = st.number_input(
        label=dict_["userDataCalc"]["FLOORSMIN_AVG"]["label"],
        value=0.208300,
        min_value=0.0,
        format="%.6f",
    )
    FLOORSMAX_AVG = st.number_input(
        label=dict_["userDataCalc"]["FLOORSMAX_AVG"]["label"],
        value=0.166700,
        min_value=0.0,
        format="%.6f",
    )
    NONLIVINGAREA_AVG = st.number_input(
        label=dict_["userDataCalc"]["NONLIVINGAREA_AVG"]["label"],
        value=0.017000,
        min_value=0.0,
        format="%.6f",
    )
    APARTMENTS_AVG = st.number_input(
        label=dict_["userDataCalc"]["APARTMENTS_AVG"]["label"],
        value=0.158800,
        min_value=0.0,
        format="%.6f",
    )
    NONLIVINGAPARTMENTS_AVG = st.number_input(
        label=dict_["userDataCalc"]["NONLIVINGAPARTMENTS_AVG"]["label"],
        value=0.0,
        min_value=0.0,
        format="%.6f",
    )
    YEARS_BUILD_AVG = st.number_input(
        label=dict_["userDataCalc"]["YEARS_BUILD_AVG"]["label"],
        value=0.755200,
        min_value=0.0,
        format="%.6f",
    )
    COMMONAREA_AVG = st.number_input(
        label=dict_["userDataCalc"]["COMMONAREA_AVG"]["label"],
        value=0.019100,
        min_value=0.0,
        format="%.6f",
        help=dict_["userDataCalc"]["COMMONAREA_AVG"]["help"],
    )
    YEARS_BEGINEXPLUATATION_AVG = st.number_input(
        label=dict_["userDataCalc"]["YEARS_BEGINEXPLUATATION_AVG"]["label"],
        value=0.982100,
        min_value=0.0,
        format="%.6f",
    )

    st.write(dict_["bki"]["desc"])
    st.caption(dict_["bki"]["caption"])
    st.caption(dict_["bki"]["caption2"])

    bureau_AMT_CREDIT_SUM_min = st.number_input(
        label=dict_["bki"]["bureau_AMT_CREDIT_SUM_min"]["label"],
        value=0.0,
        min_value=0.0,
    )
    bureau_AMT_CREDIT_SUM_DEBT_max = st.number_input(
        label=dict_["bki"]["bureau_AMT_CREDIT_SUM_DEBT_max"]["label"], value=638496.0
    )
    bureau_DAYS_CREDIT_UPDATE_mean = st.number_input(
        label=dict_["bki"]["bureau_DAYS_CREDIT_UPDATE_mean"]["label"],
        value=-250.666667,
        help=dict_["bki"]["bureau_DAYS_CREDIT_UPDATE_mean"]["help"],
    )
    bureau_DAYS_CREDIT_UPDATE_max = st.number_input(
        label=dict_["bki"]["bureau_DAYS_CREDIT_UPDATE_max"]["label"],
        value=-15.0,
        help=dict_["bki"]["bureau_DAYS_CREDIT_UPDATE_max"]["help"],
    )
    bureau_DAYS_ENDDATE_FACT_max = st.number_input(
        label=dict_["bki"]["bureau_DAYS_ENDDATE_FACT_max"]["label"],
        value=-813.0,
        max_value=0.0,
        help=dict_["bki"]["bureau_DAYS_ENDDATE_FACT_max"]["help"],
    )
    bureau_DAYS_CREDIT_ENDDATE_max = st.number_input(
        label=dict_["bki"]["bureau_DAYS_CREDIT_ENDDATE_max"]["label"],
        value=1043.0,
        help=dict_["bki"]["bureau_DAYS_CREDIT_ENDDATE_max"]["help"],
    )
    bureau_AMT_CREDIT_SUM_DEBT_min = st.number_input(
        label=dict_["bki"]["bureau_AMT_CREDIT_SUM_DEBT_min"]["label"],
        value=None,
        placeholder=0.0,
    )

    st.write(dict_["bank"]["desc"])
    st.caption(dict_["bank"]["caption"])
    st.caption(dict_["bank"]["caption2"])

    prev_SELLERPLACE_AREA_min = st.number_input(
        label=dict_["bank"]["prev_SELLERPLACE_AREA_min"]["label"],
        value=4.0,
        min_value=-1.0,
        help=dict_["bank"]["prev_SELLERPLACE_AREA_min"]["help"],
    )
    prev_AMT_DOWN_PAYMENT_mean = st.number_input(
        label=dict_["bank"]["prev_AMT_DOWN_PAYMENT_mean"]["label"],
        value=0.0,
        min_value=0.0,
    )
    prev_WEEKDAY_APPR_PROCESS_START_SATURDAY_count_norm = st.number_input(
        label=dict_["bank"]["prev_SATURDAY"]["label"],
        value=0.0,
        min_value=0.0,
        help=dict_["bank"]["prev_SATURDAY"]["help"],
    )
    prev_NAME_GOODS_CATEGORY_Furniture_count_norm = st.number_input(
        label=dict_["bank"]["prev_Furniture"]["label"],
        value=0.0,
        min_value=0.0,
        help=dict_["bank"]["prev_Furniture"]["help"],
    )
    prev_CNT_PAYMENT_mean = st.number_input(
        label=dict_["bank"]["prev_CNT_PAYMENT_mean"]["label"], value=36.0, min_value=0.0
    )

    st.write(dict_["scoring"]["desc"])
    st.caption(dict_["scoring"]["caption"])

    EXT_SOURCE_1 = st.number_input(
        label=dict_["scoring"]["EXT_SOURCE_1"],
        value=0.560240,
        min_value=0.0,
        format="%.6f",
    )
    EXT_SOURCE_2 = st.number_input(
        label=dict_["scoring"]["EXT_SOURCE_2"],
        value=0.552325,
        min_value=0.0,
        format="%.6f",
    )
    EXT_SOURCE_3 = st.number_input(
        label=dict_["scoring"]["EXT_SOURCE_3"],
        value=0.429424,
        min_value=0.0,
        format="%.6f",
    )

    submit = st.form_submit_button(dict_["defaultButton"])
    if submit:
        st.write(dict_["waitingMessage"])
        result = create_task()
        if result.status_code == 200:
            message = result.json()["message"]
            prediction = get_prediction().json()
            st.session_state["first_form_completed"] = True
            st.session_state["prediction"] = prediction
        else:
            st.write(result.json())


@st.cache_data
def load_data():
    return pd.read_csv(data_path)


if "pred_completed" not in st.session_state:
    st.session_state["pred_completed"] = False

if st.session_state["first_form_completed"]:
    st.subheader(
        dict_["defaultProba"]
        + str(round(prediction[1] * 100, 2))
        + dict_["defaultProbaIcon"]
    )

    intervals = load_data()

    # расчёт интервала
    pred_interval = len(intervals[intervals["right_border"] < prediction[1]]) - 1

    # инициируем светофочик

    if intervals["conversion"][pred_interval] > 0.98:
        st.success(dict_["green"])
        st.session_state["first_form_completed"] = False
        st.session_state["pred_completed"] = True
        st.button(dict_["buttonCalc"])

    elif (intervals["conversion"][pred_interval] <= 0.98) & (
        intervals["conversion"][pred_interval] > 0.9
    ):
        st.warning(dict_["yellow"])
        st.session_state["first_form_completed"] = False
        st.session_state["pred_completed"] = True
        st.button(dict_["buttonCalc"])

    else:
        st.error(dict_["red"])
        st.session_state["first_form_completed"] = False
        st.session_state["pred_completed"] = True
        st.button(dict_["buttonCalc"])
