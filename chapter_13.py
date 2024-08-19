# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 12:32:39 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 13
"""

import asyncio

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# How to get all tasks

# One advantage of asyncio is that it can access all of the tasks that are
# currently running and are not yet done.
# =============================================================================

# We can get a collection of all scheduled and/or running tasks
tasks = asyncio.all_tasks()

#%%
# =============================================================================
# Example of getting all tasks
# =============================================================================

async def task_coroutine(value):
    print(f"\tTask {value} is running")
    
    await asyncio.sleep(1)
    
async def main():
    print("Main coroutine started")
    
    # start many tasks
    started_tasks = [asyncio.create_task(task_coroutine(i)) for i in range(10)]
    
    # get all tasks
    tasks = asyncio.all_tasks()
    
    # Report all tasks
    for task in tasks:
        print(f">Task {task.get_name()}, {task.get_coro()}")
        
    # wait for all tasks to complete
    for tasks in started_tasks:
        await task
        
asyncio.run(main())

#%%
# =============================================================================
# It's important to NOT include the current main task when awaiting all tasks

# If we do, it will generate a RunTimeError since the main task cannot await itself
# We need to take it out of the general list of running tasks.
# =============================================================================

async def task_coroutine(value):
    print(f"\tTask {value} is running")
    
    await asyncio.sleep(1)
    
async def main():
    print("Main coroutine started")
    
    # Start many tasks
    for i in range(10):
        asyncio.create_task(task_coroutine(i))
        
    # allow som of the tasks time to start
    await asyncio.sleep(0.1)
    
    # get all tasks
    tasks = asyncio.all_tasks()
    
    # get the current task
    current = asyncio.current_task()
    
    # remove the current task from the list
    tasks.remove(current)
    
    # wait for the rest of tasks to be done
    for task in tasks:
        await task
        
asyncio.run(main())