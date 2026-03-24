# app/utils/exceptions.py

import traceback
from app.utils.logger import get_logger

logger = get_logger(__name__)


class BaseAppException(Exception):
    """
    Base Exception class for all custom exceptions
    """

    def __init__(self, message: str, original_exception: Exception = None):
        self.message = message
        self.original_exception = original_exception

        super().__init__(self.message)

        # Automatically log exception
        self.log_exception()

    def log_exception(self):
        if self.original_exception:
            trace = traceback.format_exc()
        else:
            trace = "No traceback available (raised manually)"

        logger.error(
            f"\nException Type: {self.__class__.__name__}\n"
            f"Message: {self.message}\n"
            f"Traceback: {trace}\n"
        )


class EmotionDetectionError(BaseAppException):
    pass


class TTSGenerationError(BaseAppException):
    pass


class MappingError(BaseAppException):
    pass