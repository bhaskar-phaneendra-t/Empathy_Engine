import streamlit as st
import requests
import os
import time

st.title("🎙️ Empathy Engine")

text = st.text_area("Enter your text")

if "audio_bytes" not in st.session_state:
    st.session_state.audio_bytes = None

if st.button("Generate Audio"):

    if text.strip() == "":
        st.warning("Enter text")
    else:
        try:
            st.session_state.audio_bytes = None

            response = requests.post(
                "http://127.0.0.1:8000/generate-audio",
                json={"text": text}
            )

            if response.status_code == 200:
                data = response.json()

                st.success(f"Emotion: {data['emotion']}")
                st.write(f"Confidence: {data['confidence']:.2f}")

                audio_path = data["audio_file"]

                if os.path.exists(audio_path):
                    time.sleep(0.3)

                    with open(audio_path, "rb") as f:
                        st.session_state.audio_bytes = f.read()

                else:
                    st.error("Audio file not found")

            else:
                st.error(response.text)

        except Exception as e:
            st.error(str(e))


# 🔥 ALWAYS RENDER
if st.session_state.audio_bytes:
    st.audio(st.session_state.audio_bytes, format="audio/mp3")

    st.download_button(
        "Download Audio",
        st.session_state.audio_bytes,
        file_name="emotion_audio.mp3"
    )