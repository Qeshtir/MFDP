from models.userdf import UserDataFrame, UpdateUserDataFrame
from typing import List


def get_all_dfs(session) -> List[UserDataFrame]:
    return session.query(UserDataFrame).all()


def get_df_by_id(id: int, session) -> UserDataFrame:
    user_df = session.get(UserDataFrame, id)
    if user_df:
        return user_df
    return None


def update_df(id: int, new_data: UpdateUserDataFrame, session) -> UserDataFrame:
    user_df = session.get(UserDataFrame, id)
    if user_df:
        user_df_data = new_data.dict(exclude_unset=True)
    for key, value in user_df_data.items():
        setattr(user_df, key, value)

    session.add(user_df)
    session.commit()
    session.refresh(user_df)
    return user_df


def create_df(new_user_df: UserDataFrame, session) -> None:
    session.add(new_user_df)
    session.commit()
    session.refresh(new_user_df)


def delete_all_dfs(session) -> None:
    session.query(UserDataFrame).delete()
    session.commit()


def delete_dfs_by_id(id: int, session) -> None:
    user_df = session.get(UserDataFrame, id)
    if user_df:
        session.delete(user_df)
        session.commit()
        return

    raise Exception("User DF with supplied ID does not exist")
