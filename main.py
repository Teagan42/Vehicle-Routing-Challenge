import argparse
import asyncio

import gevent
from gevent import monkey

from vrp.app import App

monkey.patch_all()  # Patches the standard library to cooperate with gevent


async def async_task(name, delay):
    print(f"Starting async task {name}")
    await asyncio.sleep(delay)
    print(f"Finished async task {name}")


def gevent_task(name, delay):
    print(f"Starting gevent task {name}")
    gevent.sleep(delay)
    print(f"Finished gevent task {name}")


async def main_asyncio():
    print("Running asyncio tasks")
    tasks = [async_task("A", 2), async_task("B", 3)]
    await asyncio.gather(*tasks)
    print("Finished asyncio tasks")


def main_gevent():
    print("Running gevent tasks")
    tasks = [gevent.spawn(gevent_task, "C", 2), gevent.spawn(gevent_task, "D", 3)]
    gevent.joinall(tasks)
    print("Finished gevent tasks")


app = App()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Attempts to optimize cost through vehicle routing given a set of delivery loads."
    )
    parser.add_argument(
        "file_path",
        type=str,
        required=True,
        help="Path to the file containing the load data to process.",
    )
    args = parser.parse_args()
    # Run asyncio tasks
    asyncio.run(main_asyncio())
