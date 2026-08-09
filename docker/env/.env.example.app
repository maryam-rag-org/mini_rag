APP_NAME="Mini RAG App"
APP_VERSION="0.1s"
LLM_API_KEY=""

FILE_ALLOWED_TYPES= ["application/pdf", "text/plain"]
FILE_MAX_SIZE = 10  # 10 MB
FILE_DEFAULT_CHUNK_SIZE = 512000 #0.5 MB  

POSTGRES_USERNAME = "postgres"
POSTGRES_PASSWORD = "admin"
POSTGRES_HOST = "pgvector" # name of docker image that host postgres
POSTGRES_PORT = 5432
POSTGRES_MAIN_DATABASE = "minirag"

# ==================== LLM Config ====================
GENERATION_BACKEND = "QWEN"
EMBEDDING_BACKEND = "COHERE"

QWEN_API_KEY=""
QWEN_API_URL_LITERAL = ["http://localhost:11434/v1/", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1" ]  #from ollama , qwen
QWEN_API_URL="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"

COHERE_API_KEY=""

GENERATION_MODEL_ID= "qwen3:4b"

EMBEDDING_MODEL_ID_LITERAL  = ["embed-multilingual-v3.0"]
EMBEDDING_MODEL_ID = "embed-multilingual-v3.0"

EMBEDDING_MODEL_SIZE_LITERAL = [1024]
EMBEDDING_MODEL_SIZE = 1024

INPUT_DEFAULT_MAX_CHARACTERS=1024
GENERATION_DEFAULT_MAX_TOKENS=200
GENERATION_DEFAULT_TEMPERATURE=0.1

# ==================== Vector DB Config ====================
VECTOR_DB_BACKEND_LITERAL = ["PGVECTOR", "QDRANT"]
VECTOR_DB_BACKEND = "PGVECTOR" 

VECTOR_DB_PATH = "qdrant_db"
VECTOR_DB_DISTANCE_MITHOD = "cosine"

VECTOR_DB_PGVEC_INDEX_THRESHOLD = 100 # should be 10000 to give the best results

# ==================== Template Configs ====================
PRIMARY_LANG = "en"
DEFAULT_LANG = "en"


