# 🎙️ Empathy Engine

An AI-powered system that converts text into **emotionally expressive speech** using advanced NLP and audio modulation.

---

## 🚀 Overview

Empathy Engine analyzes input text, detects its emotional tone using a transformer-based model, and generates speech with **realistic voice modulation** (pitch and volume) to reflect that emotion.

This project combines **AI, backend APIs, and audio processing** into a complete end-to-end system.

---

## 🧠 Features

* 🔥 Emotion Detection using HuggingFace Transformer
* 🎙️ Text-to-Speech using gTTS
* 🎛️ Voice Modulation (Pitch + Volume)
* 🎧 Audio Playback + Download
* ⚡ FastAPI Backend
* 🎨 Streamlit Frontend
* 📝 Logging & Exception Handling

---

## 🎯 Supported Emotions

* Happy 😊
* Sad 😢
* Angry 😠
* Surprised 😲
* Neutral 😐

---

## 🧠 How It Works

```text
User Input Text
        ↓
Emotion Detection (HuggingFace Model)
        ↓
Smart Rule Overrides (for edge cases)
        ↓
Emotion Mapping (Pitch + Volume)
        ↓
Text-to-Speech (gTTS)
        ↓
Audio Processing (pydub)
        ↓
Generated Audio File (.mp3)
        ↓
Streamlit UI Playback
```

---

## 🏗️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** FastAPI
* **AI Model:** HuggingFace Transformers
* **TTS Engine:** gTTS
* **Audio Processing:** pydub + ffmpeg
* **Language:** Python

---

## 📁 Project Structure

```bash
empathy_engine/
│
├── app/
│   ├── main.py
│   ├── services/
│   │   ├── emotion_service.py
│   │   ├── mapping_service.py
│   │   ├── tts_service.py
│   ├── utils/
│   │   ├── logger.py
│   │   ├── exceptions.py
│
├── output_audio/
├── logs/
├── streamlit_app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Setup Instructions (Run Locally)

### 🔹 1. Clone the Repository

```bash
git clone https://github.com/your-username/empathy_engine.git
cd empathy_engine
```

---

### 🔹 2. Create Virtual Environment

```bash
python -m venv projectenv
```

Activate:

```bash
# Windows
projectenv\Scripts\activate

# Mac/Linux
source projectenv/bin/activate
```

---

### 🔹 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 🔹 4. Install FFmpeg (IMPORTANT)

👉 Required for audio processing

* Download: https://ffmpeg.org/download.html
* Extract → go to `bin/` folder
* Add path to system environment variables

Example:

```text
C:\ffmpeg\bin
```

Verify:

```bash
ffmpeg -version
```

---

### 🔹 5. Run FastAPI Backend

```bash
uvicorn app.main:app --reload
```

API will run at:

```
http://127.0.0.1:8000
```

---

### 🔹 6. Run Streamlit Frontend

Open a new terminal:

```bash
streamlit run streamlit_app.py
```

---

## 🎧 Usage

1. Enter text in the UI
2. Click **Generate Audio**
3. View detected emotion
4. Listen to generated speech
5. Download audio file

---

## 🧪 Example Inputs

| Input                          | Expected Emotion |
| ------------------------------ | ---------------- |
| "I am so happy today!"         | Happy            |
| "This is the worst thing ever" | Angry            |
| "I feel broken inside"         | Sad              |
| "Wow! This is unbelievable!"   | Surprised        |
| "Hello, good morning!"         | Happy            |

---

## 📌 API Endpoint

### POST `/generate-audio`

**Request**

```json
{
  "text": "Your input text"
}
```

**Response**

```json
{
  "emotion": "happy",
  "confidence": 0.95,
  "audio_file": "output_audio/file.mp3"
}
```

---

## ⚠️ Notes

* First request may take time (model loading)
* Requires internet (gTTS)
* Ensure FFmpeg is properly installed
* Do not commit `output_audio/`, `logs/`, or `projectenv/`

---

## 🔮 Future Improvements

* 🔐 Google Authentication
* ☁️ Cloud storage for audio
* 🎙️ Human-like voice (ElevenLabs / Coqui)
* 📊 Emotion analytics dashboard
* 💬 Conversational AI

---

## 👨‍💻 Author

**Bhaskar Phaneendra**

---

## ⭐ Support

If you like this project:

* ⭐ Star the repo
* 🍴 Fork it
* 🚀 Improve it

---

## 🏁 Final Note

This project demonstrates a full pipeline:

```text
AI + Backend + Frontend + Audio Processing + Deployment
```

A real-world production-style system 🚀
