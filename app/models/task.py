from sqlmodel import Field, SQLModel, MetaData
from typing import Optional
import datetime


class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    id: int = Field(default=None, primary_key=True, nullable=False)
    userid: int = Field(default=None, foreign_key="users.id", nullable=False)
    user_df_id: int = Field(default=None, foreign_key="dataframes.id", nullable=False)
    status: str
    start_date: datetime.datetime
    end_date: datetime.datetime = Field(default=None, nullable=True)

    def __init__(
        self,
        userid,
        user_df_id,
        status,
        start_date=datetime.datetime.now(),
        end_date=None,
    ):
        super().__init__()
        self.userid = userid
        self.user_df_id = user_df_id
        self.status = status
        self.start_date = start_date
        self.end_date = end_date


class UpdateTask(SQLModel):
    status: Optional[str]
    end_date: Optional[datetime.datetime]
