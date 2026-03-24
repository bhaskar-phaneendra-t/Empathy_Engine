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
            text_lower = text.lower().strip()

            # ---------------------------------
            # ANGER (TOP PRIORITY)
            # ---------------------------------
            anger_keywords = [
                "hate", "angry", "furious", "rage", "worst",
                "useless", "idiot", "stupid", "dumb",
                "annoying", "frustrating", "irritating", "mad"
            ]

            if any(word in text_lower for word in anger_keywords):
                return {
                    "emotion": "angry",
                    "confidence": 0.99
                }

            # ---------------------------------
            #  SAD
            # ---------------------------------
            sad_keywords = [
                "sad", "hurt", "pain", "cry", "depressed",
                "broken", "upset", "tired", "lonely", "disappointed"
            ]

            if any(word in text_lower for word in sad_keywords):
                return {
                    "emotion": "sad",
                    "confidence": 0.95
                }

            # ---------------------------------
            #  GREETING / FRIENDLY
            # ---------------------------------
            greeting_phrases = [
                "hi", "hello", "hey",
                "good morning", "good evening", "good afternoon",
                "how are you", "how are you now", "nice to meet you"
            ]

            if any(p in text_lower for p in greeting_phrases):
                return {
                    "emotion": "happy",
                    "confidence": 0.95
                }

            # ---------------------------------
            #  HAPPY / APPRECIATION
            # ---------------------------------
            happy_keywords = [
                "thank", "thanks", "appreciate", "grateful",
                "awesome", "great", "good", "nice", "happy", "love"
            ]

            if any(word in text_lower for word in happy_keywords):
                return {
                    "emotion": "happy",
                    "confidence": 0.92
                }

            # ---------------------------------
            #  SURPRISE (STRICT ONLY)
            # ---------------------------------
            surprise_keywords = [
                "wow", "unbelievable", "shocked",
                "no way", "amazing", "can't believe"
            ]

            if any(word in text_lower for word in surprise_keywords):
                return {
                    "emotion": "surprised",
                    "confidence": 0.95
                }

            # ---------------------------------
            #  QUESTIONS → NEUTRAL (LOW PRIORITY)
            # ---------------------------------
            question_words = [
                "what", "why", "how", "where", "when", "who",
                "can you", "could you", "will you"
            ]

            if "?" in text_lower or any(q in text_lower for q in question_words):
                return {
                    "emotion": "neutral",
                    "confidence": 0.9
                }

            # ---------------------------------
            #  AI MODEL (FINAL FALLBACK)
            # ---------------------------------
            results = self.classifier(text)[0]

            # take best prediction
            best = results[0]

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

            #  CRITICAL FIX: never allow surprise for normal questions
            if emotion == "surprised" and "?" in text_lower:
                emotion = "neutral"

            return {
                "emotion": emotion,
                "confidence": float(score)
            }

        except Exception as e:
            raise EmotionDetectionError("Emotion detection failed", e)