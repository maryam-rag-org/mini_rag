from enum import Enum


class LLMEnums(Enum):

    Qwen = "QWEN"
    COHERE = "COHERE"

class QwenEnums(Enum):

    SYSTEM = "system"
    USER = "usre"
    ASSISTANT = "assistant"

class CoHereEnums(Enum):

    SYSTEM = "SYSTEM"
    USER = "USER"
    ASSISTANT = "CHATBOT"

    DOCUMENT = "search_document"
    QUERY = "search_query"


class DocumentTypeEnum(Enum):
    DOCUMENT = "document"
    QUERY = "query"

