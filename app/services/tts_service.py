# app/services/tts_service.py

import os
from datetime import datetime
from gtts import gTTS
from pydub import AudioSegment

from app.utils.logger import get_logger
from app.utils.exceptions import TTSGenerationError

logger = get_logger(__name__)


class TTSService:

    def __init__(self):
        try:
            os.makedirs("output_audio", exist_ok=True)
            logger.info("TTSService initialized")
        except Exception as e:
            raise TTSGenerationError("Init failed", e)

    def change_pitch(self, sound, pitch):
        new_sample_rate = int(sound.frame_rate * (2.0 ** pitch))
        return sound._spawn(
            sound.raw_data,
            overrides={"frame_rate": new_sample_rate}
        ).set_frame_rate(44100)

    def generate_audio(self, text: str, params: dict, emotion: str) -> str:
        try:
            if not text.strip():
                raise ValueError("Empty text")

            logger.info(f"Generating audio for: {text}")

            filename = f"{emotion}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.mp3"
            file_path = os.path.join("output_audio", filename)

            #  STEP 1: Generate base audio
            tts = gTTS(text=text, lang='en')
            tts.save(file_path)

            #  STEP 2: Load audio
            audio = AudioSegment.from_file(file_path)

            #  STEP 3: Apply volume
            audio = audio + params.get("volume", 0)

            #  STEP 4: Apply pitch
            pitch = params.get("pitch", 0)
            audio = self.change_pitch(audio, pitch)

            #  STEP 5: Save final
            audio.export(file_path, format="mp3")

            logger.info(f"Audio generated: {file_path}")

            return file_path

        except Exception as e:
            logger.error(f"TTS error: {str(e)}")
            raise TTSGenerationError("Audio generation failed", e)