# src/run_server.py

import asyncio
import os
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from src.server.nebulalink_server import NebulaLinkServer


async def main():
    server = NebulaLinkServer("localhost", 8765)
    await server.start()
    print("Server is running. Press Ctrl+C to stop.")
    try:
        await asyncio.Future()  # Run forever
    except KeyboardInterrupt:
        print("Stopping server...")
    finally:
        server.stop()


if __name__ == "__main__":
    asyncio.run(main())
