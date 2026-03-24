from app.services.tts_service import TTSService

def test_tts():
    service = TTSService()

    text = "Hello, this is a test of the empathy engine"

    params = {
        "rate": 180,
        "pitch": 120,
        "volume": 1.0
    }

    file_path = service.generate_audio(text, params)

    print(f"Audio file generated at: {file_path}")


if __name__ == "__main__":
    test_tts()