from fastapi import FastAPI, WebSocket
from backend.app.websocket import websocket_endpoint
import asyncio
from backend.app.kafka_consumer import consume_weather_data

app = FastAPI()

@app.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    """
    WebSocket endpoint handler for the "/ws" route.

    This function delegates the WebSocket connection handling to the
    websocket_endpoint function from the websocket module.

    Args:
        websocket (WebSocket): The WebSocket connection object
    """
    await websocket_endpoint(websocket)

@app.on_event("startup")
async def startup_event():
    """
    FastAPI startup event handler.

    This function is executed when the FastAPI application starts.
    It starts the Kafka consumer in a separate thread to continuously
    process incoming weather data without blocking the main application.
    """
    loop = asyncio.get_event_loop()
    loop.create_task(asyncio.to_thread(consume_weather_data))
