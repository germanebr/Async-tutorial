# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 11:37:59 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 11
"""

import asyncio

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# We usually need to perform some activity when an asyncio task is done, but it
# can be challenging given the asynchronous nature of tasks. The
# solution is to use a callback function, triggered when a task is done.

# We can configure a task to automatically execute one or more regular Python functions once
# the task is done.
# These are called callback functions.

# You can create a callback on a task with the add_done_callback()

# The add_done_callback() method can be used to add or register as many done callback
# functions as we like.
# =============================================================================

# Done callback function
def handle(task):
    print(task)
    
# Register the done callback function
task.add_done_callback(handle)

# You can also remove the callback
task.remove_done_callback(handle)

#%%
# =============================================================================
# Example of adding a done callback function
# =============================================================================

# Custom done callback function
def callback(task):
    print("Task is completed!")
    
async def task_coroutine():
    print("\tExecuting the task")
    
    await asyncio.sleep(1)
    
async def main():
    print("Main coroutine started")
    
    # Create and schedule the task
    task = asyncio.create_task(task_coroutine())
    
    # Add a done callback function
    task.add_done_callback(callback)
    
    await task
    
    print("Main coroutine done")
    
asyncio.run(main())

#%%
# =============================================================================
# Example of adding more than one callback
# =============================================================================

# First done callback with a generic message
def callback1(task):
    print("\tTask is done!")
    
# Second done callback reports the details of the task
def callback2(task):
    print(f"\tTask: {task}")
    
async def task_coroutine():
    print("\tExecuting the task")
    
    await asyncio.sleep(1)
    
async def main():
    print("Main coroutine started")
    
    # Create and schedule the task
    task = asyncio.create_task(task_coroutine())
    
    # Add first callback function
    task.add_done_callback(callback1)
    
    # Add second callback function
    task.add_done_callback(callback2)
    
    await task
    
    print("Main coroutine done")
    
asyncio.run(main())

#%%
# =============================================================================
# Example of removing a done callback
# =============================================================================

# Custom done callback function
def callback(task):
    print("Task is completed!")
    
async def task_coroutine():
    print("\tExecuting the task")
    
    await asyncio.sleep(1)
    
async def main():
    print("Main coroutine started")
    
    # Create and schedule the task
    task = asyncio.create_task(task_coroutine())
    
    # Add a done callback function
    task.add_done_callback(callback)
    
    # Wait a moment to let the task run
    await asyncio.sleep(0.1)
    
    # Remove the task
    task.remove_done_callback(callback)
    
    await task
    
    print("Main coroutine done")
    
asyncio.run(main())

#%%
# =============================================================================
# You can also add a callback even when the task is already done.
# In this case, the callback will be executed as soon as it cans.
# =============================================================================

# Custom done callback function
def callback(task):
    print("Task is completed!")
    
async def task_coroutine():
    print("\tExecuting the task")
    
    await asyncio.sleep(1)
    
async def main():
    print("Main coroutine started")
    
    # Create and schedule the task
    task = asyncio.create_task(task_coroutine())
    
    await task
    
    # Add a done callback function
    task.add_done_callback(callback)
    
    print("Main coroutine done")
    
asyncio.run(main())