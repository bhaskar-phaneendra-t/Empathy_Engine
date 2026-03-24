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
                top_k=3
            )
            logger.info("EmotionService initialized (Hybrid Mode)")
        except Exception as e:
            raise EmotionDetectionError("Failed to load model", e)

    def detect_emotion(self, text: str) -> dict:
        try:
            text_lower = text.lower()

            # ---------------------------------
            # 🔥 STRONG KEYWORD SIGNALS (HIGH WEIGHT)
            # ---------------------------------

            anger_words = [
                "idiot", "stupid", "useless", "hate", "worst",
                "frustrated", "annoyed", "angry", "irritated"
            ]

            sad_words = [
                "sad", "depressed", "hurt", "pain", "broken",
                "lonely", "tired", "cry", "upset"
            ]

            happy_words = [
                "happy", "great", "awesome", "amazing",
                "fantastic", "love", "good", "nice"
            ]

            surprise_words = [
                "wow", "unbelievable", "shocking",
                "can't believe", "unexpected", "incredible"
            ]

            # ---------------------------------
            # 🔥 PRIORITY RULES
            # ---------------------------------

            if any(w in text_lower for w in anger_words):
                return {"emotion": "angry", "confidence": 0.97}

            if any(w in text_lower for w in sad_words):
                return {"emotion": "sad", "confidence": 0.95}

            if any(w in text_lower for w in surprise_words):
                return {"emotion": "surprised", "confidence": 0.95}

            if any(w in text_lower for w in happy_words):
                return {"emotion": "happy", "confidence": 0.92}

            # ---------------------------------
            # 🤖 HUGGINGFACE MODEL (MAIN BRAIN)
            # ---------------------------------

            results = self.classifier(text)[0]

            # Weighted scoring
            scores = {}

            mapping = {
                "joy": "happy",
                "anger": "angry",
                "sadness": "sad",
                "surprise": "surprised",
                "fear": "sad",
                "disgust": "angry",
                "neutral": "neutral"
            }

            for r in results:
                label = mapping.get(r["label"].lower(), "neutral")
                score = r["score"]

                scores[label] = scores.get(label, 0) + score

            # Pick best
            emotion = max(scores, key=scores.get)
            confidence = scores[emotion]

            return {
                "emotion": emotion,
                "confidence": float(confidence)
            }

        except Exception as e:
            logger.error(f"Emotion detection error: {str(e)}")
            raise EmotionDetectionError("Emotion detection failed", e)