# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 15:29:57 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 18
"""

import asyncio

from random import random

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# Tasks with timeouts

# It is a best practice to use a timeout when waiting for a long-running task. If the task does
# not complete within a given time limit, it can then be canceled and perhaps tried again, or
# an error raised.

# The asyncio module provides the timeout() asynchronous context manager to address
# exactly this problem.

# The benefit of asyncio.timeout() being a context manager, means that we can await many
# coroutines, e.g. many sub-tasks, within the body and only cancel the one task that takes too
# long.
# =============================================================================

# Set a timeout
async with asyncio.timeout(5):
    # Execute long running task
    result = await task()
    
    # You can also execute many tasks
    await task1()
    await task2()
    await task3()
    
#%%
# =============================================================================
# You need to handle the TimeoutError in case there are tasks left after the timeout completes
# =============================================================================

try:
    async with asyncio.timeout(5):
        # Execute long running task
        result = await task(1)
        
        # Report the result
        print(result)
except asyncio.TimeoutError:
    print("Timeout waiting")
    
#%%
# =============================================================================
# You can reschedule and check the status of the timeout with three functions
# asyncio.Timeout.when(): Return the current deadline
# asyncio.Timeout.reschedule(): Change the current deadline to a new time.
# asyncio.Timeout.when(): expired() Return True if the timeout has expired, False
# otherwise.
# =============================================================================

# Set no timeout
async with asyncio.timeout(None) as timeout:
    # Do something else
    # ...
    
    # Calculate a deadline 5 seconds in the future
    loop = asyncio.get_running_loop()
    deadline = loop.time() + 5
    
    # Set the new deadline
    timeout.reschedule(deadline)
    
    # Execute long running task
    result = await tsk()
    
#%%
# =============================================================================
# Example of timeout with a long running task
# =============================================================================

async def task(value):
    await asyncio.sleep(10)
    
    return value * 100

async def main():
    # Schedule the task
    running_task = asyncio.create_task(task(1))
    
    # Allow the task to run
    await asyncio.sleep(0)
    
    # Handle the timeout
    try:
        async with asyncio.timeout(5):
            # Wait for the task to complete
            result = await running_task
            
            # Report the result
            print(result)
    except asyncio.TimeoutError:
        print("Timeout waiting")
        
asyncio.run(main())

#%%
# =============================================================================
# Example of a timeout delay set later
# =============================================================================

async def task(value):
    await asyncio.sleep(10)
    
    return value * 100

async def main():
    # Handle timeout
    try:
        # Set the timeout
        async with asyncio.timeout(None) as timeout:
            await asyncio.sleep(1)
            
            # Set a deadline 5 seconds in the future
            loop = asyncio.get_running_loop()
            deadline = loop.time() + 5
            
            # set the new deadline
            timeout.reschedule(deadline)
            
            # Execute long running task
            result = await task(1)
            
    except asyncio.TimeoutError:
        print("Timeout waiting")
        
asyncio.run(main())

#%%
# =============================================================================
# Example of extending a timeout
# =============================================================================

async def task(value):
    await asyncio.sleep(10)
    
    return value * 100

async def main():
    # Handle the timeout
    try:
        async with asyncio.timeout(5) as timeout:
            # Simulate a long running task
            await asyncio.sleep(4)
            
            # Set deadline 11 seconds into the future
            loop = asyncio.get_running_loop()
            deadline = loop.time() + 11
            
            # Set the new deadline
            timeout.reschedule(deadline)
            
            # Execute long running task
            result = await task(1)
            print(result)
    except asyncio.TimeoutError:
        print("Timeout waiting")
        
asyncio.run(main())