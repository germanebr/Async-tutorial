# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 12:30:26 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 29
"""

import asyncio

from random import random

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# Conditions

# It is common for one or more tasks to wait on an activity to be completed by
# another task.
# Rather than requiring the task to complete and have other task wait upon it, we can use a
# concurrency primitive designed for this purpose called a monitor or a condition variable.
# The condition variable implements the common wait/notify and wait/notify-all patterns for
# concurrent programming. Dependent tasks can wait on the condition variable and the target
# task can complete its work and notify all interested parties that a condition has been met
# and they are able to resume.

# A condition (or monitor) allows multiple coroutines to be notified about some result.
# It is the combination of a lock and an event.
# =============================================================================

async def task(condition, work_list):
    await asyncio.sleep(1)
    
    # Add data to the work list
    work_list.append(33)
    
    # Notify a waiting coroutine that the work is done
    print("\t> Task sending notification")
    async with condition:
        condition.notify()
        
async def main():
    # Create a condition
    condition = asyncio.Condition()
    
    # Prepare the work list
    work_list = list()
    
    # Wait to be notified that the data is ready
    print("Main waiting for data...")
    
    async with condition:
        # Create and start the task
        _ = asyncio.create_task(task(condition, work_list))
        
        # Wait to be notified
        await condition.wait()
        
    # We know the data is ready
    print(f"Got data: {work_list}")
    
asyncio.run(main())

#%%
# =============================================================================
# Example of wait and notify all

# In this example, we will start a suite of tasks that will wait on the condition to be notified
# before performing their processing and reporting a result.
# The main coroutine will block for a moment and then notify all waiting coroutines that they
# can begin processing.
# =============================================================================

async def task(condition, number):
    print(f"\tTask {number} waiting...")
    
    # Acquire the condition
    async with condition:
        # Wait to be notified
        await condition.wait()
        
    value = random()
    await asyncio.sleep(value)
    
    print(f"\tTask {number} got {value}!")
    
async def main():
    # Create a condition
    condition = asyncio.Condition()
    
    # Create and schedule many tasks
    tasks = [asyncio.create_task(task(condition, i))
             for i in range(5)]
    
    # Allow the tasks to run
    await asyncio.sleep(1)
    
    # Acquire the condition
    async with condition:
        # Notify all waiting tasks
        condition.notify_all()
        
    # Wait for all tasks to complete
    _ = await asyncio.wait(tasks)
    
asyncio.run(main())

#%%
# =============================================================================
# Example of wait for

# The wait_for() method takes a callable, such as a function with no arguments or a lambda
# expression. The coroutine calling the wait_for() method will block until notified and the
# callable passed in as an argument returns a True value.
# This might mean that the coroutine is notified many times by different coroutines, but will
# only unblock and continue execution once the condition in the callable is met.
# =============================================================================

async def task(condition, work_list):
    # Acquire the condition
    async with condition:
        value = random()
        
        await asyncio.sleep(value)
        
        # Add work to the list
        work_list.append(value)
        print(f"\tTask added {value}")
        
        # Notify the waiting coroutine
        condition.notify()
        
async def main():
    # Create the condition
    condition = asyncio.Condition()
    
    work_list = list()
    
    # Create and start many tasks
    _ = [asyncio.create_task(task(condition, work_list))
         for _ in range(5)]
    
    # Acquire the condition
    async with condition:
        # Wait to be notified
        await condition.wait_for(lambda: len(work_list) == 5)
        
        print(f"Done! Got {work_list}")
        
asyncio.run(main())