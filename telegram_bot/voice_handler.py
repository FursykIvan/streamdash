import os
import tempfile

import requests
import speech_recognition as sr
from pydub import AudioSegment

from producer.weather_api_client import get_weather

recognizer = sr.Recognizer()

def handle_voice_query(voice_data: bytes) -> dict:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as temp_ogg:
            temp_ogg.write(voice_data)
            temp_ogg_path = temp_ogg.name

        temp_wav_path = temp_ogg_path.replace(".ogg", ".wav")
        audio = AudioSegment.from_ogg(temp_ogg_path)
        audio.export(temp_wav_path, format="wav")

        with sr.AudioFile(temp_wav_path) as source:
            audio_data = recognizer.record(source)
            transcript = recognizer.recognize_google(audio_data, language="uk-UA")

        os.remove(temp_ogg_path)
        os.remove(temp_wav_path)

        try:
            weather_info = get_weather(transcript.strip())
            return {
                "status": "success",
                "data": weather_info
            }
        except requests.HTTPError:
            return {
                "status": "error",
                "message": "Місто не знайдено або проблема із запитом"
            }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Не вдалося обробити голосове повідомлення: {str(e)}"
        }
