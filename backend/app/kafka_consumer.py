from kafka import KafkaConsumer
import json
from backend.app.db import SessionLocal
from backend.app.models import WeatherData

consumer = KafkaConsumer(
    "weather-topic",  # Назва топіка
    bootstrap_servers=["kafka:9092"],
    group_id="weather-group",
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

def consume_weather_data():
    """
    Consumes weather data from a Kafka topic and stores it in the database.

    This function continuously listens to the 'weather-topic' Kafka topic,
    deserializes the received messages, and stores the weather data in the database
    using the WeatherData model.

    Note:
        This function runs in an infinite loop until interrupted.
    """
    db = SessionLocal()
    try:
        for message in consumer:
            weather_info = message.value

            weather = WeatherData(
                city=weather_info["city"],
                temperature=weather_info["temperature"],
                humidity=weather_info["humidity"],
                weather_description=weather_info.get("weather_description"),
                timestamp=weather_info["timestamp"]
            )
            db.add(weather)
            db.commit()
    finally:
        db.close()
