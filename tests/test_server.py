# tests/test_server.py

import pytest
import asyncio
import websockets
import json


@pytest.mark.asyncio
async def test_server_connection():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({"action": "ping"}))
        response = await websocket.recv()
        assert json.loads(response) == {"action": "pong"}


@pytest.mark.asyncio
async def test_unknown_action():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({"action": "unknown"}))
        response = await websocket.recv()
        assert json.loads(response) == {"error": "Unknown action"}


# Add more tests for other server functionalities
