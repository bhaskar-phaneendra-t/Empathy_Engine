# app/services/mapping_service.py

from app.utils.logger import get_logger
from app.utils.exceptions import MappingError

logger = get_logger(__name__)


class VoiceMappingService:

    def __init__(self):
        try:
            self.voice_map = {
                "happy": {"pitch": 0.08, "volume": +5},
                "sad": {"pitch": -0.08, "volume": -6},
                "angry": {"pitch": 0.12, "volume": +10},
                "surprised": {"pitch": 0.15, "volume": +8},
                "neutral": {"pitch": 0.0, "volume": 0}
            }

            logger.info("VoiceMappingService initialized")

        except Exception as e:
            raise MappingError("Mapping init failed", e)

    def get_voice_params(self, emotion: str) -> dict:
        try:
            if emotion not in self.voice_map:
                emotion = "neutral"

            params = self.voice_map[emotion]

            logger.debug(f"Voice params: {params}")

            return params

        except Exception as e:
            raise MappingError("Mapping failed", e)