# src/server/nebulalink_server.py

import asyncio
import websockets
import json
from typing import Set, Dict, Any

from utils import get_logger, NebulaLinkError, handle_error
from controllers.power_controller import PowerController
from controllers.display_controller import DisplayController
from controllers.program_controller import ProgramController

logger = get_logger(__name__)

class NebulaLinkServer:
    def __init__(self, host: str = 'localhost', port: int = 8765):
        self.host = host
        self.port = port
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.power_controller = PowerController()
        self.display_controller = DisplayController()
        self.program_controller = ProgramController()

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
            elif action == 'shutdown':
                result = self.power_controller.shutdown()
                await self.send_to_client(websocket, result)
            elif action == 'restart':
                result = self.power_controller.restart()
                await self.send_to_client(websocket, result)
            elif action == 'sleep':
                result = self.power_controller.sleep()
                await self.send_to_client(websocket, result)
            elif action == 'hibernate':
                result = self.power_controller.hibernate()
                await self.send_to_client(websocket, result)
            elif action == 'get_power_plans':
                result = self.power_controller.get_power_plans()
                await self.send_to_client(websocket, {'action': 'power_plans', 'plans': result})
            elif action == 'set_power_plan':
                result = self.power_controller.set_power_plan(data.get('guid'))
                await self.send_to_client(websocket, result)
            elif action == 'get_display_info':
                result = self.display_controller.get_display_info()
                await self.send_to_client(websocket, {'action': 'display_info', 'displays': result})
            elif action == 'set_resolution':
                result = self.display_controller.set_resolution(data.get('display_id'), data.get('width'), data.get('height'))
                await self.send_to_client(websocket, result)
            elif action == 'set_refresh_rate':
                result = self.display_controller.set_refresh_rate(data.get('display_id'), data.get('rate'))
                await self.send_to_client(websocket, result)
            elif action == 'enable_dummy_display':
                result = self.display_controller.enable_dummy_display()
                await self.send_to_client(websocket, result)
            elif action == 'disable_dummy_display':
                result = self.display_controller.disable_dummy_display()
                await self.send_to_client(websocket, result)
            elif action == 'get_running_programs':
                result = self.program_controller.get_running_programs()
                await self.send_to_client(websocket, {'action': 'running_programs', 'programs': result})
            elif action == 'pause_program':
                result = self.program_controller.pause_program(data.get('pid'))
                await self.send_to_client(websocket, result)
            elif action == 'resume_program':
                result = self.program_controller.resume_program(data.get('pid'))
                await self.send_to_client(websocket, result)
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