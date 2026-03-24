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
                top_k=3   # 🔥 important for better decisions
            )
            logger.info("EmotionService initialized with HuggingFace model")
        except Exception as e:
            raise EmotionDetectionError("Failed to load model", e)

    def detect_emotion(self, text: str) -> dict:
        try:
            if not text or not text.strip():
                raise ValueError("Empty text")

            text_lower = text.lower()

            # ---------------------------------
            # 🔥 PRIORITY 1: GREETING (HIGHEST)
            # ---------------------------------
            greeting_words = [
                "hi", "hello", "hey",
                "good morning", "good evening", "good afternoon",
                "happy birthday", "have a nice day", "nice to meet you"
            ]

            if any(word in text_lower for word in greeting_words):
                return {
                    "emotion": "happy",
                    "confidence": 0.98
                }

            # ---------------------------------
            # 🔥 PRIORITY 2: STRONG NEGATIVE
            # ---------------------------------
            angry_words = [
                "idiot", "stupid", "useless", "hate", "worst",
                "dumb", "fool", "nonsense", "trash", "annoying"
            ]

            if any(word in text_lower for word in angry_words):
                return {
                    "emotion": "angry",
                    "confidence": 0.97
                }

            # ---------------------------------
            # 🔥 PRIORITY 3: STRONG POSITIVE
            # ---------------------------------
            positive_words = [
                "amazing", "awesome", "fantastic", "great",
                "love", "wonderful", "excellent", "beautiful"
            ]

            if any(word in text_lower for word in positive_words):
                return {
                    "emotion": "happy",
                    "confidence": 0.95
                }

            # ---------------------------------
            # 🔥 PRIORITY 4: SURPRISE
            # ---------------------------------
            surprise_words = [
                "wow", "unbelievable", "shocking",
                "can't believe", "incredible", "unexpected"
            ]

            if any(word in text_lower for word in surprise_words):
                return {
                    "emotion": "surprised",
                    "confidence": 0.95
                }

            # ---------------------------------
            # 🔥 AI MODEL (MAIN LOGIC)
            # ---------------------------------
            results = self.classifier(text)[0]

            best = max(results, key=lambda x: x["score"])

            raw_label = best["label"].lower()
            score = best["score"]

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
            logger.error(f"Emotion detection error: {str(e)}")
            raise EmotionDetectionError("Emotion detection failed", e)