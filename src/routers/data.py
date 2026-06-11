from fastapi import APIRouter, FastAPI, Depends, UploadFile, File, status
from fastapi.responses import JSONResponse

from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController

import os
import aiofiles

from models import ResponseSignal

import logging

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["data", "api_v1"],
)

# upload pdf
@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, 
                      file: UploadFile,
                      app_settings: Settings = Depends(get_settings)):

        # check for file type and file size file properties  ==> logic SO in controllers
        data_controller = DataController()
        is_valid, result_signal = data_controller.validate_uploaded_file(file)

        if not is_valid:
            return JSONResponse(
                status_code = status.HTTP_400_BAD_REQUEST,
                content = {"signal": result_signal}
            )        

        project_dir_path = ProjectController().get_project_path(project_id = project_id)
        file_path, file_id = data_controller.generate_unique_file_path(original_file_name=file.filename, project_id = project_id)

        try:
            # open the  file as binary to save it in chunk
            async with aiofiles.open(file_path, 'wb') as f:
                while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                    await f.write(chunk)

        except Exception as e:

            logger.error(f"Error while uploading file: {e}")
            return JSONResponse(
                status_code = status.HTTP_400_BAD_REQUEST,
                content = {
                    "signal": ResponseSignal.FILE_UPLOAD_FAILED.value
                    }
            ) 


        # upload file to the project directory
        
        return JSONResponse(
                content = {
                    "signal": ResponseSignal.FILE_UPLOADED_SUCCESSFULLY.value,
                    "file_id": file_id
                    }
            ) 