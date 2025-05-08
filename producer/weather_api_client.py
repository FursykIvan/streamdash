import aiohttp
import os
import logging
from datetime import datetime
from typing import Dict, Any

# Налаштування детального логування
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('weather_api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"


async def get_weather_by_city(city: str) -> Dict[str, Any]:
    """
    Retrieves weather data for a specified city with detailed logging of each step.

    Args:
        city (str): The name of the city to get weather data for.
                   Supports Ukrainian city names which are normalized to English.

    Returns:
        Dict[str, Any]: A dictionary containing weather data with the following keys:
            - city: Name of the city
            - temp: Current temperature in Celsius
            - feels_like: "Feels like" temperature in Celsius
            - humidity: Humidity percentage
            - description: Weather description
            - wind_speed: Wind speed in m/s
            - time: Current time in HH:MM format
            - error: Error message (only if an error occurred)

    Raises:
        ValueError: If the API key is not found or if the API returns an error
    """
    logger.debug(f"Початок обробки запиту для міста: {city}")
    try:
        if not WEATHER_API_KEY:
            error_msg = "WEATHER_API_KEY не знайдено"
            logger.critical(error_msg)
            raise ValueError(error_msg)

        city_mapping = {
            "київ": "Kyiv",
            "львів": "Lviv",
            "харків": "Kharkiv",
            "одеса": "Odesa",
            "луцьк": "Lutsk"
        }
        normalized_city = city_mapping.get(city.lower(), city)
        logger.debug(f"Нормалізована назва міста: {normalized_city}")

        params = {
            "q": f"{normalized_city},UA",
            "appid": WEATHER_API_KEY,
            "units": "metric",
            "lang": "ua"
        }
        logger.debug(f"Параметри запиту: {params}")

        async with aiohttp.ClientSession() as session:
            async with session.get(WEATHER_API_URL, params=params) as response:
                logger.debug(f"Отримано відповідь, статус: {response.status}")

                if response.status != 200:
                    error_data = await response.json()
                    error_msg = f"Помилка API: {error_data.get('message', 'Невідома помилка')}"
                    logger.error(f"{error_msg}. Статус: {response.status}")
                    raise ValueError(error_msg)

                data = await response.json()
                logger.debug("Успішно отримано дані погоди")
                logger.debug(f"Структура відповіді: {data.keys()}")

                return {
                    "city": data["name"],
                    "temp": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"],
                    "wind_speed": data["wind"]["speed"],
                    "time": datetime.fromtimestamp(data["dt"]).strftime("%H:%M")
                }

    except Exception as e:
        logger.error(f"Критична помилка для міста {city}: {str(e)}", exc_info=True)
        return {"error": str(e)}
