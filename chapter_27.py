# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 11:32:41 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 27
"""

import asyncio

from random import random

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# Locks

# Mutual exclusion locks or mutex locks for short can be used to protect critical sections of
# code from concurrent execution.
# It is possible to suffer race conditions if two or more coroutines operate upon the same
# variables, or if tasks are executed out of order.
# We can use locks to define atomic blocks of code where execution is serialized, e.g. made
# sequential.

# The below example show a situation where a race condition is met
# =============================================================================

async def task():
    global value
    
    # Retrieve the value
    tmp = value
    await asyncio.sleep(0)
    
    # Update the tmp value
    tmp += 1
    await asyncio.sleep(0)
    
    # Store the updated value
    value = tmp
    
async def main():
    global value
    
    value = 0
    coros = [task() for _ in range(10000)]
    
    # Execute all coroutines
    await asyncio.gather(*coros)
    
    # Report the value of the counter
    print(value)
    
asyncio.run(main())

#%%
# =============================================================================
# Example of asyncio lock
# =============================================================================

async def task(lock, num, value):
    # Acquire the lock to protect the critical section
    async with lock:
        print(f"\t>{num} got lock... sleeping for {value}")
        # Block for a moment
        await asyncio.sleep(value)
        
async def main():
    # Create a shared lock
    lock = asyncio.Lock()
    
    # Create many concurrent coroutines
    coros = [task(lock, i, random()) for i in range(10)]
    
    # Execute and wait for tasks to complete
    await asyncio.gather(*coros)
    
asyncio.run(main())

#%%
# =============================================================================
# Fixing an asyncio race condition
# =============================================================================

async def task(lock):
    # Acquire the lock
    async with lock:
        global value
        
        # Retrieve the value
        tmp = value
        await asyncio.sleep(0)
        
        # Update the tmp value
        tmp += 1
        await asyncio.sleep(0)
        
        # Store the updated value
        value = tmp
    
async def main():
    global value
    value = 0
    
    # Create the shared lock
    lock = asyncio.Lock()
    
    coros = [task(lock) for _ in range(10000)]
    
    # Execute all coroutines
    await asyncio.gather(*coros)
    
    # Report the value of the counter
    print(value)
    
asyncio.run(main())