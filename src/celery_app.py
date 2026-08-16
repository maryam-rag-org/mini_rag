from celery import Celery
from helpers.config import get_settings

settings = get_settings()

# Celery app  instance
celery_app = Celery(
    "minirag",
    broker  = settings.CELERY_BROKER_URL,
    backend = settings.CELERY_RESULT_BACKEND,
    include = [ # list of modules to import when the Celery worker starts
        "tasks.mail_service"
        ] 
)

# Conf Celery with essential settings

celery_app.conf.update(
    task_serializer=settings.CELERY_TASK_SERIALIZER,
    result_serializer=settings.CELERY_TASK_SERIALIZER,
    accept_content=[
        settings.CELERY_TASK_SERIALIZER
    ],
    # Task safty - late ack prevents task loss on worker crash
    task_acks_late=settings.CELERY_TASK_ACKS_LATE,

    # Time limits - Prevent hanging tasks
    task_time_limit = settings.CELERY_TASK_TIME_LIMIT,

    #Result backend - store results for ststus tracking
    task_ignore_result=False,
    result_expires=3600,

    # worker settings
    worker_concurrency=settings.CELERY_WORKER_CONCURRENCY,

    # Connection stteings for better reliaiblity
    broker_connection_retry_on_startup=True,
    broker_connection_retry=True, # case loss the connection while working 
    broker_connection_max_retries=10,
    worker_cancel_long_running_tasks_on_connection_loss=True,


    task_routes = {
        "tasks.mail_service.send_email_reports": {"queue": "mail_server_queue"},
    },
)


celery_app.conf.task_default_queue = "default" # name of the queue


