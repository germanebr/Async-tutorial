# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 11:56:23 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 12
"""

import asyncio

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# Gettint the main and current tasks

# The coroutine that is provided to asyncio.run() is the MAIN coroutine or task

# When the main coroutine exits, all other tasks are canceled and the asyncio event loop
# is terminated.

# The most important detail of the main coroutine is that when it is done, the event loop is
# CLOSED.
# =============================================================================

# Get the current task
task = asyncio.current_task()

# AFTER getting the current task, you can also get the current coroutine
coro = task.get_coro()

#%%
# =============================================================================
# Example of getting the main task
# =============================================================================

async def main():
    print("Main coroutine started")
    
    # Get the current task
    task = asyncio.current_task()
    
    print(task)
    
asyncio.run(main())

#%%
# =============================================================================
# Example of a coroutine accessing the task
# =============================================================================

async def another_coroutine():
    print("Executing the coroutine")
    
    # Get the current task
    task = asyncio.current_task()
    print(task)
    
async def main():
    print("Main coroutine started")
    
    # create and run a second coroutine
    await another_coroutine()
    
    print("Main coroutine done")
    
asyncio.run(main())

#%%
# =============================================================================
# Example of a new task accessing itself
# =============================================================================

async def another_coroutine():
    print("\tExecuting the task")
    
    # Get the current task
    task = asyncio.current_task()
    print("\t",task)
    
async def main():
    print("Main coroutine started")
    
    # Create and schedule another task
    task = asyncio.create_task(another_coroutine())
    
    await task
    
    print("Main coroutine done")
    
asyncio.run(main())