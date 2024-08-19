# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 12:06:49 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 20
"""

import asyncio

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# Sleep tasks

# The sleep() function has many uses.
# In practice, it can be used to allow a task to wait a fixed time before performing an action.
# This can be helpful in order to avoid overloading a resource, such as a remote server or
# database.

# A sleep can also be used to wait for a condition in a program, such as for another task to
# complete or for a variable to be set to True.
# This is called a wait loop and allows the waiting task to perform actions while also waiting
# for a condition.

# Another important use for sleep in asyncio programs is to suspend the current task and allow
# other coroutines to execute.

# Sleeping for zero seconds will suspend the current task and give an opportunity to other
# tasks to run.
# =============================================================================

# Run forever
while True:
    # Check for a condition
    if condition():
        # Stop waiting
        break
    # Otherwise, sleep for a moment
    await asyncio.sleep(0.2)
    
# Allow other tasks to run for a moment
await asyncio.sleep(0)
    
#%%
# =============================================================================
# Example of sleeping a task
# =============================================================================

# custom coroutine
async def custom_coro():
    # report a message
    print('task running')
    # block for a moment
    await asyncio.sleep(1)
    # report a message
    print('task done')
    
# entry point coroutine
async def main():
    # execute another task
    await asyncio.create_task(custom_coro())
    
# start the asyncio event loop
asyncio.run(main())

#%%
# =============================================================================
# Example of sleep with a return value
# =============================================================================

async def main():
    # get the sleep awaitable
    awaitable = asyncio.sleep(0.1)
    # report the awaitable
    print(type(awaitable))
    print(awaitable)
    # await the awaitable
    await awaitable
    
# start the asyncio event loop
asyncio.run(main())

#%%
# =============================================================================
# Example of sleeping zero seconds
# =============================================================================

async def custom_coro():
    print('task running')
    # block for a moment
    await asyncio.sleep(1)
    
    # report a message
    print('task done')
    
async def main():
    # Execute another coroutine
    task = asyncio.create_task(custom_coro())
    
    print("Main is blocking now")
    await asyncio.sleep(0)
    
    print("Main is done blocking")
    await task
    
asyncio.run(main())

#%%
# =============================================================================
# Example of periodic task with sleep

# This code keeps running the periodic task because of Spyder main event loop
# The code will stop after main is done on a regular Python script
# =============================================================================

async def periodic():
    while True:
        print("\t>Task is running...")
        await asyncio.sleep(0.2)
        
async def main():
    print("Main is starting")
    
    # Start the periodic task
    _ = asyncio.create_task(periodic())
    
    # Report a message
    print("Main is resuming with work...")
    
    # Wai a while for some reason
    await asyncio.sleep(3)
    
    print("Main is done")
    
asyncio.run(main())