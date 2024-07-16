from fastapi.testclient import TestClient


# Positive case - creating a DF for user, we already created previously
def test_df_creation(client: TestClient):
    user = {
        "firstname": "Demo",
        "lastname": "User",
        "login": "DemoLogin",
        "password": "demo",
        "role": "user",
    }

    client.post("/user/signup", json=user)
    df = {
        "userid": 1,
        "dataset": {
            "bureau_AMT_CREDIT_SUM_min": 0.0,
            "prev_SELLERPLACE_AREA_min": 4.0,
            "AMT_INCOME_TOTAL": 261000.0,
            "prev_AMT_DOWN_PAYMENT_mean": 0.0,
            "prev_WEEKDAY_APPR_PROCESS_START_SATURDAY_count_norm": 0.0,
            "bureau_AMT_CREDIT_SUM_DEBT_max": 638496.0,
            "bureau_DAYS_CREDIT_UPDATE_mean": -250.666667,
            "bureau_DAYS_CREDIT_UPDATE_max": -15.0,
            "prev_NAME_GOODS_CATEGORY_Furniture_count_norm": 0.0,
            "bureau_DAYS_ENDDATE_FACT_max": -813.0,
            "AMT_REQ_CREDIT_BUREAU_QRT": 0.0,
            "OWN_CAR_AGE": 8.0,
            "bureau_DAYS_CREDIT_ENDDATE_max": 1043.0,
            "prev_CNT_PAYMENT_mean": 36.0,
            "BASEMENTAREA_AVG": 0.092500,
            "LANDAREA_AVG": 0.127900,
            "bureau_AMT_CREDIT_SUM_DEBT_min": 0.0,
            "FLAG_OWN_CAR": 1,
            "ORGANIZATION_TYPE_Self-employed": 0,
            "FLOORSMIN_AVG": 0.208300,
            "FLOORSMAX_AVG": 0.166700,
            "DAYS_BIRTH": -16499,
            "NONLIVINGAREA_AVG": 0.017000,
            "APARTMENTS_AVG": 0.158800,
            "HOUSETYPE_MODE_block of flats": 1,
            "EXT_SOURCE_2": 0.552325,
            "NONLIVINGAPARTMENTS_AVG": 0.0,
            "YEARS_BUILD_AVG": 0.755200,
            "COMMONAREA_AVG": 0.019100,
            "YEARS_BEGINEXPLUATATION_AVG": 0.982100,
            "EXT_SOURCE_1": 0.560240,
            "EXT_SOURCE_3": 0.429424,
        },
    }

    response = client.post("/df/add/", json=df)
    assert response.status_code == 200


# Negative case - creating a DF for unknown user
def test_df_create_unknown_user(client: TestClient):
    df = {
        "userid": 101,
        "dataset": {
            "bureau_AMT_CREDIT_SUM_min": 0.0,
            "prev_SELLERPLACE_AREA_min": 4.0,
            "AMT_INCOME_TOTAL": 261000.0,
            "prev_AMT_DOWN_PAYMENT_mean": 0.0,
            "prev_WEEKDAY_APPR_PROCESS_START_SATURDAY_count_norm": 0.0,
            "bureau_AMT_CREDIT_SUM_DEBT_max": 638496.0,
            "bureau_DAYS_CREDIT_UPDATE_mean": -250.666667,
            "bureau_DAYS_CREDIT_UPDATE_max": -15.0,
            "prev_NAME_GOODS_CATEGORY_Furniture_count_norm": 0.0,
            "bureau_DAYS_ENDDATE_FACT_max": -813.0,
            "AMT_REQ_CREDIT_BUREAU_QRT": 0.0,
            "OWN_CAR_AGE": 8.0,
            "bureau_DAYS_CREDIT_ENDDATE_max": 1043.0,
            "prev_CNT_PAYMENT_mean": 36.0,
            "BASEMENTAREA_AVG": 0.092500,
            "LANDAREA_AVG": 0.127900,
            "bureau_AMT_CREDIT_SUM_DEBT_min": 0.0,
            "FLAG_OWN_CAR": 1,
            "ORGANIZATION_TYPE_Self-employed": 0,
            "FLOORSMIN_AVG": 0.208300,
            "FLOORSMAX_AVG": 0.166700,
            "DAYS_BIRTH": -16499,
            "NONLIVINGAREA_AVG": 0.017000,
            "APARTMENTS_AVG": 0.158800,
            "HOUSETYPE_MODE_block of flats": 1,
            "EXT_SOURCE_2": 0.552325,
            "NONLIVINGAPARTMENTS_AVG": 0.0,
            "YEARS_BUILD_AVG": 0.755200,
            "COMMONAREA_AVG": 0.019100,
            "YEARS_BEGINEXPLUATATION_AVG": 0.982100,
            "EXT_SOURCE_1": 0.560240,
            "EXT_SOURCE_3": 0.429424,
        },
    }

    response = client.post("/df/add/", json=df)
    assert response.status_code == 404
    assert response.json() == {"detail": "User does not exist"}


