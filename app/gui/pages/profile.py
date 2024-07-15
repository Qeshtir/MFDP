import httpx
import streamlit as st
from auth.jwt_handler import verify_access_token
from gui.navigation import make_sidebar
import pandas as pd
import numpy as np
import json
from decouple import config

make_sidebar()


st.title("Привет")

st.write("Здесь всё будет на русском, просто потому что данные в задаче трудно интерпретировать")

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
    res = httpx.post(url=localhost+"df/add/", json=data, headers=header)
    return res.json()


def create_task():
    user_df = df_entered()["id"]
    st.session_state["user_df"] = user_df
    data = {"userid": user_id, "user_df_id": user_df, "status": "created"}
    res = httpx.post(
        url=localhost+"task/execute/", json=data, headers=header
    )
    return res


def get_prediction():
    user_df = st.session_state["user_df"]
    res = httpx.get(url=localhost+"df/get/"+str(user_df))
    return res


with st.form("df enter"):
    prediction = None
    st.subheader("Форма для получения предсказания")

    st.write("Данные, которые можно получить с клиента")
    st.caption("Здесь содержится блок данных, которые можно получить опросом клиента при звонке или заполнении формы на сайте")

    AMT_INCOME_TOTAL = st.number_input(label="Годовой доход клиента", value= 261000.0, min_value=0.1,
                                       help="Не может быть 0, мы же не хотим выдавать ипотеку людям, не имеющим дохода?")
    FLAG_OWN_CAR = st.number_input(label="Наличие машины", value= 1.0, min_value=0.0, max_value=1.0, step=1.0,
                                       help="1.0 или 0.0. Здесь должен быть флаг, но для реализации так проще.")
    OWN_CAR_AGE = st.number_input(label="Возраст машины", value= 8.0, min_value=0.0,
                                       help="Возраст машины клиента, 0 если машины нет")
    ORGANIZATION_TYPE_Self_employed = st.number_input(label="Признак самозанятости", value=0.0, min_value=0.0, max_value=1.0, step=1.0,
                                       help="1.0 или 0.0. Здесь должен быть флаг, но для реализации так проще.")
    DAYS_BIRTH = st.number_input(label="Возраст клиента", value=-16499, min_value=-43800, max_value=-6570, step=1,
                                       help="В днях, относительно текущей даты. Всегда отрицательное число, не может быть меньше 18 лет")
    HOUSETYPE_MODE_block_of_flats = st.number_input(label="Признак многоквартирности", value=1.0, min_value=0.0, max_value=1.0, step=1.0,
                                       help="1.0 или 0.0, по типу жилья, в котором проживает клиент. Здесь должен быть флаг, но для реализации так проще.")


    st.write("Данные клиента, предрассчитанные")
    st.caption(
        "Здесь содержится блок данных, которые можно получить у клиента, но они требуют агрегации, и в интерфейсе пользователя"
        "должны отображаться автоматически. Тем не менее, здесь, в рамках демо, мы сделаем их изменяемыми")

    st.write("Данные об обращении в БКИ")

    AMT_REQ_CREDIT_BUREAU_QRT = st.number_input(label="Количество обращений клиента в кредитное бюро", value=0.0, step=1.0, min_value=0.0,
                                       help="Количество обращений клиента в кредитное бюро за квартал до месяца, предшествующего подаче заявки")

    st.write("Данные о недвижимости клиента, нормализованные")

    BASEMENTAREA_AVG = st.number_input(label="Средняя площадь подвала", value=0.092500, min_value=0.0, format="%.6f")
    LANDAREA_AVG = st.number_input(label="Средняя площадь придомовой территории", value=0.127900, min_value=0.0, format="%.6f")
    FLOORSMIN_AVG = st.number_input(label="Среднее минимальное количество этажей жилья", value=0.208300, min_value=0.0, format="%.6f")
    FLOORSMAX_AVG = st.number_input(label="Среднее максимальное количество этажей жилья", value=0.166700, min_value=0.0, format="%.6f")
    NONLIVINGAREA_AVG = st.number_input(label="Средняя нежилая площадь (всего)", value=0.017000, min_value=0.0, format="%.6f")
    APARTMENTS_AVG = st.number_input(label="Средняя жилая площадь", value=0.158800, min_value=0.0, format="%.6f")
    NONLIVINGAPARTMENTS_AVG = st.number_input(label="Средняя нежилая площадь апартаментов", value=0.0, min_value=0.0, format="%.6f")
    YEARS_BUILD_AVG = st.number_input(label="Средний возраст жилья в годах", value=0.755200, min_value=0.0, format="%.6f")
    COMMONAREA_AVG = st.number_input(label="Средняя площадь общего назначения", value=0.019100, min_value=0.0, format="%.6f",
                                     help="Параметр плохо поддаётся интерпретации, в России бы такое место называлось МОП, но оно не является частной собственностью")
    YEARS_BEGINEXPLUATATION_AVG = st.number_input(label="Средний возраст жилья в годах", value=0.982100, min_value=0.0, format="%.6f")

    st.write("Данные БКИ, предрассчитанные")
    st.caption(
        "Здесь содержится блок данных, которые можно получить у БКИ, но они требуют агрегации, и в интерфейсе пользователя"
        "должны отображаться автоматически. Тем не менее, здесь, в рамках демо, мы сделаем их изменяемыми")
    st.caption(
        "Важно! Эти параметры могут быть не заполненными, т.к. тех или иных данных по клиенту может не быть. В качестве иллюстрации"
        "для такой возможности выбран параметр 'Минимальная сумма открытой задолженности по кредиту'")

    bureau_AMT_CREDIT_SUM_min = st.number_input(label="Минимальная сумма открытого кредита", value=0.0, min_value=0.0)
    bureau_AMT_CREDIT_SUM_DEBT_max = st.number_input(label="Максимальная сумма открытой задолженности по кредиту", value=638496.0)
    bureau_DAYS_CREDIT_UPDATE_mean = st.number_input(label="Как давно, в среднем, менялись данные БКИ", value=-250.666667,
                                                     help="Количество дней до подачи заявки, "
                                                          "за которое происходило последнее обновление по кредитам аппликанта, "
                                                          "может быть положительной (допришедшие данные после подачи заявки) может быть 0."
                                                          "Описательная статистика, среднее по аппликанту.")
    bureau_DAYS_CREDIT_UPDATE_max = st.number_input(label="Как давно в последний раз менялись данные БКИ", value=-15.0,
                                                    help="Количество дней до подачи заявки, "
                                                         "за которое происходило последнее обновление по кредитам аппликанта, "
                                                         "может быть положительной (допришедшие данные после подачи заявки) может быть 0."
                                                         "Описательная статистика, максимум по аппликанту.")
    bureau_DAYS_ENDDATE_FACT_max = st.number_input(label="Когда закрыт последний кредит", value=-813.0, max_value=0.0,
                                                   help="Количество дней, прошедших с момента закрытия предыдущего кредита, 0.0 - в дату подачи заявки.")

    bureau_DAYS_CREDIT_ENDDATE_max = st.number_input(label="Когда будет закрыт самый долгий кредит", value=1043.0,
                                                     help="0.0 или отрицательное число - он уже закрыт.")
    bureau_AMT_CREDIT_SUM_DEBT_min = st.number_input(label="Минимальная сумма открытой задолженности по кредиту", value=None, placeholder=0.0)

    st.write("Данные истории банка, предрассчитанные")
    st.caption(
        "Здесь содержится блок данных, которые можно получить у банка в рамках прошлых взаимодействий с клиентом, но они требуют агрегации, и в интерфейсе пользователя"
        "должны отображаться автоматически. Тем не менее, здесь, в рамках демо, мы сделаем их изменяемыми.")
    st.caption(
        "Важно! Эти параметры могут быть не заполненными, т.к. тех или иных данных по клиенту может не быть. Пример подобной ситуации иллюстрирован выше.")

    prev_SELLERPLACE_AREA_min = st.number_input(label="Минимальная торговая площадь места продавца", value=4.0, min_value=-1.0,
                                                help="0.0 - нет площади, отрицательное число - не продавец.")
    prev_AMT_DOWN_PAYMENT_mean = st.number_input(label="Средний аванс предыдущего кредита", value=0.0, min_value=0.0)
    prev_WEEKDAY_APPR_PROCESS_START_SATURDAY_count_norm = st.number_input(label="Как часто в среднем день оформления кредита был субботой?", value=0.0, min_value=0.0,
                                                            help = "Пожалуй, самый забавный признак. Это среднее значение всех раз,"
                                                                   "когда клиент обращался за предыдущим кредитом в субботу."
                                                                          )
    prev_NAME_GOODS_CATEGORY_Furniture_count_norm = st.number_input(label="Как часто в среднем предмет кредита был мебелью?", value=0.0, min_value=0.0,
                                                            help = "Тоже забавный признак. Это среднее значение всех раз,"
                                                                   "когда клиент обращался за кредитом именно на мебель."
                                                                          )
    prev_CNT_PAYMENT_mean = st.number_input(label="Средний срок предыдущего кредита", value=36.0, min_value=0.0)

    st.write("Данные кредитного скоринга")
    st.caption(
        "В оригинальном датасете эти данные были кодированы и нормализованы. Подобные вещи в интерфейсе пользователя"
        "должны отображаться автоматически. Тем не менее, здесь, в рамках демо, мы сделаем их изменяемыми.")

    EXT_SOURCE_1 = st.number_input(label="Значение скоринга, первая компонента", value=0.560240, min_value=0.0, format="%.6f")
    EXT_SOURCE_2 = st.number_input(label="Значение скоринга, вторая компонента", value=0.552325, min_value=0.0, format="%.6f")
    EXT_SOURCE_3 = st.number_input(label="Значение скоринга, третья компонента", value=0.429424, min_value=0.0, format="%.6f")

    submit = st.form_submit_button("Предсказать дефолт!")
    if submit:
        st.write(f"Please, wait a couple of seconds. Prediction will take some time")
        result = create_task()
        if result.status_code == 200:
            message = result.json()["message"]
            prediction = get_prediction().json()
        else:
            st.write(result.json())


@st.cache_data
def load_data():
    return pd.read_csv(data_path)


if prediction:
    st.subheader(f"Congratz! Your default proba is {prediction[1]} 🎉")
    st.write(
        f"However, I we're not sure, if client will have a default or not, so here is some interpret data, for making us more confident:"
    )
    data = load_data()

    #hist_values = np.histogram(data["quality"], bins=9, range=(0, 8))[0]
    #st.bar_chart(hist_values)
    st.write(data.describe())
    st.write(data.head(100))
