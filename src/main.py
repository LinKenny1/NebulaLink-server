# src/main.py

import asyncio
from server.nebulalink_server import NebulaLinkServer
from utils import get_logger

logger = get_logger(__name__)

async def main():
    server = NebulaLinkServer()
    logger.info("Starting NebulaLink Server...")
    await server.start()

if __name__ == "__main__":
    asyncio.run(main())