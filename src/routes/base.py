from fastapi import APIRouter, FastAPI, Depends
from helpers.config import get_settings, Settings

import os

from datatime import datatime

base_router = APIRouter(
    prefix="/api/v1",
    tags=["base", "api_v1"],
)

@base_router.get("/")
async def welcome_message(app_settings: Settings = Depends(get_settings)):

    
    '''app_name = os.getenv("APP_NAME")
    app_version = os.getenv("APP_VERSION")'''

    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION

 
    return {
        "app_name": app_name,
        "app_version": app_version,
        "datatime": datatime.now().strftime("%Y-%m-%d %H:%M:%S")
    }