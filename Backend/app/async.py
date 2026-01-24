import asyncio
import time
from rich import print


async def endpoint(route):
    print(f">> handling {route}")

    # emulate databse delay
    await asyncio.sleep(1)

    print(f"<< response {route}")
    return route


async def server():
    # Run test requests
    tests = (
        "GET /shipment?id=1",
        "PATCH /shipment?id=4",
        "GET /shipment?id=3",
    )

    start = time.perf_counter()

    async with asyncio.TaskGroup() as task_group:
        tasks = [task_group.create_task(endpoint(route)) for route in tests]

    end = time.perf_counter()
    print(f"Time taken: {end - start: .2f}s")


# Run server
asyncio.run(server())
