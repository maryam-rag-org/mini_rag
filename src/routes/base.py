from fastapi import APIRouter, FastAPI, Depends
from helpers.config import get_settings, Settings

from tasks.mail_service import send_email_reports

import os
from time import sleep
import logging

logger = logging.getLogger("uvicorn.error")

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
    }


@base_router.get("/send_reports")
async def send_reports(app_settings: Settings = Depends(get_settings)):

    task =  send_email_reports.delay(mail_wait_seconds=3) # will be executed in the background by celery worker

    return {
        "success": True,
        "task_id": task.id,
        }

    