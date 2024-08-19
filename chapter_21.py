# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 13:17:05 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 21
"""

import asyncio

from random import random

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# Wait for tasks

# It is a good practice that any waiting performed in an asyncio program be limited to a
# timeout.
# This is because something may go wrong when waiting on a resource and the program may
# be blocked for an extended period of time. Instead, we should wait for a reasonable amount
# of time and then take action, such as retry or give up.

# Asyncio provides a way to wait on another task with a timeout via the asyncio.wait_for()
# function. If the timeout elapses before the task completes, the task is canceled and the caller
# receives an exception.
# =============================================================================

async def task_coro():
    # Generate a random value between 1 and 2
    value = 1 + random()
    print(f"\t>Task will sleep for {value} seconds...")
    
    await asyncio.sleep(value)
    
    print("\t>Task done!")
    
async def main():
    task = asyncio.create_task(task_coro())
    
    # execute and wait for the task without a timeout
    try:
        await asyncio.wait_for(task,
                               timeout = 0.2)
        
    # Check for a TimeoutError if the task is not completed on the assigned time
    except asyncio.TimeoutError:
        print("Gave up waiting, task cancelled")
        
asyncio.run(main())

#%%
# =============================================================================
# Example of waiting on a task that fails
# =============================================================================

async def task_coro(arg):
    value = arg * random()
    
    print(f"\t>Task will sleep for {value} seconds")
    await asyncio.sleep(value)
    
    # Fail with an exception
    raise Exception("Something bad happened!")
    
    print("\t>Task done")
    
async def main():
    task = task_coro(1)
    
    # You need to handle two exceptions: one for the timeout of the wait, and another for a possible exception generated on the task
    try:
        await asyncio.wait_for(task,
                               timeout = 2.0)
    except asyncio.TimeoutError:
        print("Gave up waiting... Task cancelled")
    except Exception as e:
        print(f"Task failed with: {e}")
        
asyncio.run(main())

#%%
# =============================================================================
# Example waiting on a task that is cancelled
# =============================================================================

async def task_coro(arg):
    value = arg * random()
    
    print(f"\t>Task will sleep for {value} seconds")
    await asyncio.sleep(value)
    
    print("\t>Task done")
    
async def task_cancel(task):
    await asyncio.sleep(0.3)
    task.cancel()
    
async def main():
    task = asyncio.create_task(task_coro(1))
    
    # Create the wait for coroutine
    wait_coro = asyncio.wait_for(task,
                                 timeout = 1)
    
    # Create and run the cancel task
    asyncio.create_task(task_cancel(task))
    
    # Await the wait_for coroutine
    try:
        await wait_coro
    except asyncio.TimeoutError:
        print("Gave up waiting... Task cancelled")
    except asyncio.CancelledError:
        print(f"Task was cancelled externally")
        print(task)
        
asyncio.run(main())