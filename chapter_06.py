# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 16:25:49 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 6
"""

import asyncio

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# Coroutines are how we define behavior in asyncio programs, but tasks are how
# they are executed.

# The name of a task helps keeping track for debugging

# It can be set when the task is created from a coroutine via the name argument
# =============================================================================

# Create a named task from a coroutine
task = asyncio.create_task(coro(), name = "MyTask")

# It can also be named as follows
task.set_name("MyTask")

# You can get the name of the task as well
name = task.get_name()

#%%
# =============================================================================
# Example on getting the default task name

# In this example, we will define a coroutine for a task that will report a message and block for
# a moment.
# We will then define the main coroutine that will be used as the entry point to the asyncio
# program. The main coroutine will report a message, then create and schedule the task
# coroutine. It will then wait for the task to be completed.
# =============================================================================

# Define the coroutine or a task
async def task_coroutine():
    # Report the message
    print("Executing the task")
    
    # Block for a moment
    await asyncio.sleep(1)
    
# Custom coroutine
async def main():
    # Report the message
    print("Main coroutine started")
    
    # Create and schedule the task
    task = asyncio.create_task(task_coroutine())
    # Wait for the task to be completed
    await task
    
    # Report the task
    print(task)
    # Report the task name
    print(f"Name: {task.get_name()}")
    
    # Report a final message
    print("Main coroutine completed!")
    
# Start the asyncio event loop
asyncio.run(main())

#%%
# =============================================================================
# Example on specifying the name of the tasks ourselves
# =============================================================================

# Define the coroutine or a task
async def task_coroutine():
    # Report the message
    print("Executing the task")
    
    # Block for a moment
    await asyncio.sleep(1)
    
# Custom coroutine
async def main():
    # Report the message
    print("Main coroutine started")
    
    # Create and schedule the task
    task = asyncio.create_task(task_coroutine(),
                               name = "MyTask")
    # Wait for the task to be completed
    await task
    
    # Report the task
    print(task)
    # Report the task name
    print(f"Name: {task.get_name()}")
    
    # Report a final message
    print("Main coroutine completed!")
    
# Start the asyncio event loop
asyncio.run(main())