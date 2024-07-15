from fastapi import APIRouter, HTTPException, Depends, status, Body
from models.user import User, TokenResponse
from auth.hash_password import HashPassword
from database.database import get_session
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt_handler import create_access_token
from typing import Annotated
from auth.authenticate import authenticate

from services.crud import users as UsersService

user_router = APIRouter(tags=["User"])
hash_password = HashPassword()


@user_router.post("/signup")
async def sign_new_user(
    user: Annotated[
        User,
        Body(
            openapi_examples={
                "admin": {
                    "summary": "Admin",
                    "description": "An **admin** role user creation.",
                    "value": {
                        "firstname": "Igor",
                        "lastname": "Makarov",
                        "login": "SomeLogin",
                        "password": "!strong_AS_plnd!",
                        "role": "admin",
                    },
                },
                "demo_user": {
                    "summary": "User",
                    "description": "A **user** role user creation.",
                    "value": {
                        "firstname": "Demo",
                        "lastname": "User",
                        "login": "DemoLogin",
                        "password": "demo",
                        "role": "user",
                    },
                },
            },
        ),
    ],
    session=Depends(get_session),
) -> dict:
    user_exist = UsersService.get_user_by_login(user.login, session)

    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with login provided exists already.",
        )

    hashed_password = hash_password.create_hash(user.password)
    user.password = hashed_password
    UsersService.create_user(user, session)

    return {"message": "User created successfully"}


@user_router.post("/signin", response_model=TokenResponse)
async def sign_user_in(
    user: OAuth2PasswordRequestForm = Depends(), session=Depends(get_session)
) -> dict:
    user_exist = UsersService.get_user_by_login(user.username, session)

    if user_exist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )

    if hash_password.verify_hash(user.password, user_exist.password):
        access_token = create_access_token(user_exist.id)
        return {"access_token": access_token, "token_type": "Bearer"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid details passed."
    )


# only for test purpose - deleting users from cache_db. Be aware of using this in other cases!
@user_router.delete("/")
async def delete_all_users(
    user: str = Depends(authenticate), session=Depends(get_session)
):
    UsersService.delete_all_users(session)
    return {"message": "Users deleted successfully"}
