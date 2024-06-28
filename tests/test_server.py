# tests/test_server.py

import pytest
import asyncio
import websockets
import json
from src.server import NebulaLinkServer

@pytest.fixture
async def server():
    server = NebulaLinkServer('localhost', 8765)
    task = asyncio.create_task(server.start())
    yield server
    task.cancel()
    await asyncio.sleep(0.1)  # Allow time for server to shut down

@pytest.mark.asyncio
async def test_server_connection(server):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({"action": "ping"}))
        response = await websocket.recv()
        assert json.loads(response) == {"action": "pong"}

@pytest.mark.asyncio
async def test_unknown_action(server):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({"action": "unknown"}))
        response = await websocket.recv()
        assert json.loads(response) == {"error": "Unknown action"}

# Add more tests for other server functionalities