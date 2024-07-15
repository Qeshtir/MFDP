from sqlmodel import Field, SQLModel, MetaData
from sqlalchemy import LargeBinary
from typing import Optional
import pandas as pd
import pickle


class UserDataFrame(SQLModel, table=True):
    __tablename__ = "dataframes"
    id: int = Field(default=None, primary_key=True, nullable=False)
    userid: int = Field(default=None, foreign_key="users.id")
    dataset: bytes = LargeBinary()
    prediction: float = Field(default=0, nullable=False)

    def __init__(
        self,
        userid,
        prediction=None,
        dataset=None,
    ):
        super().__init__()
        self.userid = userid
        self.dataset = dataset
        self.prediction = prediction  # Should be None for data init

    def validate_data(self):
        # data is a dict with certain fields required. Type and requirements are checked via front, but this is a
        # doblecheck method
        # also this method should be used before any serialization

        # columns consistency check
        """
        'bureau_AMT_CREDIT_SUM_min', 'prev_SELLERPLACE_AREA_min',
        'AMT_INCOME_TOTAL', 'prev_AMT_DOWN_PAYMENT_mean',
        'prev_WEEKDAY_APPR_PROCESS_START_SATURDAY_count_norm',
        'bureau_AMT_CREDIT_SUM_DEBT_max', 'bureau_DAYS_CREDIT_UPDATE_mean',
        'bureau_DAYS_CREDIT_UPDATE_max',
        'prev_NAME_GOODS_CATEGORY_Furniture_count_norm',
        'bureau_DAYS_ENDDATE_FACT_max', 'AMT_REQ_CREDIT_BUREAU_QRT',
        'OWN_CAR_AGE', 'bureau_DAYS_CREDIT_ENDDATE_max',
        'prev_CNT_PAYMENT_mean', 'BASEMENTAREA_AVG', 'LANDAREA_AVG',
        'bureau_AMT_CREDIT_SUM_DEBT_min', 'FLAG_OWN_CAR',
        'ORGANIZATION_TYPE_Self-employed', 'FLOORSMIN_AVG', 'FLOORSMAX_AVG',
        'DAYS_BIRTH', 'NONLIVINGAREA_AVG', 'APARTMENTS_AVG',
        'HOUSETYPE_MODE_block of flats', 'EXT_SOURCE_2',
        'NONLIVINGAPARTMENTS_AVG', 'YEARS_BUILD_AVG', 'COMMONAREA_AVG',
        'YEARS_BEGINEXPLUATATION_AVG', 'EXT_SOURCE_1', 'EXT_SOURCE_3'
        """

        validation_dict = {
            "bureau_AMT_CREDIT_SUM_min": 0,
            "prev_SELLERPLACE_AREA_min": 0,
            "AMT_INCOME_TOTAL": 0,
            "prev_AMT_DOWN_PAYMENT_mean": 0,
            "prev_WEEKDAY_APPR_PROCESS_START_SATURDAY_count_norm": 0,
            "bureau_AMT_CREDIT_SUM_DEBT_max": 0,
            "bureau_DAYS_CREDIT_UPDATE_mean": 0,
            "bureau_DAYS_CREDIT_UPDATE_max": 0,
            "prev_NAME_GOODS_CATEGORY_Furniture_count_norm": 0,
            "bureau_DAYS_ENDDATE_FACT_max": 0,
            "AMT_REQ_CREDIT_BUREAU_QRT": 0,
            "OWN_CAR_AGE": 0,
            "bureau_DAYS_CREDIT_ENDDATE_max": 0,
            "prev_CNT_PAYMENT_mean": 0,
            "BASEMENTAREA_AVG": 0,
            "LANDAREA_AVG": 0,
            "bureau_AMT_CREDIT_SUM_DEBT_min": 0,
            "FLAG_OWN_CAR": 0,
            "ORGANIZATION_TYPE_Self-employed": 0,
            "FLOORSMIN_AVG": 0,
            "FLOORSMAX_AVG": 0,
            "DAYS_BIRTH": 0,
            "NONLIVINGAREA_AVG": 0,
            "APARTMENTS_AVG": 0,
            "HOUSETYPE_MODE_block of flats": 0,
            "EXT_SOURCE_2": 0,
            "NONLIVINGAPARTMENTS_AVG": 0,
            "YEARS_BUILD_AVG": 0,
            "COMMONAREA_AVG": 0,
            "YEARS_BEGINEXPLUATATION_AVG": 0,
            "EXT_SOURCE_1": 0,
            "EXT_SOURCE_3": 0,
        }
        # search for inconsistent keys and add 0 to such values

        for key in validation_dict.keys():
            if key in self.dataset.keys():
                continue
            self.dataset[key] = 0
        print("Keys are fine")

        # value checking
        values_for_adding = []

        def isNumeric(val):
            if isinstance(val, (int, float)):
                return True
            try:
                float(val)
            except ValueError:
                # неверный тип, ошибка приведения
                return False
            except TypeError:
                # верный тип None
                return True
            else:
                return True

        for v in self.dataset.values():
            if isNumeric(v):
                continue
            values_for_adding.append(v)
        if values_for_adding:
            print(f"validation errors {values_for_adding}")
            return values_for_adding
        print("Values are fine")
        return None

    def serialize(self):
        # data should be a valid dict object
        dataset = pd.DataFrame(self.dataset, index=[0])

        # NoneType is appliable for our model, so we just change a type of object columns to float
        object_columns = dataset.loc[:, dataset.dtypes == object].columns
        dataset[object_columns] = dataset[object_columns].astype('float')

        self.dataset = pickle.dumps(dataset)


class UpdateUserDataFrame(SQLModel):
    prediction: Optional[float]
