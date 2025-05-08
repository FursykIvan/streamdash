from sqlalchemy import Column, Integer, String, Float
from backend.app.db import Base

class WeatherData(Base):
    """
    SQLAlchemy model representing weather data in the database.

    Attributes:
        id (int): Primary key for the weather data record
        city (str): Name of the city for which weather data is recorded
        temperature (float): Temperature in Celsius
        humidity (int): Humidity percentage
        weather_description (str): Text description of the weather conditions
        timestamp (int): Unix timestamp when the weather data was recorded
    """
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Integer, nullable=False)
    weather_description = Column(String, nullable=True)
    timestamp = Column(Integer, nullable=False)