# Positive case - validation pattern - adding missing values
def test_df_partially_input(client: TestClient):
    df = {
        "userid": 1,
        "dataset": {
            "bureau_AMT_CREDIT_SUM_min": 0.0,
            "prev_SELLERPLACE_AREA_min": 4.0,
            "AMT_INCOME_TOTAL": 261000.0,
            "prev_AMT_DOWN_PAYMENT_mean": 0.0,
            "prev_WEEKDAY_APPR_PROCESS_START_SATURDAY_count_norm": 0.0,
            "bureau_AMT_CREDIT_SUM_DEBT_max": 638496.0,
            "bureau_DAYS_CREDIT_UPDATE_mean": -250.666667,
            "bureau_DAYS_CREDIT_UPDATE_max": -15.0,
            "prev_NAME_GOODS_CATEGORY_Furniture_count_norm": 0.0,
            "bureau_DAYS_ENDDATE_FACT_max": -813.0,
            "AMT_REQ_CREDIT_BUREAU_QRT": 0.0,
            "OWN_CAR_AGE": 8.0,
            "bureau_DAYS_CREDIT_ENDDATE_max": 1043.0,
            "prev_CNT_PAYMENT_mean": 36.0,
            "BASEMENTAREA_AVG": 0.092500,
            "LANDAREA_AVG": 0.127900,
            "bureau_AMT_CREDIT_SUM_DEBT_min": 0.0,
            "FLAG_OWN_CAR": 1,
            "ORGANIZATION_TYPE_Self-employed": 0,
            "FLOORSMIN_AVG": 0.208300,
            "FLOORSMAX_AVG": 0.166700,
            "DAYS_BIRTH": -16499,
        },
    }

    response = client.post("/df/add/", json=df)
    assert response.status_code == 200


# Negative case - validation pattern - adding non-numeric values. However, this is valid only for bot.
# In GUI there is no chance to enter non-numeric values for DF due to numeric input.
def test_df_with_validation_errors(client: TestClient):
    df = {
        "userid": 1,
        "dataset": {
            "bureau_AMT_CREDIT_SUM_min": "0.0",
            "prev_SELLERPLACE_AREA_min": "fff",
            "AMT_INCOME_TOTAL": 261000.0,
            "prev_AMT_DOWN_PAYMENT_mean": 0.0,
            "prev_WEEKDAY_APPR_PROCESS_START_SATURDAY_count_norm": 0.0,
            "bureau_AMT_CREDIT_SUM_DEBT_max": 638496.0,
            "bureau_DAYS_CREDIT_UPDATE_mean": -250.666667,
            "bureau_DAYS_CREDIT_UPDATE_max": -15.0,
            "prev_NAME_GOODS_CATEGORY_Furniture_count_norm": 0.0,
            "bureau_DAYS_ENDDATE_FACT_max": -813.0,
            "AMT_REQ_CREDIT_BUREAU_QRT": 0.0,
            "OWN_CAR_AGE": 8.0,
            "bureau_DAYS_CREDIT_ENDDATE_max": 1043.0,
            "prev_CNT_PAYMENT_mean": 36.0,
            "BASEMENTAREA_AVG": 0.092500,
            "LANDAREA_AVG": 0.127900,
            "bureau_AMT_CREDIT_SUM_DEBT_min": 0.0,
            "FLAG_OWN_CAR": 1,
            "ORGANIZATION_TYPE_Self-employed": 0,
            "FLOORSMIN_AVG": 0.208300,
            "FLOORSMAX_AVG": 0.166700,
            "DAYS_BIRTH": -16499,
            "NONLIVINGAREA_AVG": 0.017000,
            "APARTMENTS_AVG": 0.158800,
            "HOUSETYPE_MODE_block of flats": 1,
            "EXT_SOURCE_2": 0.552325,
            "NONLIVINGAPARTMENTS_AVG": 0.0,
            "YEARS_BUILD_AVG": 0.755200,
            "COMMONAREA_AVG": 0.019100,
            "YEARS_BEGINEXPLUATATION_AVG": 0.982100,
            "EXT_SOURCE_1": 0.560240,
            "EXT_SOURCE_3": 0.429424,
        },
    }

    response = client.post("/df/add/", json=df)
    assert response.status_code == 200
    assert response.json() == {"message": "Validation errors ['fff']"}


# Positive case - get df by its ID and check a zero prediction
def test_df_get(client: TestClient):
    response = client.get("/df/get/1")
    assert response.status_code == 200
    assert response.json()[1] == 0


# Negative case - get df by unknown ID
def test_df_get_error(client: TestClient):
    response = client.get("/df/get/101")
    assert response.status_code == 404
    assert response.json() == {"detail": "DF does not exist"}


# Only positive case - update DF with prediction value (only inside rm_worker crud operation, but we will imitate it)
def test_df_update_prediction(client: TestClient):
    prediction = {"prediction": 5}
    response = client.put("/df/edit/1", json=prediction)
    assert response.status_code == 200
    assert response.json() == {"message": "Prediction has been added, value: 5.0"}


# Just for correct test case, delete all previously created data
def test_delete_all(client: TestClient):
    response_df = client.delete("/df/")
    response_cli = client.delete("/user/")
    assert response_df.status_code == 200
    assert response_df.json() == {"message": "User DFs deleted successfully"}
    assert response_cli.status_code == 200
    assert response_cli.json() == {"message": "Users deleted successfully"}
