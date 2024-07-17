import streamlit as st
from gui.navigation import make_sidebar
import pandas as pd
from decouple import config

make_sidebar()
data_path = config("DATA_PATH")

st.title("Привет, это калькулятор")


@st.cache_data
def load_data():
    return pd.read_csv(data_path)


with st.form("pred calc", clear_on_submit=False):
    intervals = load_data()
    prediction = st.session_state["prediction"]
    st.subheader(f"Вероятность дефолта: {round(prediction[1]*100, 2)}% 🎉")

    # расчёт интервала
    pred_interval = len(intervals[intervals["right_border"] < prediction[1]]) - 1

    # инициируем расчёт калькулятора
    credit_sum = st.number_input(label="Сумма кредита", value=12000000, min_value=100000, max_value=30000000,
                                         step=100000)
    years = st.number_input(label="Срок кредита, в годах", value=10.0, min_value=0.25, max_value=30.0)
    percent = st.number_input(label="Процентная ставка", value=25.0, min_value=0.0, max_value=30.0)

    submit = st.form_submit_button("Рассчитать прибыль!")
    if submit:
        # Мы выдаём всем на интервал одинаковое количество кредитов одинаковой суммы
        credit_applied = credit_sum * intervals["credits_overall"][pred_interval]

        # Тогда мат.ожидание продукта:
        credit_mo = credit_applied * intervals["conversion"][pred_interval]

        # Расчёт прибыльной части кредита
        credit_with_percent = credit_mo * (percent/100) * years

        # итоговая прибыль
        profit = credit_mo + credit_with_percent - credit_applied

        # прибыль на один кредит
        profit = profit / intervals["credits_overall"][pred_interval]

        st.session_state['calc_completed'] = True

        st.write(
            f"Возможная прибыль на полный срок **{round(profit, 2)}**")
        st.write(
            f"Вероятность возврата у клиентов такого типа **{round(intervals['conversion'][pred_interval]*100, 2)}%**")