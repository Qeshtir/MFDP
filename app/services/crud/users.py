from models.user import User, UserUpdate
from typing import List


def get_all_users(session) -> List[User]:
    return session.query(User).all()


def get_user_by_id(id: int, session) -> User:
    user = session.get(User, id)
    if user:
        return user
    return None


def update_user(id: int, new_data: UserUpdate, session) -> User:
    user = session.get(User, id)
    if user:
        user_data = new_data.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def create_user(new_user: User, session) -> None:
    session.add(new_user)
    session.commit()
    session.refresh(new_user)


def delete_all_users(session) -> None:
    session.query(User).delete()
    session.commit()


def delete_users_by_id(id: int, session) -> None:
    user = session.get(User, id)
    if user:
        session.delete(user)
        session.commit()
        return

    raise Exception("User with supplied ID does not exist")


def get_user_by_login(login: str, session) -> User:
    user = session.query(User).filter(User.login == login).first()
    if user:
        return user
    return None
