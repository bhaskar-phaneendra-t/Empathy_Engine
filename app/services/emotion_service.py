# app/services/emotion_service.py

from transformers import pipeline

from app.utils.logger import get_logger
from app.utils.exceptions import EmotionDetectionError

logger = get_logger(__name__)


class EmotionService:
    def __init__(self):
        try:
            self.classifier = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                top_k=1
            )
            logger.info("EmotionService initialized with HuggingFace model")
        except Exception as e:
            raise EmotionDetectionError("Failed to load model", e)

    def detect_emotion(self, text: str) -> dict:
        try:
            text_lower = text.lower()

            # 🔥 HARD OVERRIDES (VERY IMPORTANT)

            if any(word in text_lower for word in ["sorry", "apologize"]):
                return {"emotion": "sad", "confidence": 0.95}

            if any(word in text_lower for word in ["thank", "thanks"]):
                return {"emotion": "happy", "confidence": 0.95}

            if any(word in text_lower for word in [
                "never give up", "you can do it", "believe", "achieve"
            ]):
                return {"emotion": "happy", "confidence": 0.95}

            if any(word in text_lower for word in [
                "idiot", "stupid", "useless", "hate"
            ]):
                return {"emotion": "angry", "confidence": 0.98}

            # 🔥 AI MODEL (fallback)
            result = self.classifier(text)[0][0]

            raw_label = result["label"].lower()
            score = result["score"]

            mapping = {
                "joy": "happy",
                "anger": "angry",
                "sadness": "sad",
                "surprise": "surprised",
                "fear": "sad",
                "disgust": "angry",
                "neutral": "neutral"
            }

            emotion = mapping.get(raw_label, "neutral")

            return {
                "emotion": emotion,
                "confidence": float(score)
            }

        except Exception as e:
            raise EmotionDetectionError("Emotion detection failed", e)