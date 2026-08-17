from celery_app import celery_app, get_setup_utils
from helpers.config import get_settings

from controllers import ProcessController, NLPController

from models import ResponseSignal
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.AssetModel import AssetModel


from models.db_schemes import DataChunk

from models.enums.AssetTypeEnum import AssetTypeEnum


import asyncio
import json

import logging

logger = logging.getLogger('celery.task')

@celery_app.task(name="tasks.file_processing.process_project_file", bind=True,
                 autoretry_for=(Exception,),
                 retry_kwargs={'max_retries': 3, 'countdown': 60})
def process_project_file(self, project_id: int, 
                                     file_id: str, 
                                     chunk_size: int, 
                                     overlap: int, 
                                     do_reset: bool):

    return asyncio.run(
        _process_project_file(self, project_id=project_id,file_id=file_id,
                                    chunk_size=chunk_size, overlap=overlap, do_reset=do_reset)
        )

async def _process_project_file(task_instance, project_id: int, 
                                     file_id: str, 
                                     chunk_size: int, 
                                     overlap: int, 
                                     do_reset: bool):

    db_engine, vectordb_client = None, None

    try:
        (db_engine, db_client, llm_provider_factory, 
        vectordb_provider_factory,generation_client, 
        embedding_client, vectordb_client, template_parser) = await get_setup_utils()

        
        project_model = await ProjectModel.create_instance(
                db_client=db_client
            )

        project = await project_model.get_project_or_create_one(
                project_id=project_id
            )
        
        nlp_controller = NLPController(
            vectordb_client= vectordb_client,
            generation_client= generation_client,
            embedding_client= embedding_client,
            template_parser= template_parser
        )
        
        asset_model = await AssetModel.create_instance(
                db_client=db_client
            )
        
        project_file_ids = {}

        if file_id:
            asset_record = await asset_model.get_asset_record(
                asset_project_id=project.project_id,
                asset_name=file_id
            )

            if asset_record is None:
                # update task instance state to indicate failure
                task_instance.update_state(
                    state='FAILURE',
                    meta={'signal': ResponseSignal.FILE_ID_ERROR.value}
                )

                raise Exception(f"File with ID {file_id} not found in project {project.project_id}")
                
                
            project_file_ids = {
                asset_record.asset_id:asset_record.asset_name
                }

        else:
            
            
            project_file = await asset_model.get_all_project_assets(
                asset_project_id = project.project_id,
                asset_type = AssetTypeEnum.FILE.value
                )
            
            project_file_ids = {
                
                record.asset_id:record.asset_name 
                for record in project_file
            }

        if len(project_file_ids) == 0:

            task_instance.update_state(
                state='FAILURE',
                meta={'signal': ResponseSignal.NO_FILES_ERROR.value}
            )

            raise Exception(f"No files found in project {project.project_id}")

        
        process_controller = ProcessController(project_id = project_id)

        chunk_model = await ChunkModel.create_instance(
                db_client=db_client
            )

        if do_reset == 1:
                # delete vectors collection
                collection_name = nlp_controller.create_collection_name(project_id=project.project_id)
                _ = await vectordb_client.delete_collection(collection_name = collection_name)

                # delete chunks
                _ = await chunk_model.delete_chunks_by_project_id(
                    project_id=project.project_id
                    )
                

                

        num_records = 0
        num_files = 0

        for asset_id, file_id in project_file_ids.items():

            file_content = process_controller.get_file_content(file_id=file_id)

            if file_content is None:
                logger.error(f"Error while processing file {file_id}")
                continue
            


            file_chunks = process_controller.process_file_content(
                                    file_content=file_content,
                                    file_id=file_id,
                                    chunk_size=chunk_size,
                                    chunk_overlap=overlap
                                    )

            if file_chunks is None or len(file_chunks) == 0:
                logger.error(f"No chunks found for file {file_id}")
                continue
        
            file_chunks_records = [
                DataChunk(
                    chunk_text= chunk.page_content,
                    chunk_metadata=chunk.metadata,
                    chunk_order = i+1,
                    chunk_project_id =  project.project_id,
                    chunk_asset_id = asset_id

                )
                for i, chunk in enumerate(file_chunks)
            ]
            
            
                
            num_records += await chunk_model.insert_many_chunks(chunks=file_chunks_records)
            num_files += 1

        task_instance.update_state(
            state='SUCCESS',
            meta={
                "signal": ResponseSignal.PROCESSING_SUCCESS.value,
                }
            )
        logger.warning(f"Task completed successfully for project {project.project_id} with {num_records} chunks inserted from {num_files} files.")

        return {
                "signal": ResponseSignal.PROCESSING_SUCCESS.value,
                "inserted_chuncks": num_records,
                "processed_files": num_files
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
        