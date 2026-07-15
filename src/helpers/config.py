from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # all variables that we want to load from the .env file should be defined here with data type
    APP_NAME: str
    APP_VERSION: str
    LLM_API_KEY: str

    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int

    MONGO_URL: str
    MONGODB_DATABASE: str

    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str

    QWEN_API_KEY: str = None
    QWEN_API_URL: str = None
    
    COHERE_API_KEY: str = None

    GENERATION_MODEL_ID: str = None
    EMBEDDING_MODEL_ID: str = None
    EMBEDDING_MODEL_SIZE: int = None

    INPUT_DEFAULT_MAX_CHARACTERS: int = None
    GENERATION_DEFAULT_MAX_TOKENS: int = None
    GENERATION_DEFAULT_TEMPERATURE: float = None


    class Config:
        env_file = ".env"

def get_settings():
    return Settings()