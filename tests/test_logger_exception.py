from app.utils.logger import get_logger
from app.utils.exceptions import (
    EmotionDetectionError,
    TTSGenerationError,
    MappingError
)

logger = get_logger("test_logger")


def test_emotion_error():
    try:
        logger.info("Testing EmotionDetectionError...")
        raise EmotionDetectionError("Emotion detection failed due to invalid input")
    except EmotionDetectionError as e:
        logger.warning(f"Caught exception: {type(e).__name__}")


def test_tts_error():
    try:
        logger.info("Testing TTSGenerationError...")
        raise TTSGenerationError("TTS engine crashed")
    except TTSGenerationError as e:
        logger.warning(f"Caught exception: {type(e).__name__}")


def test_mapping_error():
    try:
        logger.info("Testing MappingError...")
        raise MappingError("Invalid emotion mapping")
    except MappingError as e:
        logger.warning(f"Caught exception: {type(e).__name__}")


if __name__ == "__main__":
    test_emotion_error()
    test_tts_error()
    test_mapping_error()