"""The package entry point into the application."""

import asyncio
from .app import run

if __name__ == "__main__":
    asyncio.run(run())
