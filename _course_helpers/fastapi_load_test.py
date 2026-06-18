import asyncio
import threading
import time

from fastapi import FastAPI

app = FastAPI()


@app.get("/async/{id}")
async def async_func(id: int):
    print(f"sync. Потоков: {threading.active_count()}")
    print(f"async. Начал {id}: {time.time()}:.2f")
    await asyncio.sleep(3)
    print(f"async. Закончил {id}: {time.time()}:.2f")


@app.get("/sync/{id}")
async def sync_func(id: int):
    print(f"sync. Потоков: {threading.active_count()}")
    print(f"sync. Начал {id}: {time.time()}:.2f")
    time.sleep(3)
    print(f"aync. Закончил {id}: {time.time()}:.2f")
