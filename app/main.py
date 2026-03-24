# app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.services.emotion_service import EmotionService
from app.services.mapping_service import VoiceMappingService
from app.services.tts_service import TTSService

from app.utils.logger import get_logger
from app.utils.exceptions import (
    EmotionDetectionError,
    MappingError,
    TTSGenerationError
)

logger = get_logger(__name__)

app = FastAPI()


class TextRequest(BaseModel):
    text: str


emotion_service = EmotionService()
mapping_service = VoiceMappingService()
tts_service = TTSService()


@app.get("/")
def root():
    return {"message": "Empathy Engine Running 🚀"}


@app.post("/generate-audio")
def generate_audio(request: TextRequest):
    try:
        text = request.text
        logger.info(f"Received request: {text}")

        # 🔥 Emotion only
        result = emotion_service.detect_emotion(text)

        emotion = result["emotion"]
        confidence = result["confidence"]

        logger.info(f"Emotion: {emotion}, Confidence: {confidence}")

        # 🔥 Mapping (emotion only)
        params = mapping_service.get_voice_params(emotion)

        # 🔥 TTS
        file_path = tts_service.generate_audio(text, params, emotion)

        return {
            "emotion": emotion,
            "confidence": confidence,
            "audio_file": file_path
        }

    except EmotionDetectionError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except MappingError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except TTSGenerationError as e:
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")