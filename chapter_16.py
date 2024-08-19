# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 14:40:58 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 16
"""

import asyncio

from random import random

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# Tasks as completed

# It is common to issue many tasks at once, then need to process the results from each task as
# the tasks are completed.
# This can be more efficient than waiting for all tasks to complete before handling the results.
# We can achieve this and iterate tasks in the order they are done using the as_completed()
# function.

# Importantly, the asyncio.as_completed() function does not return an iterable of return
# values of provided awaitables. Instead, it returns an iterable that when traversed will yield
# awaitables (or wrapped awaitables) in the provided list.
# These can be awaited by the caller in order to get results in the order that tasks are completed,
# e.g. get the result from the next task to complete.
# =============================================================================

for task in asyncio.as_completed(tasks):
    result = await task
    
# You can also specify a timeout for executing the tasks (need to handle a TimeoutError if the tasks are not completed by that time)
try:
    for task in asyncio.as_completed(tasks, timeout = 10):
        result = await task
except asyncio.TimeoutError:
    pass

# =============================================================================
# You can also manage all the coroutines inside the function without blocking the rest of the code

# You block the code UNTIL YOU AWAIT a coroutine

# You can iterate with a regular for loop the generator
# =============================================================================

generator = asyncio.as_completed(tasks)

# get the next coroutine
coro = next(generator)

# get a result from the next task to complete
result = await coro

#%%
# =============================================================================
# Example of as completed with tasks
# =============================================================================

async def task_coro(arg):
    # Generate a random value between 0 and 1
    value = random()
    await asyncio.sleep(value)
    
    return arg * value

async def main():
    # Create many tasks
    coros = [asyncio.create_task(task_coro(i)) for i in range(10)]
    
    # get results as tasks are completed
    for coro in asyncio.as_completed(coros):
        # Get the result from the next task to complete
        result = await coro
        print(f"\t>Got {result}")
        
asyncio.run(main())

#%%
# =============================================================================
# Example of as completed with timeout
# =============================================================================

async def task_coro(arg):
    # Generate a random value between 0 and 1
    value = random()
    await asyncio.sleep(value)
    
    return arg * value

async def main():
    # Create many tasks
    coros = [asyncio.create_task(task_coro(i)) for i in range(10)]
    
    # Handle the timeout
    try:
        for coro in asyncio.as_completed(coros, timeout = 0.5):
            result = await coro
            print(f"\t>Got {result}")
    except asyncio.TimeoutError:
        print("Gave up after timeout")
        
asyncio.run(main())

#%%
# =============================================================================
# Example of as completed with an exception

# Will fail since we're not handling the exception
# =============================================================================

async def task_coro(arg):
    # Generate a random value between 0 and 1
    value = random()
    
    # Block for a moment
    await asyncio.sleep(value)
    
    # Check if the task should fail
    if value > 0.5:
        raise Exception("Something bad happened")
    
    return arg * value

async def main():
    # Create many tasks
    coros = [asyncio.create_task(task_coro(i)) for i in range(10)]
    
    # get results as tasks are completed
    for coro in asyncio.as_completed(coros):
        # Get the result from the next task to complete
        result = await coro
        print(f"\t>Got {result}")
        
asyncio.run(main())