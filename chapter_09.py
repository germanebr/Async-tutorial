# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 15:11:21 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 9
"""

import asyncio

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# Task results

# The result of a task is the return value from the coroutine that it executes.
# If the coroutine does not explicitly return a value, then the result of the task will be None.
# =============================================================================

# get the return value from the wrapped coroutine
value = task.result()

#%%
# =============================================================================
# If the coroutine fails with an unhandled exception, it is re-raised when calling the result()
# method and may need to be handled.
# =============================================================================

try:
    # Get the return value from the wrapped coroutine
    value = task.result()
    
except Exception:
    # Task failed and there is no result
    pass

#%%
# =============================================================================
# If the task was canceled, then a CancelledError exception is raised when calling the
# result() method and may need to be handled.

# It is a good idea to check if the task was canceled first.
# =============================================================================

# Handle the error
try:
    value = task.result()
except asyncio.CancelledError:
    # task was cancelled
    
    
# Better if you check before if it was cancelled
if not task.cancelled():
    value = task.result()
else:
    # task was cancelled
    
#%%
# =============================================================================
# Retrieve reuslt from running task

# If the task is not done executing, it'll raise an InvalidStateError exception
# when trying to get a result before it finishes. You need to handle that error
# =============================================================================

try:
    value = task.result()
except asyncio.InvalidStateError:
    # Task is not yet done
    pass

# It's better to check beforehand
if not task.done():
    await task

# Get the result AFTER executing the task
value = task.result()



# Awaiting for a task automatically gets the result
value = await task

#%%
# =============================================================================
# Example of getting a result from a done task

# Instead of awaiting and getting the result separately, we can assign everythin in a single line
# value = await task

# We would prefer to use the result() method on the task when we know that the task is
# already done and the waiting was performed by other means, such as the asyncio.wait()
# function
# =============================================================================
async def task_coroutine():
    print("Executing the task")
    
    await asyncio.sleep(1)
    
    return 99

async def main():
    print("Executing main coroutine")
    
    task = asyncio.create_task(task_coroutine(),
                               name = "MyTask")
    
    await task
    
    value = task.result()
    print(f"Result: {value}")
    print("Main coroutine done")
    
asyncio.run(main())

#%%
# =============================================================================
# Example of getting a result from a failed task

# If the task fails with an unhandled exception, the exception will be re-raised when calling the
# result() method on the task to get the result.
# =============================================================================

async def task_coroutine():
    print("Executing the task")
    
    await asyncio.sleep(1)
    
    # Fail with an exception
    raise Exception("Something bad happened")
    
    # Return a value (never reached)
    return 99

async def main():
    print("Executing main coroutine")
    
    task = asyncio.create_task(task_coroutine())
    await asyncio.sleep(1.1)
    
    try:
        # Get the result
        value = task.result()
        print(f"Result: {value}")
        
    except Exception as e:
        print(f"Failed with: {e}")
    
    print("Main coroutine done")
    
asyncio.run(main())

#%%
# =============================================================================
# Example of getting a result from a cancelled task
# =============================================================================

async def task_coroutine():
    print("Executing the task")
    
    await asyncio.sleep(1)
    
    return 99

async def main():
    print("Main coroutine started")
    
    task = asyncio.create_task(task_coroutine())
    await asyncio.sleep(0.1)
    
    task.cancel()
    await asyncio.sleep(0.1)
    
    # This approach will end in a CancelledError
    # value = task.result()
    # print(f"Result: {value}")
    
    try:
        value = task.result()
        print(f"Result: {value}")
    except asyncio.CancelledError:
        print("Unable to get the result... cancelled")
    
    print("Main coroutine done")
    
asyncio.run(main())

