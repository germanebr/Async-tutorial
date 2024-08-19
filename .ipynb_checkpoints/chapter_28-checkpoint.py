# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 12:17:05 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 28
"""

import asyncio

from random import random

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# Events

# An event provides a way to notify coroutines that something has happened.
# This is achieved using a coroutine-safe manner that avoids race conditions.
# An event manages an internal boolean flag that can be either set or not set.
# Coroutines can check the status of the event, change the status of the event or wait on the
# event for it to be set.
# =============================================================================

async def task(event, number):
    # Wait for the event to be set
    await event.wait()
    
    # Generate a random value between 0 and 1
    value = random()
    
    # Block for a moment
    await asyncio.sleep(value)
    print(f"\t>Task {number} got {value}")
    
async def main():
    # Create a shared event object
    event = asyncio.Event()
    
    # Create and run the tasks
    tasks = [asyncio.create_task(task(event, i))
             for i in range(5)]
    
    # Allow the tasks to start
    print("Main coroutine blocking...")
    await asyncio.sleep(0)
    
    # Start processing in all tasks
    print("Main setting the event")
    event.set()
    
    # Await for all tasks to terminate
    _ = await asyncio.wait(tasks)
    
asyncio.run(main())