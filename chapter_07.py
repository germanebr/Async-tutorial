# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 12:07:25 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 7
"""

import asyncio

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# Because tasks are execute asynchronously, we often need tocheck on the
# status of the task, such as whether it is done, still running, or cancelled.

# You can check if a task is done with the done() function. It returns a boolean
# response determining if it finished running (not necessarily succesfully or completely).

# You can check if a task was cancelled with the cancelled() method. It also
# returns a boolean response
# =============================================================================

# Check if a task is done
if task.done():
    print("The task is done!")
else:
    print("The task is still running")
    
# Check if the task was cancelled
if task.cancelled():
    print("The task got cancelled")
    
#%%
# =============================================================================
# Example on checking if a task is done
# =============================================================================

# Define the coroutine for a task
async def task_coroutine():
    # Report a message
    print("Executing the task")
    
    # Block for a moment
    await asyncio.sleep(1)
    
# Custom coroutine
async def main():
    # Create and schedule the task
    task = asyncio.create_task(task_coroutine(),
                               name = "MyTask")
    
    # Check if it's done (will FALSE since it task has only been scheduled, but not executed)
    print(f"\tTask {task.get_name()} done: {task.done()}")
    
    # Wait a moment (allows executing the task)
    await asyncio.sleep(0.1)
    
    # Check again if done (will FALSE since it has suspended, but still running due to sleep)
    print(f"\tTask {task.get_name()} done: {task.done()}")
    
    # Wait for the task to complete
    await task
    
    # Check again if done
    print(f"\tTask {task.get_name()} done: {task.done()}")
    
# Start the asyncio event loop
asyncio.run(main())

#%%
# =============================================================================
# Example exception that causes a task to be done

# We can explore the status of a task where the wrapped coroutine fails with
# an unhandled exception.
# =============================================================================

async def task_coroutine():
    print("Executing the task")
    
    await asyncio.sleep(0.5)
    
    # Raise an exception
    raise Exception("Something bad happened")
    
async def main():
    task = asyncio.create_task(task_coroutine(),
                               name = "MyTask")
    
    # Will FALSE since just scheduled, but not executed
    print(f"\t>Task {task.get_name()} done: {task.done()}")
    
    await asyncio.sleep(0.1)
    
    # Will FALSE since suspended, but still running
    print(f"\t>Task {task.get_name()} done: {task.done()}")
    
    await asyncio.sleep(0.5)
    
    # Will TRUE even though the task has an exception that terminates the code
    print(f"\t>Task {task.get_name()} done: {task.done()}")
    
# Start the asyncio event loop
asyncio.run(main())

#%%
# =============================================================================
# Example on checking if a task was canceled

# Will explicitly cancel the task for this example
# The command cancel() requests the task cancellation, and in most cases it will
# cancel.
# =============================================================================

async def task_coroutine():
    print("Executing the task")
    
    await asyncio.sleep(1)
    
async def main():
    task = asyncio.create_task(task_coroutine(),
                               name = "MyTask")
    
    print(f"\t>Task {task.get_name()} canceled: {task.cancelled()}")
    
    await asyncio.sleep(0.1)
    
    # Cancel the task
    task.cancel()
    
    # Wait for the task to be done cancelling
    await asyncio.sleep(0.1)
    
    print(f"\t>Task {task.get_name()} canceled: {task.cancelled()}")
    print(f"\t>Task {task.get_name()} done: {task.done()}")
    
asyncio.run(main())