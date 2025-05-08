# StreamDash 🚀

**StreamDash** is a comprehensive real-time data processing platform that collects weather data, processes it through a streaming pipeline, and visualizes it in a dynamic dashboard. The system also features a Telegram bot interface for user interaction and voice command processing.

## 📋 Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Components](#components)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [License](#license)

## 🔍 Overview

StreamDash demonstrates a complete ETL (Extract, Transform, Load) pipeline using modern streaming technologies. It fetches weather data from external APIs, processes it through Apache Kafka, stores it in PostgreSQL, and delivers real-time updates to users via a React dashboard and Telegram bot.

## 🏗️ Architecture

![StreamDash Architecture](https://mermaid.ink/img/pako:eNqFkk1rwzAMhv-K0GmD_QGDHQrtYYcNtl12CcGxmhjixJPtQCn97_OSpWtLGfOJ6NWjV5I9UmEVUkZLXTvTwBN4Z1pYGFfDGhqnPSyNdWBqWMEWvIXKGQcXsLZGOVhqVZHXDRRKO1J_gNqAUg5-jHawVtpT8QZKNcbBs9KNgfvxeAIPULZk4Ek1FdxNJlPYgW5JwKNqS7ibTmewBd2RgAdVl3A_m83hG3RLAu5VVcLDfL6AHeiOBNypsoTHxeIJvkB3JOBWlSU8LZdP8Am6JwE3qirhebV6gQ_QPQm4VmUJr-v1K7yDHkjAlapKeNtsXuAN9EgCLlVVwvt2-wZvoEcScKHKEj52uzd4BT2RgHNVlvC53-_hBfREAs5UWcLXfn-AF9ATCThVZQnfh8MRnkFPJOBElSX8HA5HeAI9k4BjVZbwezwe4RH0TAKOVFnC3_F4hAfQMwk4VGUJ_6fTCe5BzyTgQJUl_J9OJ7gDPZOAfVWW8H86neAW9EwC9lRZwmmaJrgBPZOAXVWWcJqmCa5BzyRgR5UlnKZpgivQMwnYVmUJp2ma4BL0TAK2VFnCaZomuAA9k4BNVZZwmqYJzkHPJGBDlSWcpmmCM9AzCVhXZQmnaZrgFPRMAv6psoTTNE1wAnomAX9UWcJpmib4BT2TgF9VlnCapgl-QM8k4IcqS_gHnNANrw?type=png)

## 🧩 Components

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

## 📦 Features

- **Real-time Data Processing**: Stream processing with Apache Kafka
- **Data Persistence**: PostgreSQL database storage
- **Real-time Updates**: WebSocket broadcasting to frontend
- **Interactive Dashboard**: React-based visualization
- **Voice Command Processing**: Speech-to-text functionality in Telegram bot
- **Weather Data Integration**: Real-time weather information
- **Containerized Deployment**: Fully dockerized environment
- **Scalable Architecture**: Microservices-based design

## 🚀 Installation

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

## 🖥️ Usage

### Dashboard
Access the dashboard at `http://localhost:3000`

### Kafka UI
Monitor Kafka topics at `http://localhost:8080`

### Backend API
Access the FastAPI backend at `http://localhost:8000`

### Telegram Bot
Start a conversation with the bot using your Telegram client

## 📁 Project Structure
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
