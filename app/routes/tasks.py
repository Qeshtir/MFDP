from fastapi import APIRouter, Body, Depends, HTTPException, status
from database.database import get_session
from models.task import Task
from typing import Annotated
from sqlalchemy.orm import Session
from routes.dataframes import check_dataframe
from services.crud import tasks as TasksService
from auth.authenticate import authenticate
import pickle
import uuid
import pika
from services.ml.params import connection_params

task_router = APIRouter(tags=["Task"])


@task_router.get("/get/{id}", response_model=Task)
async def get_task(id: int, db: Session = Depends(get_session)):
    task = TasksService.get_task_by_id(id, db)
    if task:
        return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task with supplied ID does not exist",
    )


@task_router.post("/execute/")
async def execute_task(
    task: Annotated[
        Task,
        Body(
            openapi_examples={
                "full_df": {
                    "summary": "A valid task object",
                    "description": "Dataframe should be a valid dict object of straight these params",
                    "value": {
                        "userid": 1,
                        "user_df_id": 1,
                        "status": "created",
                    },
                },
            },
        ),
    ],
    user: str = Depends(authenticate),
):
    # logic for the task execution.
    # Установка соединения
    connection = pika.BlockingConnection(connection_params)

    # Создание канала
    channel = connection.channel()

    # Имя очереди
    queue_name = "predictions"
    queue_callback = "predictions_callback"

    # Отправка сообщения
    channel.queue_declare(queue=queue_name)  # Создание очереди (если не существует)
    channel.queue_declare(queue=queue_callback)  # Создание очереди (если не существует)

    corr_id = uuid.uuid4()
    callback_to = queue_callback

    message_obj = {"task": task, "corr_id": corr_id, "callback": callback_to}

    message = pickle.dumps(message_obj)
    channel.basic_publish(exchange="", routing_key=queue_name, body=message)

    print(f"Sent: '{task}'")

    # Ожидаем callback по corr_id
    def callback(ch, method, properties, body):
        message = pickle.loads(body)
        if message == corr_id:
            print("We got it")
            # Закрытие соединения
            ch.basic_ack(
                delivery_tag=method.delivery_tag
            )  # Ручное подтверждение обработки сообщения
            connection.close()

    channel.basic_consume(
        queue=queue_callback,
        on_message_callback=callback,
        auto_ack=False,  # Автоматическое подтверждение обработки сообщений
    )

    print("Waiting for messages")
    channel.start_consuming()
    return {"message": f"Task has been completed. Please update prediction data."}


@task_router.post("/create/")
async def create_task(
    task: Annotated[
        Task,
        Body(
            openapi_examples={
                "full_df": {
                    "summary": "A valid task object",
                    "description": "Dataframe should be a valid dict object of straight these params",
                    "value": {
                        "userid": 1,
                        "user_df_id": 1,
                        "status": "created",
                    },
                },
            },
        ),
    ],

    db: Session = Depends(get_session),
    user: str = Depends(authenticate),
):
    TasksService.create_task(task, db)
    return {"message": f"Task has been added", "id": task.id}

@task_router.delete("/{id}")
async def delete_task(
    id: int, db: Session = Depends(get_session), user: str = Depends(authenticate)
) -> dict:
    try:
        TasksService.delete_tasks_by_id(id, db)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tasks with supplied ID does not exist",
        )

    return {"message": "Task deleted successfully"}


@task_router.get("/history/{user_id}")
async def task_history(
    user_id: int, db: Session = Depends(get_session), user: str = Depends(authenticate)
):
    task_list = []
    task = TasksService.get_task_by_user_id(user_id, db)
    for t in task:
        u_df = await check_dataframe(t.user_df_id, db)
        result_dict = {
            "#": t.id,
            "data": u_df[0],
            "prediction": u_df[1],
            "operation_start": t.start_date,
            "operation_finish": t.end_date,
            "operation_status": t.status,
        }
        task_list.append(result_dict)
    return task_list


@task_router.delete("/")
async def delete_all_tasks(
    db: Session = Depends(get_session), user: str = Depends(authenticate)
) -> dict:
    TasksService.delete_all_tasks(db)
    return {"message": "Tasks deleted successfully"}
