# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 14:32:20 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 8
"""

import asyncio

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# We may need to stop or cancel a task from executing after it has started. This may be for
# many reasons, such as we no longer require the result, or the running task may negatively
# impact the program.

# After cancelling a task, you need to handle the CancelledError exception it raises

# If a task is already done, it CANNOT BE CANCELLED and cancel() will be FALSE

# Requesting to cancel a task DOES NOT GUARANTEE the task will actually cancel
# =============================================================================

# The command will return a boolean value to establish if the task was succesfully cancelled or not
request_succesful = task.cancel()

# You can also specify a message argument for the cancellation exception
request_succesful = task.cancel("Task no longer needed")

#%%
# =============================================================================
# If the CancelledError exception is not handled within the task’s coroutine, the exception will
# bubble-up and the task will terminate with a canceled status. It will be canceled. Otherwise,
# if the CancelledError exception is handled within the task’s coroutine, the task will not be
# canceled.

# If a task is required to clean-up when it is canceled, this can be achieved with a try-finally
# block within the body of a task, or the CancelledError exception can be handled and
# re-raised.
# =============================================================================

async def task_coroutine():
    print("Executing the task")
    
    await asyncio.sleep(1)
    
async def main():
    print("Main coroutine started")
    
    # Schedule the task
    task = asyncio.create_task(task_coroutine(),
                               name = "MyTask")
    
    # Let the task execute
    await asyncio.sleep(0.1)
    
    # Cancel the task
    was_cancelled = task.cancel()
    
    print(f"Task {task.get_name()} was cancelled: {was_cancelled}")
    
    # Handle the cancellation exception
    try:
        # Wait for the task to cancel
        await task
    except asyncio.CancelledError:
        pass
    
    print(f"Task {task.get_name()} is cancelled: {task.cancelled()}")
    print("Main coroutine done")
    
asyncio.run(main())

#%%
# =============================================================================
# Example on cancelling a scheduled task

# You can also cancel tasks even when they haven't been executed, just scheduled
# It will also raise a Cancellederror exception that needs to be handled.

# If a scheduled task is canceled, it will raise a CancelledError exception when it is given an
# opportunity to run, but before the body of the task is executed.
# This means that a task cannot consume a request to cancel that is made prior to the task’s
# first opportunity to execute.
# =============================================================================

async def task_coroutine():
    print("Executing task")
    
    await asyncio.sleep(1)
    
async def main():
    print("Main coroutine started")
    
    task = asyncio.create_task(task_coroutine(),
                               name = "MyTask")
    
    # Cancel the task BEFORE executing
    was_cancelled = task.cancel()
    
    print(f"\tWas cancelled: {was_cancelled}")
    
    # Let the task execute the cancellation
    await asyncio.sleep(0.1)
    
    print(f"Cancelled: {task.cancelled()}")
    
    print("Main coroutine done")
    
asyncio.run(main())

#%%
# =============================================================================
# Example of a task handling the request to cancel

# This can be achieved by expecting and handling a CancelledError exception inside the task body.
# If a task’s coroutine handles the CancelledError, then the task will not be canceled, may
# continue to run, and will not be marked with the canceled status meaning the cancelled()
# method will return False.

# This means that although the cancel() method may return True indicating that the request
# to cancel was successful, it does not mean that will be canceled, only that the task has the
# potential to be canceled.
# =============================================================================

async def task_coroutine():
    try:
        print("Executing the task")
        
        await asyncio.sleep(1)
        
    except asyncio.CancelledError:
        print("Received a request to cancel")
        
async def main():
    print("Main coroutine started")
    
    task = asyncio.create_task(task_coroutine(),
                               name = "MyTask")
    
    await asyncio.sleep(0.1)
    
    # Cancel the task
    was_cancelled = task.cancel()
    
    print(f"Task was requested to cancel: {was_cancelled}")
    
    await asyncio.sleep(0.1)
    
    # Check the status of the task
    print(f"Was cancelled: {task.cancelled()}")
    
    print("Main coroutine done")
    
asyncio.run(main())

#%%
# =============================================================================
# Cancelling a task with a custom message
# =============================================================================

async def task_coroutine():
    try:
        print("Executing task")
        
        await asyncio.sleep(1)
        
    except asyncio.CancelledError as e:
        print(F"Received request to cancel with: {e}")
        
async def main():
    print("Main coroutine started")
    
    task = asyncio.create_task(task_coroutine(),
                               name = "MyTask")
    
    await asyncio.sleep(0.1)
    
    # Cancel the task
    was_cancelled = task.cancel("Stop right now!")
    
    print(f"Was requested to canel: {was_cancelled}")
    
    await asyncio.sleep(0.1)
    
    print(f"Task cancelled: {task.cancelled()}")
    
    print("Main coroutine done")
    
asyncio.run(main())