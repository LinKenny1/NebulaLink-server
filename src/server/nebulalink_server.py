# src/server/nebulalink_server.py

import asyncio
import websockets
import json
from typing import Set, Dict, Any

from utils import get_logger, NebulaLinkError, handle_error

logger = get_logger(__name__)

class NebulaLinkServer:
    def __init__(self, host: str = 'localhost', port: int = 8765):
        self.host = host
        self.port = port
        self.clients: Set[websockets.WebSocketServerProtocol] = set()

    async def register(self, websocket: websockets.WebSocketServerProtocol):
        self.clients.add(websocket)
        logger.info(f"New client connected. Total clients: {len(self.clients)}")

    async def unregister(self, websocket: websockets.WebSocketServerProtocol):
        self.clients.remove(websocket)
        logger.info(f"Client disconnected. Total clients: {len(self.clients)}")

    async def send_to_client(self, websocket: websockets.WebSocketServerProtocol, message: Dict[str, Any]):
        await websocket.send(json.dumps(message))

    async def broadcast(self, message: Dict[str, Any]):
        if self.clients:
            await asyncio.wait([client.send(json.dumps(message)) for client in self.clients])

    async def handle_message(self, websocket: websockets.WebSocketServerProtocol, message: str):
        try:
            data = json.loads(message)
            action = data.get('action')

            if action == 'ping':
                await self.send_to_client(websocket, {'action': 'pong'})
            else:
                logger.warning(f"Unknown action received: {action}")
                await self.send_to_client(websocket, {'error': 'Unknown action'})

        except json.JSONDecodeError:
            logger.error("Received invalid JSON")
            await self.send_to_client(websocket, {'error': 'Invalid JSON'})
        except Exception as e:
            error_details = handle_error(e)
            await self.send_to_client(websocket, {'error': error_details})

    async def ws_handler(self, websocket: websockets.WebSocketServerProtocol, path: str):
        await self.register(websocket)
        try:
            async for message in websocket:
                await self.handle_message(websocket, message)
        finally:
            await self.unregister(websocket)

    async def start(self):
        server = await websockets.serve(self.ws_handler, self.host, self.port)
        logger.info(f"Server started on {self.host}:{self.port}")
        await server.wait_closed()

def run_server():
    server = NebulaLinkServer()
    asyncio.run(server.start())

if __name__ == "__main__":
    run_server()