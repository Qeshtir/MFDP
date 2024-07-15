from fastapi import FastAPI
from database.database import conn
from routes.users import user_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from routes.dataframes import dataframe_router
from routes.tasks import task_router
import uvicorn

# for handling None in JSON response use ORJSONResponse
app = FastAPI(default_response_class=ORJSONResponse)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    conn()


# Register routes
app.include_router(user_router, prefix="/user")
app.include_router(dataframe_router, prefix="/df")
app.include_router(task_router, prefix="/task")


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8080, reload=True)
