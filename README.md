# StreamDash 🚀

**StreamDash** is a real-time ETL service that consumes data from Kafka, processes it, stores it in PostgreSQL and broadcasts the results via WebSocket to a dynamic frontend dashboard.

### 🔧 Tech Stack

- **Backend**: FastAPI
- **Streaming**: Apache Kafka, WebSocket
- **Database**: PostgreSQL
- **Frontend**: React + WebSocket
- **Infrastructure**: Docker, Docker Compose

### 📦 Features

- Event simulator (Kafka Producer)
- ETL service: extract → transform → load
- Real-time WebSocket broadcasting
- Basic data visualization dashboard (React)
- Fully dockerized environment

### 📸 Preview

________

### 🚀 Quick Start

```bash
git clone https://github.com/FursykIvan/streamdash.git
cd streamdash
docker-compose up --build
