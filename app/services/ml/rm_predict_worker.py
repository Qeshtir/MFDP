import pika

from params import connection_params
from database.database import get_session_for_bot
from models.userdf import UpdateUserDataFrame
from services.crud import dataframes as DFService
from services.crud import tasks as TasksService

# Ни в коем случае нельзя трогать следующие импорты - удаление "неиспользуемых" провоцирует ошибку ORM, которую очень
# трудно отловить.
# -----
from models.task import UpdateTask, Task
from models.user import User
from models.userdf import UserDataFrame
# -----

import joblib
import pickle
import pandas as pd
import datetime
from decouple import config

import warnings

warnings.filterwarnings("ignore")

model_path = config("MODEL_PATH")

# Установка соединения
connection = pika.BlockingConnection(connection_params)

# Создание канала
channel = connection.channel()

# Имя очереди
queue_name = "predictions"
channel.queue_declare(queue=queue_name)  # Создание очереди (если не существует)

# Функции, которая будет вызвана при получении сообщения

#  load model
model = joblib.load(model_path)


def make_prediction(ch, method, properties, body):
    message = pickle.loads(body)
    task = message["task"]
    session = get_session_for_bot()
    user_df = task.user_df_id

    TasksService.create_task(task, session)

    #  make a prediction
    df = DFService.get_df_by_id(user_df, session)
    df = pickle.loads(df.dataset)
    valid_df = pd.DataFrame(df, index=[0])

    # Предсказание по единице
    predict = model.predict_proba(valid_df)[0][1]

    # update df
    DFService.update_df(user_df, UpdateUserDataFrame(prediction=predict), session)

    # update task
    TasksService.update_task(
        task.id,
        UpdateTask(
            status="done",
            end_date=datetime.datetime.now(),
        ),
        session,
    )

    return {"message": f"Task {task.id} has been completed"}


def make_callback(ch, method, properties, body):
    # Логика простая - если мы выполнили задачу (сделали предикт или не прошли по балансу), отправляем коллбэк

    message = pickle.loads(body)
    queue_name = message["callback"]
    corr_id = message["corr_id"]
    answer = pickle.dumps(corr_id)

    channel.basic_publish(exchange="", routing_key=queue_name, body=answer)
    ch.basic_ack(
        delivery_tag=method.delivery_tag
    )  # Ручное подтверждение обработки сообщения
    print("Done")


def callback(ch, method, properties, body):
    make_prediction(ch, method, properties, body)
    make_callback(ch, method, properties, body)


# Подписка на очередь и установка обработчика сообщений


def start_consuming_ml():
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=False,  # Автоматическое подтверждение обработки сообщений
    )
    print("Waiting for messages. To exit, press Ctrl+C")
    channel.start_consuming()


if __name__ == "__main__":
    start_consuming_ml()
