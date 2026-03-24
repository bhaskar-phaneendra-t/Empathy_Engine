from app.services.emotion_service import EmotionService

def test_emotion():
    service = EmotionService()

    texts = [
        "I am very happy today!",
        "This is the worst experience ever",
        "The meeting is scheduled at 5 PM"
    ]

    for text in texts:
        emotion = service.detect_emotion(text)
        print(f"Text: {text}")
        print(f"Emotion: {emotion}")
        print("-" * 50)


if __name__ == "__main__":
    test_emotion()