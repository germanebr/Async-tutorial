# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 16:33:36 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 10
"""

import asyncio

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# Handling asyncio unhandled exceptions

# A coroutine within a task may raise an exception that is not handled.
# This will cause the task to fail and terminate.
# We are able to check if a task has failed with an unhandled exception.

# We can retrieve an unhandled exception in a task via the exception() method.
# If an unhandled exception was not raised in the task, then a value of None is returned.
# =============================================================================

# Get the exception raised by a task
exception = task.exception()

#%%
# =============================================================================
# Check for an exception in a cancelled task

# The CancelledError exception IS NOT RAISED when calling the exception() method
# =============================================================================

# check if the task was not cancelled
if not task.cancelled():
    # Get the exception raised by a task
    exception = task.exception()
else:
    # Task was cancelled
    pass

#%%
# =============================================================================
# Check for an exception on a running task

# If the task is not yet done, an InvalidStateError exception is raised when
# calling for the exception() function.
# =============================================================================

# Check if the task is not done
if not task.done():
    await task
# Get the exception raised by a task after
exception = task.exception()

#%%
# =============================================================================
# If a task fails with an unhandled exception and the exception is not retrieved via the
# exception() method, then it is generally referred to as a “never-retrieved” exception.
# The asyncio event loop will automatically report never-retrieved exceptions as part of shutting
# down an asyncio program.
# =============================================================================

# Define the exception handler
def exception_handler(loop, context):
    # Get the exception
    ex = context['exception']
    # Log details
    print(f"got excpetion {ex}")
    
# We can configure the event loop to call this function for never-retrieved exceptions
loop = asyncio.get_running_loop()

# Set the exception handler
loop.set_exception_handler(exception_handler)

#%%
# =============================================================================
# Example of checking for a task exception

# In this example, we can define a
# task coroutine to explicitly raise an exception that is not handled.
# This will cause the task coroutine to fail.
# The main coroutine will sleep to wait for the task to be completed. This is to avoid using the
# await expression which will propagate the exception back to the caller.
# Once the task is done, the main coroutine will retrieve and report the exception raised in the
# task.
# =============================================================================

async def task_coroutine():
    print("Executing task")
    
    # block for a moment
    await asyncio.sleep(1)
    
    #raise an exception
    raise Exception("Something bad happened")
    
async def main():
    print("Main coroutine started")
    
    # create and schedule the task
    task = asyncio.create_task(task_coroutine())
    
    # wait for the task to complete
    await asyncio.sleep(1.1)
    
    # get the exception
    ex = task.exception()
    
    # report the details of the exception
    print(f"exception: {ex}")
    
    print("Main coroutine done")
    
asyncio.run(main())

#%%
# =============================================================================
# Example of handling a task exception
# =============================================================================

async def task_coroutine():
    print("\tExecuting task")
    
    await asyncio.sleep(1)
    
    raise Exception('Something bad happened')
    
async def main():
    print("Main coroutine started")
    
    task = asyncio.create_task(task_coroutine())
    
    # Wait for the task to complete
    try:
        await task
    except Exception as e:
        # report the exception
        print(f"\tFailed with: {e}")
        
    print("Main coroutine done")
    
asyncio.run(main())

#%%
# =============================================================================
# Handling a task exception with result
# =============================================================================

async def task_coroutine():
    print("\tExecuting the task")
    
    await asyncio.sleep(1)
    
    # Fail with an exception
    raise Exception("Something bad happened")
    
    # Return a value (never reached)
    return 100

async def main():
    print("Main coroutine started")
    
    task = asyncio.create_task(task_coroutine())
    
    await asyncio.sleep(1.1)
    
    try:
        # get the result
        value = task.result()
    except Exception as e:
        print(f"\tFailed with: {e}")
        
    print("Main coroutine done")
    
asyncio.run(main())