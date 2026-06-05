from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv(".env")  # ".env" is the default filename for environment variables

# all the routers files will see thr .env file and can access the environment variables defined in it
from routers.base import base_router

app = FastAPI()

app.include_router(base_router)
