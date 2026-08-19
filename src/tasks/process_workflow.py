from celery import chain
from celery_app import celery_app, get_setup_utils
from helpers.config import get_settings

from tasks.file_processing import process_project_file
from tasks.data_indexing import _index_data_content


import asyncio

import logging

logger = logging.getLogger('celery.task')

################# SECONDE NODE IN CHAIN #################

@celery_app.task(name="tasks.process_workflow.push_after_process_task", bind=True,
                 autoretry_for=(Exception,),
                 retry_kwargs={'max_retries': 3, 'countdown': 60})
def push_after_process_task(self, prev_task_result):

    project_id = prev_task_result.get("project_id")
    do_reset = prev_task_result.get("do_reset")

    task_results = asyncio.run(
        _index_data_content(self, project_id, do_reset)
    )

    return {
        "task_results": task_results,
        "project_id": project_id,
        "do_reset": do_reset
    }


################# FIRST NODE IN CHAIN #################
# Chain of task --> process project then push indexing 
@celery_app.task(name="tasks.process_workflow.process_and_push_workflow", bind=True,
                 autoretry_for=(Exception,),
                 retry_kwargs={'max_retries': 3, 'countdown': 60})
def process_and_push_workflow(self, project_id:int,
                              file_id:int, chunk_size:int,
                              overlap_size:int, do_reset:int):

    workflow = chain(
        # .s ==> call functions one by one and take the output as an input to the next task
        process_project_file.s(project_id, file_id, chunk_size, overlap_size, do_reset), # arguments to function should be sorted
        push_after_process_task.s() # NO INPUT AUTO TAKE FROM the first node
    )

    result = workflow.apply_async()

    return {
        "signal": "WORKFLOW_STATED",
        "workflow_id" : result.id,
        "tasks": ["tasks.file_processing.process_project_file", 
                  "tasks.data_indexing.index_data_content"]
    }
    