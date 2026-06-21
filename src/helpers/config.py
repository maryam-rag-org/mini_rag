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

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()