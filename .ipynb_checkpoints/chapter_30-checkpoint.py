# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 12:30:26 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 30
"""

import asyncio

from random import random

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# Semaphores

# A semaphore is a concurrency primitive that is used to signal between concurrent tasks.
# Semaphores are configurable and versatile, allowing them to be used like a mutex to protect a
# critical section, but also to be used as a coroutine-safe counter or a gate to protect a limited
# resource.

# A semaphore is a concurrency primitive that allows a limit on the number of coroutines that
# can acquire a lock protecting a critical section.
# Once at capacity (no more positions are available), new coroutines can only acquire a position
# on the semaphore once an existing coroutine holding the semaphore releases a position.

# Each time release() is called, it will increment the internal counter of the semaphore,
# regardless of the initial value. This can be used to increase the capacity of the semaphore
# dynamically.
# =============================================================================

# Create a semaphore with alimit of 100 calls
semaphore = asyncio.Semaphore(100)

# Acquire the semaphore (returns a coroutine that must be awaited)
await sempahore.acquire()

# Release the semaphore
semaphore.release()

# Increase dynamically the semaphore limit
semaphore.acquire()
# do something
# ...
# Release the semaphore
semaphore.release()

# Increase the size of the semaphore
for i in range(5):
    semaphore.release()
    
#%%
# =============================================================================
# Example of using an asyncio semaphore

# We will develop an example with a suite of coroutines but a limit on the number of coroutines
# that can perform an action simultaneously.
# A semaphore will be used to limit the number of concurrent coroutines which will be less
# than the total number of coroutines, allowing some coroutines to suspend, wait for a position,
# then be notified and acquire a position on the semaphore.
# =============================================================================

async def task(semaphore, number):
    # Acquire the semaphore
    async with semaphore:
        # Generate a random value and report
        value = random()
        
        await asyncio.sleep(value)
        
        print(f"Task {number} got {value}")
        
async def main():
    # Create the shared semaphore
    semaphore = asyncio.Semaphore(2)
    
    # create and schedule tasks
    tasks = [asyncio.create_task(task(semaphore, i))
             for i in range(10)]
    
    # Wait for all tasks to complete
    _ = await asyncio.wait(tasks)
    
asyncio.run(main())