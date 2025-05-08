import os
import logging
from dotenv import load_dotenv
from deepgram import DeepgramClient, PrerecordedOptions
from producer.weather_api_client import get_weather_by_city

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

load_dotenv()


class VoiceHandler:
    """
    Handles voice message processing for weather queries.

    This class provides functionality to transcribe voice messages,
    identify city names from the transcription, and retrieve weather data
    for the identified cities.
    """

    def __init__(self):
        """
        Initializes the VoiceHandler with Deepgram API client.

        Raises:
            ValueError: If DEEPGRAM_API_KEY environment variable is not set
            Exception: If Deepgram client initialization fails
        """
        api_key = os.getenv("DEEPGRAM_API_KEY")
        if not api_key:
            logger.error("DEEPGRAM_API_KEY not found in .env")
            raise ValueError("DEEPGRAM_API_KEY is missing")

        try:
            self.deepgram = DeepgramClient(api_key)
            self.content_type = "audio/ogg"
            logger.info("Deepgram client initialized successfully")
        except Exception as e:
            logger.error(f"Deepgram initialization error: {str(e)}")
            raise

        # Previously known Ukrainian cities
        self.ukrainian_cities = [
            "київ", "львів", "харків", "одеса", "дніпро", "вінниця",
            "луцьк", "житомир", "ужгород", "тернопіль", "чернівці", "миколаїв",
            "чернігів", "черкаси", "суми", "полтава", "івано-франківськ", "хмельницький"
        ]

    async def _transcribe_audio(self, audio_data: bytes):
        """
        Transcribes audio data to text using Deepgram API.

        Args:
            audio_data (bytes): The binary audio data to transcribe

        Returns:
            str or None: The transcribed text if successful, None otherwise

        Note:
            Uses Ukrainian language model for transcription
        """
        try:
            source = {"buffer": audio_data, "mimetype": self.content_type}
            options = PrerecordedOptions(
                model="nova-2",
                language="uk",
                punctuate=True,
                smart_format=True,
                detect_entities=True,
                diarize=False,
                encoding="linear16"
            )

            response = self.deepgram.listen.prerecorded.v("1").transcribe_file(source, options)

            if not response or not hasattr(response, 'results'):
                logger.error("Empty or invalid response from Deepgram API")
                return None

            channel = response.results.channels[0]
            alternative = channel.alternatives[0]
            transcript = alternative.transcript

            logger.info(f"Transcript: {transcript}")
            return transcript

        except Exception as e:
            logger.error(f"Transcription error: {str(e)}", exc_info=True)
            return None

    async def _resolve_city_and_get_weather(self, transcript: str):
        """
        Attempts to identify a city name from the transcript and retrieve weather data.

        The method uses two approaches:
        1. First tries to use the entire transcript as a city name
        2. If that fails, searches for known Ukrainian city names within the transcript

        Args:
            transcript (str): The transcribed text to analyze

        Returns:
            tuple: A tuple containing (city_name, weather_data) if successful,
                  or (None, None) if no city could be identified or weather data retrieved
        """
        if not transcript:
            return None, None

        text = transcript.replace('.', '').strip().lower()

        # Attempt 1: we assume that the entire text is the name of the city
        direct_city = text
        weather = await get_weather_by_city(direct_city)
        if weather and "temp" in weather:
            return direct_city.capitalize(), weather

        # Attempt 2: Search in a list of cities
        for city in self.ukrainian_cities:
            if city in text:
                city_name = city.capitalize()
                weather = await get_weather_by_city(city_name)
                if weather and "temp" in weather:
                    return city_name, weather

        return None, None

    async def process_voice(self, audio_data: bytes):
        """
        Processes voice data to extract weather information for a city.

        This is the main method that orchestrates the entire voice processing workflow:
        1. Transcribes the audio to text
        2. Identifies a city name from the transcript
        3. Retrieves weather data for the identified city
        4. Formats the response

        Args:
            audio_data (bytes): The binary audio data to process

        Returns:
            dict: A dictionary containing the processing results with the following structure:
                - On success:
                  {
                    "status": "success",
                    "city": str,
                    "weather": dict,
                    "recognized_text": str,
                    "speech_response": str
                  }
                - On error:
                  {
                    "status": "error",
                    "message": str,
                    "recognized_text": str or None
                  }
        """
        try:
            transcript = await self._transcribe_audio(audio_data)
            if not transcript:
                return {
                    "status": "error",
                    "message": "Не вдалося розпізнати аудіо. Спробуйте ще раз",
                    "recognized_text": None
                }

            city, weather = await self._resolve_city_and_get_weather(transcript)
            if not city or not weather:
                return {
                    "status": "error",
                    "message": "Не вдалося визначити місто або отримати погоду. Спробуйте іншу назву",
                    "recognized_text": transcript
                }

            weather_desc = weather.get("description", "").capitalize()
            response_text = (
                f"🌦️ Погода у місті {city}:\n"
                f"🌡️ {weather.get('temp', 'N/A')}°C (відчувається як {weather.get('feels_like', 'N/A')}°C)\n"
                f"💧 Вологість: {weather.get('humidity', 'N/A')}%\n"
                f"🌬️ Вітер: {weather.get('wind_speed', 'N/A')} м/с\n"
                f"📝 {weather_desc}\n"
                f"🕒 Оновлено: {weather.get('time', 'N/A')}"
            )

            return {
                "status": "success",
                "city": city,
                "weather": weather,
                "recognized_text": transcript,
                "speech_response": response_text
            }

        except Exception as e:
            logger.error(f"Critical error: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": "Технічна помилка. Спробуйте пізніше",
                "recognized_text": None
            }


voice_handler = VoiceHandler()


async def handle_voice_query(audio_data: bytes):
    """
    A convenience function that processes voice data using the singleton VoiceHandler instance.

    This function serves as the main entry point for voice processing in the application.

    Args:
        audio_data (bytes): The binary audio data to process

    Returns:
        dict: The result of voice processing. See VoiceHandler.process_voice() for details
              on the return value structure.
    """
    return await voice_handler.process_voice(audio_data)
