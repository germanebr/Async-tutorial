# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 11:28:04 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 19
"""

import asyncio

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# Shield tasks

# asyncio has a way of shielding tasks from cancellation with asyncio.shield()

# the request for cancellation made on the returned awaitable object is not
# propagated to the inner awaitable.
# This means that the request for cancellation is absorbed by the shield.

# Cancelling the task inside the shield cancels the shield as well
# =============================================================================

# Create a task
task = asyncio.create_task(coro())

# Create a shield for the task
shield = asyncio.shield(task)

# Cancel the shield (does not cancel the task)
shield.cancel()

#%%
# =============================================================================
# Example shielding a task from cancellation
# =============================================================================

async def simple_task(number):
    await asyncio.sleep(1)
    
    return number

async def cancel_task(task):
    await asyncio.sleep(0.2)
    
    # Cancel the task
    was_cancelled = task.cancel()
    print(f"Cancelled: {was_cancelled}")
    
async def main():
    # Create a coroutine
    coro = simple_task(1)
    
    # Create a task
    task = asyncio.create_task(coro)
    
    # Create a shielded task
    shielded = asyncio.shield(task)
    
    # Create the task to cancel the previous task
    asyncio.create_task(cancel_task(shielded))
    
    # Handle cancellation error
    try:
        result = await shielded
        print(f"\t>Got {result}")
    except asyncio.CancelledError:
        print("Shielded was cancelled")
        
    await asyncio.sleep(1)
    
    print(f"Shielded: {shielded}")
    print(f"Task: {task}")
    
asyncio.run(main())

#%%
# =============================================================================
# Example of shielding a coroutine from cancellation
# =============================================================================

async def simple_task(number):
    await asyncio.sleep(1)
    
    return number

async def cancel_task(task):
    await asyncio.sleep(0.2)
    
    # Cancel the task
    was_cancelled = task.cancel()
    print(f"Cancelled: {was_cancelled}")
    
async def main():
    # Create a coroutine
    coro = simple_task(1)
    
    # Create a shielded task
    shielded = asyncio.shield(coro)
    
    # Create the task to cancel the previous task
    asyncio.create_task(cancel_task(shielded))
    
    # Handle cancellation error
    try:
        result = await shielded
        print(f"\t>Got {result}")
    except asyncio.CancelledError:
        print("Shielded was cancelled")
        
    # get all tasks
    tasks = asyncio.all_tasks()
        
    await asyncio.sleep(1)
    
    print(f"Shielded: {shielded}")
    
    for task in tasks:
        print(f"Task: {task}")
    
asyncio.run(main())

#%%
# =============================================================================
# Example of cancelling shielded inner task
# =============================================================================

async def simple_task(number):
    await asyncio.sleep(1)
    
    return number

async def cancel_task(task):
    await asyncio.sleep(0.2)
    
    # Cancel the task
    was_cancelled = task.cancel()
    print(f"Cancelled: {was_cancelled}")
    
async def main():
    # Create the coroutine
    coro = simple_task(1)
    
    # Create a task
    task = asyncio.create_task(coro)
    
    # shield the task
    shielded = asyncio.shield(task)
    
    # Create the task to cancel the previous task
    asyncio.create_task(cancel_task(task))
    
    # Handle the cancellation
    try:
        result = await shielded
        print(f"\t>Got {result}")
        
    except asyncio.CancelledError:
        print("Shielded cancelled")
        
    await asyncio.sleep(1)
    
    print(f"Shielded: {shielded}")
    print(f"Task: {task}")
    
asyncio.run(main())