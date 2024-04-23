#!/usr/bin/env python3
""" Task 0 """

import asyncio
import random
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    """
    Asynchronous generator yielding random
    numbers between 0 and 10 with 1 second delay.
    """

    for _ in range(10):
        await asyncio.sleep(1)
        yield random.random() * 10
