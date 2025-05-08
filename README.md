StreamDash 🚀 [@voice_weather_bot](https://t.me/voice_weather_bot) (Voice Weather Assistant)
Just speak - get instant weather! ☁️🎙️

StreamDash is a powerful real-time weather platform that collects, processes and visualizes live weather data through an innovative voice-first interface. The system integrates cutting-edge technologies:

Fetches data from weather APIs

Streams through Kafka for real-time processing

Handles requests via FastAPI backend

Stores historical data in PostgreSQL

Presents analytics on React dashboard

Key Innovation: Our Telegram bot revolutionizes weather access through natural voice interaction - just speak a location name and get instant forecasts without typing!

🖥️ Usage <a id="usage"></a>
Voice Weather Assistant
Open [@voice_weather_bot](https://t.me/voice_weather_bot) in Telegram

Send voice message with city/village name (e.g. "Kyiv", "Lviv", "Solotvyno")
(So ​​far only Ukrainian cities and villages)

Get detailed weather report in 1-2 seconds:

Current temperature and conditions

Precipitation probability

Wind speed and direction

24-hour forecast

How it works:

🎙️ Voice processed by DeepGram

📍 NLP extracts location from speech

⚡ Real-time data fetched from weather APIs

📊 Response formatted for easy understanding

No typing needed - just speak naturally! Try it now: 👉 [@voice_weather_bot](https://t.me/voice_weather_bot)

## 📋 Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Components](#components)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)

## 🔍 Overview <a id="overview"></a>

StreamDash demonstrates a complete real-time ETL pipeline built on a microservices architecture. Data is fetched from third-party weather APIs, streamed via Apache Kafka, processed by FastAPI services, and stored in PostgreSQL. Users receive live updates through a WebSocket-connected React dashboard and a voice-enabled Telegram bot.
This project serves as both a practical tool and a showcase of real-time data engineering and user-friendly UI/UX integration.

## 🏗️ Architecture <a id="architecture"></a>

graph TD
    Producer -->|Weather data| Kafka
    
    Kafka -->|Streams data| Backend
    
    Backend -->|Stores| PostgreSQL
    
    Backend -->|WebSocket| Frontend
    
    TelegramBot -->|Voice/Text| Backend
    
    Frontend -->|Dashboard UI| User
    
    TelegramBot -->|User input| User

## 🧩 Components <a id="components"></a>

### Backend (FastAPI)
- Consumes data from Kafka topics
- Processes and transforms the data
- Stores processed data in PostgreSQL
- Broadcasts real-time updates via WebSocket
- Provides API endpoints for data access

### Frontend (React)
- Connects to backend via WebSocket
- Displays real-time data visualizations
- Provides a user-friendly dashboard interface

### Producer
- Fetches weather data from external APIs
- Publishes data to Kafka topics
- Simulates real-time data streams

### Telegram Bot
- Provides a conversational interface to the system
- Processes text and voice commands
- Retrieves and returns weather information
- Integrates with the main data pipeline

### Infrastructure
- **Apache Kafka**: Message streaming platform
- **Zookeeper**: Manages Kafka cluster
- **PostgreSQL**: Persistent data storage
- **Docker & Docker Compose**: Containerization and orchestration

## 📦 Features <a id="features"></a>

- **Real-time Data Processing**: Stream processing with Apache Kafka
- **Data Persistence**: PostgreSQL database storage
- **Real-time Updates**: WebSocket broadcasting to frontend
- **Interactive Dashboard**: React-based visualization
- **Voice Command Processing**: Speech-to-text functionality in Telegram bot
- **Weather Data Integration**: Real-time weather information
- **Containerized Deployment**: Fully dockerized environment
- **Scalable Architecture**: Microservices-based design

## 🚀 Installation <a id="installation"></a>

### Prerequisites
- Docker and Docker Compose
- Git

### Setup
```bash
# Clone the repository
git clone https://github.com/FursykIvan/streamdash.git

# Navigate to project directory
cd streamdash

# Create .env file with required API keys
# Example:
# DEEPGRAM_API_KEY=your_deepgram_api_key
# WEATHER_API_KEY=your_weather_api_key
# TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# Start the application
docker-compose up --build
```

## 📁 Project Structure <a id="project-structure"></a>
```
streamdash/
├── backend/               # FastAPI backend service
│   ├── app/
│   │   ├── db.py          # Database connection
│   │   ├── kafka_consumer.py # Kafka consumer
│   │   ├── main.py        # Main application
│   │   ├── models.py      # Data models
│   │   └── websocket.py   # WebSocket implementation
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/              # React frontend
│   ├── src/
│   │   └── App.js         # Main React component
│   ├── Dockerfile
│   └── package.json
├── producer/              # Kafka producer
│   ├── producer.py        # Main producer script
│   ├── weather_api_client.py # Weather API client
│   ├── Dockerfile
│   └── requirements.txt
├── telegram_bot/          # Telegram bot service
│   ├── bot.py             # Main bot script
│   ├── voice_handler.py   # Voice processing
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml     # Docker Compose configuration
└── README.md              # Project documentation
```
