from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    # all variables that we want to load from the .env file should be defined here with data type
    APP_NAME: str
    APP_VERSION: str
    LLM_API_KEY: str

    FILE_ALLOWED_TYPES:  List[str] = None
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int

    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_MAIN_DATABASE: str

    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str

    QWEN_API_KEY: str = None

    QWEN_API_URL_LITERAL: List[str] = None
    QWEN_API_URL: str = None
    
    COHERE_API_KEY: str = None

    GENERATION_MODEL_ID_LITERAL:  List[str] = None
    GENERATION_MODEL_ID: str = None
    EMBEDDING_MODEL_ID: str = None
    EMBEDDING_MODEL_SIZE: int = None

    INPUT_DEFAULT_MAX_CHARACTERS: int = None
    GENERATION_DEFAULT_MAX_TOKENS: int = None
    GENERATION_DEFAULT_TEMPERATURE: float = None

    EMBEDDING_MODEL_ID_LITERAL: List[str] = None
    EMBEDDING_MODEL_SIZE_LITERAL: List[int] = None
    VECTOR_DB_BACKEND_LITERAL: List[str] = None


    VECTOR_DB_BACKEND: str
    VECTOR_DB_PATH: str
    VECTOR_DB_DISTANCE_MITHOD: str
    VECTOR_DB_PGVEC_INDEX_THRESHOLD: int = 1000

    PRIMARY_LANG:str = "en"
    DEFAULT_LANG: str = "en"

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    CELERY_TASK_SERIALIZER: str = "Json"
    CELERY_TASK_TIME_LIMIT: int = 600
    CELERY_TASK_ACKS_LATE: bool = True
    CELERY_WORKER_CONCURRENCY: int = 2
    CELERY_FLOWER_PASSWORD: str


    class Config:
        env_file = ".env"

def get_settings():
    return Settings()

    