#!/usr/bin/env python3
'''Task 4's module. '''

import asyncio
from typing import List

task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    '''Executes task_wait_random n times.'''

    tasks = []
    for _ in range(n):
        tasks.append(task_wait_random(max_delay))
    results = await asyncio.gather(*tasks)
    return sorted(results)
