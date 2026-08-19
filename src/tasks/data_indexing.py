from celery_app import celery_app, get_setup_utils
from helpers.config import get_settings

from routes.schemes.nlp import PushRequest, SearchRequest

from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models import ResponseSignal

from controllers import NLPController

from tqdm.auto import tqdm

import asyncio
import json

import logging


logger = logging.getLogger('celery.task')

@celery_app.task(
        bind=True, name = "tasks.data_indexing.index_data_content",
        autoretry_for=(Exception,),
        retry_kwargs={'max_retries': 3, 'countdown':60}
)
def index_data_content(self, project_id: int ,do_reset: int):

    return asyncio.run(
        _index_data_content(self, project_id, do_reset)
    )




async def _index_data_content(task_instance, project_id: int ,do_reset: int):


    db_engine, vectordb_client = None, None
    
    try:
                (db_engine, db_client, llm_provider_factory, 
                vectordb_provider_factory,generation_client, 
                embedding_client, vectordb_client, template_parser) = await get_setup_utils()

                logger.warning("Setrup utils were loaded!")

                project_model = await ProjectModel.create_instance(
                        db_client=db_client
                    )
                chunk_model = await ChunkModel.create_instance(
                      db_client=db_client
                )
            
                project = await project_model.get_project_or_create_one(
                    project_id=project_id
                )
            
                if not project:
                    task_instance.update_stste(
                         state = 'FAILURE',
                         meta={
                              "signal": ResponseSignal.PROJECT_NOT_FOUND_ERROR.value
                         }
                    )

                    raise Exception(f"No project found for project id: {project_id}")
                  
                nlp_controller = NLPController(
                    vectordb_client=vectordb_client,
                    generation_client=generation_client,
                    embedding_client=embedding_client,
                    template_parser = template_parser
                )
            
                has_recordes = True
                page_no = 1
                inserted_items_count = 0
                idx = 0
            
            
                # check the collection
                collection_name = nlp_controller.create_collection_name(project_id=project.project_id)
            
                _ = await vectordb_client.create_collection(
                    collection_name = collection_name,
                    embedding_size = embedding_client.embedding_size,
                    do_reset = do_reset
                )
            
                # setup batching and progress bar
                total_chunks_count = await chunk_model.get_total_chunks_count(project_id=project.project_id)
            
                pbar = tqdm(total=total_chunks_count, desc="Vector Indexing", position=0)
            
                while has_recordes:
            
                    page_chunks = await chunk_model.get_project_chunks(project_id=project.project_id, page_no=page_no)
                    
                    if not page_chunks or len(page_chunks) == 0:
                        has_recordes = False
                        break
                    
                    chunks_ids = [c.chunk_id for c in page_chunks]
                    
                    do_reset = do_reset
                    if page_no != 1:
                        do_reset = False
            
                    is_inserted = await nlp_controller.index_into_vector_db( 
                        project = project,
                        chunks = page_chunks,
                        #do_reset = do_reset, No need for it it is done up
                        chunks_id= chunks_ids
                    )
            
                    if not is_inserted:
                        task_instance.update_stste(
                                state = 'FAILURE',
                                meta={
                                        "signal": ResponseSignal.INSERT_INTO_VECTORDB_ERROR.value
                                    }
                            )

                        raise Exception(f"Can not insert into VectorDB | project id: {project_id}")
                     
                    
                    pbar.update(len(page_chunks))
            
                    page_no += 1
                    inserted_items_count += len(page_chunks)
                    idx += len(page_chunks)
                    
               
                task_instance.update_state(
                    state='SUCCESS',
                            meta={
                                "signal": ResponseSignal.INSERT_INTO_VECTORDB_SUCCESS.value,
                            }
                            )
                logger.warning(f"Task completed successfully for project {project_id} with inserted items count = {inserted_items_count}.")

                
                return {
                        "signal": ResponseSignal.INSERT_INTO_VECTORDB_SUCCESS.value,
                        "inserted_items_count": inserted_items_count
                        }
    

    except Exception as e:
            logger.error(f"Task failed with error: {str(e)}")
            raise
    
    finally:
            try:
                if db_engine:
                    await db_engine.dispose()
                if vectordb_client:
                    await vectordb_client.disconnect()
            except Exception as e:
                logger.error(f"Error during cleanup: {str(e)}")