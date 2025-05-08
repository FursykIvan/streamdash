from fastapi import WebSocket

connected_clients = []

async def websocket_endpoint(websocket: WebSocket):
    """
    Handles WebSocket connections from clients.

    This function:
    1. Accepts the WebSocket connection
    2. Adds the client to the list of connected clients
    3. Keeps the connection alive by waiting for messages
    4. Removes the client when the connection is closed

    Args:
        websocket (WebSocket): The WebSocket connection object
    """
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        connected_clients.remove(websocket)

async def broadcast_message(message: str):
    """
    Broadcasts a message to all connected WebSocket clients.

    This function sends the provided message to every client in the
    connected_clients list.

    Args:
        message (str): The message to broadcast to all connected clients
    """
    for client in connected_clients:
        await client.send_text(message)
