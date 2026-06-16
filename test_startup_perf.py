import asyncio
import time
from src.api.main import lifespan, app

async def background_task():
    # If the event loop is blocked, this task won't even be able to start
    # or progress until the blocking is over.
    timestamps = []
    for _ in range(10):
        timestamps.append(time.time())
        await asyncio.sleep(0.1)
    timestamps.append(time.time())
    return timestamps

async def main():
    task = asyncio.create_task(background_task())

    # Give the background task a tiny bit of time to start its first sleep
    await asyncio.sleep(0.01)

    start_time = time.time()

    async with lifespan(app):
        startup_end_time = time.time()

    timestamps = await task

    print(f"Startup took: {startup_end_time - start_time:.4f}s")

    max_gap = 0
    for i in range(1, len(timestamps)):
        gap = timestamps[i] - timestamps[i-1]
        if gap > max_gap:
            max_gap = gap

    print(f"Maximum gap between background task iterations (expected ~0.1s): {max_gap:.4f}s")
    print(f"This indicates the event loop was blocked for: {max_gap - 0.1:.4f}s")

if __name__ == "__main__":
    asyncio.run(main())
