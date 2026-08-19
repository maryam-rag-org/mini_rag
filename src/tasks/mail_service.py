from celery_app import celery_app
from helpers.config import get_settings, Settings

from time import sleep
import asyncio # call asyncio.run() to run async function in sync context
from datetime import datetime
import logging


logger = logging.getLogger("celery.task")

@celery_app.task(bind=True, name="tasks.mail_service.send_email_reports",)
def send_email_reports(self, mail_wait_seconds: int):
    return asyncio.run(_send_email_reports(self, mail_wait_seconds))



async def _send_email_reports(task_instance, mail_wait_seconds: int):

    started_at = str(datetime.now())

    task_instance.update_state(
         state="PROGRESS",
         meta={
              "started_at": started_at,
         }
    )

    # Simulate sending email reports with a delay
    for i in range(15):
            logger.info(f"Sending email to user {i+1} ")
            await asyncio.sleep(mail_wait_seconds)
    # END of the task

    return {
         "num_emails":15,
         "started_at": started_at,
         "ended_at": str(datetime.now())
    }



