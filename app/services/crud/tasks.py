from models.task import Task, UpdateTask
from typing import List


def get_all_tasks(session) -> List[Task]:
    return session.query(Task).all()


def get_task_by_id(id: int, session) -> Task:
    task = session.get(Task, id)
    if task:
        return task
    return None


def get_task_by_user_id(id: int, session) -> List[Task]:
    return session.query(Task).filter(Task.userid == id).all()


def update_task(id: int, new_data: UpdateTask, session) -> Task:
    task = session.get(Task, id)
    if task:
        task_data = new_data.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def create_task(new_task: Task, session) -> None:
    session.add(new_task)
    session.commit()
    session.refresh(new_task)


def delete_all_tasks(session) -> None:
    session.query(Task).delete()
    session.commit()


def delete_tasks_by_id(id: int, session) -> None:
    task = session.get(Task, id)
    if task:
        session.delete(task)
        session.commit()
        return

    raise Exception("Task with supplied ID does not exist")
