from fastapi import APIRouter, Body, Depends, HTTPException, status
from database.database import get_session
from models.userdf import UserDataFrame, UpdateUserDataFrame
from typing import Annotated
import pickle
from sqlalchemy.orm import Session
from services.crud import dataframes as DFService
from services.crud import users as UsersService
from auth.authenticate import authenticate

dataframe_router = APIRouter(tags=["Dataframe"])


@dataframe_router.get("/get/{id}")
async def check_dataframe(id: int, db: Session = Depends(get_session)):
    df = DFService.get_df_by_id(id, db)
    if df is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="DF does not exist"
        )
    u_df = pickle.loads(df.dataset)
    response_obj = u_df.to_dict("records")
    response_obj.append(df.prediction)
    return response_obj


@dataframe_router.post("/add/")
async def add_dataframe(
    dataframe: Annotated[
        UserDataFrame,
        Body(
            openapi_examples={
                "full_df": {
                    "summary": "A valid dataframe object",
                    "description": "Dataframe should be a valid dict object of straight these params",
                    "value": {
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
                    },
                },
            },
        ),
    ],
    db: Session = Depends(get_session),
    user: str = Depends(authenticate),
):
    user_exist = UsersService.get_user_by_id(dataframe.userid, db)
    if user_exist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )

    validation = dataframe.validate_data()
    if validation:
        return {"message": f"Validation errors {validation}"}
    dataframe.serialize()
    DFService.create_df(dataframe, db)
    return {"message": f"Dataframe has been added", "id": dataframe.id}


@dataframe_router.put("/edit/{id}")
async def edit_df(
    id: int,
    dataframe: Annotated[
        UpdateUserDataFrame,
        Body(
            openapi_examples={
                "user": {
                    "summary": "Normal user",
                    "description": "Typical user update.",
                    "value": {
                        "prediction": 5,
                    },
                },
            },
        ),
    ],
    db: Session = Depends(get_session),
    user: str = Depends(authenticate),
):
    user_df = DFService.update_df(id, dataframe, db)
    if user_df:
        u_df = pickle.loads(user_df.dataset)
        response_obj = u_df.to_dict("records")
        response_obj.append(user_df.prediction)
        return {"message": f"Prediction has been added, value: {response_obj[1]}"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User DF with supplied ID does not exist",
    )


@dataframe_router.delete("/{id}")
async def delete_df(
    id: int, session: Session = Depends(get_session), user: str = Depends(authenticate)
) -> dict:
    try:
        DFService.delete_dfs_by_id(id, session)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User DF with supplied ID does not exist",
        )

    return {"message": "User DF deleted successfully"}


@dataframe_router.delete("/")
async def delete_all_dfs(
    session: Session = Depends(get_session), user: str = Depends(authenticate)
) -> dict:
    DFService.delete_all_dfs(session)
    return {"message": "User DFs deleted successfully"}
