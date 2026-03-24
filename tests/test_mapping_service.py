from app.services.mapping_service import VoiceMappingService

def test_mapping():
    service = VoiceMappingService()

    emotions = ["happy", "sad", "neutral", "angry"]

    for emotion in emotions:
        try:
            params = service.get_voice_params(emotion)
            print(f"Emotion: {emotion}")
            print(f"Params: {params}")
        except Exception as e:
            print(f"Error for {emotion}: {type(e).__name__}")
        print("-" * 50)


if __name__ == "__main__":
    test_mapping()