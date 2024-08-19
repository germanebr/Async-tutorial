# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 15:55:12 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 5
"""

import asyncio

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# An asyncio task is a class that schedules and independentrly runs an asyncio coroutine.

# They allow to be queried, canceled, and results and exceptions to be retrieved later.

# A task is created from a coroutine, so it necessarily requires a coroutine.

# A task is scheduled in the asyncio event loop and will execute regardless of
# what else happens in the coroutine that created it.

# Tasks are awaitable.

# A future is a lower-level class that represents a result that will eventually arrive.

# Tasks are created on a factory function that takes a coroutine and returns the task object.

# Use asyncio.create_task() to create a task from a coroutine.

# A task will not run until the event loop is given an opportunity to run it.
# =============================================================================

# Create and schedule a task (don't do)
task = asyncio.create_task(task_coroutine())

# You can await the result if desired (don't do)
await task

# It's preferred to await the command directly (it'll create the task automatically)
await task_coroutine()

#%%
# =============================================================================
# Code that defines a task coroutine that reports a message and sleeps for a moment
# =============================================================================

# Define a coroutine for a task
async def task_coroutine():
    # Report a message
    print("Executing the task")
    
    # Block for a moment
    await asyncio.sleep(1)
    
    # Make sure the task ends
    print("Task completed")
    
# Custom coroutine
async def main():
    # Report the message
    print("Main coroutine started")
    
    # Create and schedule the task
    task = asyncio.create_task(task_coroutine())
    
    # Wait for the task to complete
    await task
    
    # Report final message
    print("Main coroutine done")
    
# Start the asyncio event loop
asyncio.run(main())

#%%
# =============================================================================
# Example creating multiple tasks

# We'll update the task coroutine to take an integer argument that is then reported
# The main coroutine will create many tasks from the task coroutine in a loop, using list comprehension.
# =============================================================================

# Define the task coroutine
async def task_coroutine(number):
    # Report a message
    print(f"Executing the task {number}")
    
    # Block for a moment
    await asyncio.sleep(1)
    
    # Report the end of the task
    print(f"Finished task {number}")
    
# Custom coroutine
async def main():
    # Report a message
    print("Main coroutine started")
    
    # Create and schedule many tasks
    tasks = [asyncio.create_task(task_coroutine(i)) for i in range(20)]
    
    # Wait for each task to complete
    for task in tasks:
        await task
        
    # Report final message
    print("Main coroutine done")
    
# Start the asyncio event loop
asyncio.run(main())

#%%
# =============================================================================
# Tasks must be created from coroutines

# Tasks must be run in the event loop

# Tasks must be assigned and the reference MUST be kept
# =============================================================================
