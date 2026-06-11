from fastapi import FastAPI

# all the routers files will see thr .env file and can access the environment variables defined in it
from routers.base import base_router
from routers.data import data_router

app = FastAPI()

app.include_router(base_router)
app.include_router(data_router)
