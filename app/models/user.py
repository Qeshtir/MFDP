from sqlmodel import Field, SQLModel, MetaData
from typing import Optional
from pydantic import BaseModel


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int = Field(default=None, primary_key=True, nullable=False)
    firstname: str
    lastname: str
    login: str
    password: str
    role: str

    def __init__(self, firstname, lastname, login, password, role):
        super().__init__()
        self.firstname = firstname
        self.lastname = lastname
        self.login = login
        self.password = password
        self.role = role


class UserUpdate(SQLModel):
    firstname: Optional[str]
    lastname: Optional[str]
    password: Optional[str]
    login: Optional[str]
    role: Optional[str]


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserSignIn(SQLModel):
    email: str
    password: str
