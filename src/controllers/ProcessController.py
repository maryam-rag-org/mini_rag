from .BaseController import BaseController
from .ProjectController import ProjectController

from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

import os
from models import ProcessingEnum

class ProcessController(BaseController):

    def __init__(self, project_id: str):
        super().__init__()

        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id = project_id)
    
    def get_file_extension(self, file_id: str):
        return file_id.split(".")[-1].lower()

    def get_file_loader(self, file_id: str):
        
        file_extension = self.get_file_extension(file_id)
        file_path = os.path.join(
                    self.project_path, 
                    file_id)

        if not os.path.exists(file_path):
            return None
        
        if file_extension == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        
        elif file_extension == ProcessingEnum.TXT.value:
            return TextLoader(file_path, encoding = "utf-8")

        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
            return None

    def get_file_content(self, file_id: str) -> list:

        loader = self.get_file_loader(file_id=file_id)

        if loader:
            documents = loader.load()
            return documents # list
        else:
            return None

    def process_file_content(self,  file_content: list,
                                    file_id: str, 
                                    chunk_size: int = 100, 
                                    chunk_overlap: int = 20):

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap,
            length_function = len, 
            )
        # text_splitter takes string as input while file_content is a list of documents, so we need to convert it to string
        
        file_content_texts = [
            recored.page_content for recored in file_content
        ]

        file_content_metadata = [
            recored.metadata for recored in file_content
        ]

        chunks = text_splitter.create_documents(file_content_texts, 
                                                metadatas = file_content_metadata)
        return chunks

