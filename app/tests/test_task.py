from fastapi.testclient import TestClient

# These imports only for proper imitation of rmworker module
from models.task import Task
from services.crud import tasks as TasksService

# from database.database import get_session_for_bot
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool

# from conftest import session_fixture as session
import datetime


# Т.к. роут task/execute/ не имеет под собой никакой логики, кроме работы с RMQ в части постановки задач воркеру, имеет
# смысл проверять исключительно работу воркера. Воркер является standalone приложением, поэтому логика его работы будет
# сымитирована в нескольких самых общих сценариях, повторяющих его флоу.


# Небольшой фикс для сессии crud, т.к. фикстуры сессии работают только с fastAPI, а мы имитируем специфичную воркеру
# работу с задачами.
def session_fix():
    engine = create_engine(
        "sqlite:///testing.db",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return Session(engine)


# Positive case. Let's imitate task creation (its all async with RMQ realization)
def test_task_creation(client: TestClient):
    # Create user
    user = {
        "firstname": "Demo",
        "lastname": "User",
        "login": "DemoLogin",
        "password": "demo",
        "role": "user",
    }

    client.post("/user/signup", json=user)

    # Create DF
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
    client.post("/df/add/", json=df)

    # Imitate prediction
    prediction = {"prediction": 5}
    client.put("/df/edit/1", json=prediction)

    # Task create and update all in one
    session = session_fix()
    task = Task(
        userid=1,
        user_df_id=1,
        status="done",
        end_date=datetime.datetime.now(),
    )
    TasksService.create_task(task, session)

    # Get history of one task
    response = client.get("/task/history/1")

    assert response.status_code == 200
    assert response.json()[0]["operation_status"] == "done"


# Negative case - imitate rejection. It's only future-case test, bcause rejection appears to be only with
# transaction model, which is not implemented in this realization of service, but can be added at any time
def test_task_creation_negative(client: TestClient):
    # Imitate rejection
    session = session_fix()
    task = Task(
        userid=1,
        user_df_id=1,
        status="rejected",
        end_date=datetime.datetime.now(),
    )
    TasksService.create_task(task, session)

    # Get history of all tasks
    response = client.get("/task/history/1")

    assert response.status_code == 200
    assert response.json()[0]["operation_status"] == "done"
    assert response.json()[1]["operation_status"] == "rejected"


# Just for correct test case, delete all previously created data
def test_delete_all(client: TestClient):
    response_df = client.delete("/df/")
    response_cli = client.delete("/user/")
    assert response_df.status_code == 200
    assert response_df.json() == {"message": "User DFs deleted successfully"}
    assert response_cli.status_code == 200
    assert response_cli.json() == {"message": "Users deleted successfully"}
