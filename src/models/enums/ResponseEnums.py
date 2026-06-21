from enum import Enum


class ResponseSignal(Enum):
    """
    Enum for response signals.
    """
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"

    FILL_TYPE_NOT_SUPPORTED = "fill_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOAD_FAILED = "file_upload_failed"
    
    FILE_UPLOADED_SUCCESSFULLY = "file_uploaded_successfully"

    PROCESSING_FAILED = "processing_failed"
    PROCESSING_SUCCESSFUL = "processing_successful"
    
