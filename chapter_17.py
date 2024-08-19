# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 15:07:12 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 17
"""

import asyncio

from random import random

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# Task Group

# You can use a TaskGroup to create and manage a collection of tasks. It has a
# number of benefits, such as canceling all tasks in the group if one task fails.

# asyncio.TaskGroup is the substitute of running separately create_task and gather
# NOTE: It is only available starting from Python 3.11

# Exiting the TaskGroup object’s block normally or via an exception will
# automatically await until all group tasks are done.

# The benefit of using the asyncio.TaskGroup is that we can issue multiple tasks in the group
# and execute code in between, such as checking results or gathering more data.
# =============================================================================

# Create a taskgroup
async with asyncio.TaskGroup() as group:
    # You can create a task inside the group
    task = group.create_task(coro())
    
    # you can also create and issue a task
    result = await group.create_task(coro())
    
# wait for all group tasks are done

#---------------------------------
# =============================================================================
# # If one task in the group fails with an exception, then all non-done tasks remaining in the
# # group will be canceled.
# =============================================================================

# Handle the failure of any tasks in the group
try:
    #Create a task group
    async with asyncio.TaskGroup() as group:
        # Create and issue a task
        task1 = group.create_task(coro1())
        
        # Create and issue a task
        task2 = group.create_task(coro2())
        
        # Create and issue a task
        task3 = group.create_task(coro3())
    # wait for all group tasks are done
except:
    # all none-done tasks are cancelled
    pass

#%%
# =============================================================================
# Example of waiting on multiple tasks

# Notice in the main that we don’t need to keep a reference to the asyncio.Task objects as the
# asyncio.TaskGroup will keep track of them for us.

# Also, notice that we don’t need to await the tasks because when we exit the context manager
# block for the asyncio.TaskGroup we will await all tasks in the group automatically.
# =============================================================================

async def task1():
    print("\tHello from coroutine 1")
    await asyncio.sleep(1)
    
async def task2():
    print("\tHello from coroutine 2")
    await asyncio.sleep(1)
    
async def task3():
    print("\tHello from coroutine 3")
    await asyncio.sleep(1)
    
async def main():
    # Create a task group
    async with asyncio.TaskGroup() as group:
        # run first task
        group.create_task(task1())
        
        # run second task
        group.create_task(task2())
        
        #run third task
        group.create_task(task3())
    
    # Wait for all tasks to complete
    print("Done")
    
asyncio.run(main())

#%%
# =============================================================================
# Example of cancelling all tasks if a task fails
# =============================================================================

async def task1():
    print("\tHello from coroutine 1")
    await asyncio.sleep(1)
    
async def task2():
    print("\tHello from coroutine 2")
    await asyncio.sleep(0.5)
    
    raise Exception("Something bad happened")
    
async def task3():
    print("\tHello from coroutine 3")
    await asyncio.sleep(1)
    
async def main():
    # Handle the exceptions
    try:
        # Create a task group
        async with asyncio.TaskGroup() as group:
            # run first task
            t1 = group.create_task(task1())
            
            # run second task
            t2 = group.create_task(task2())
            
            #run third task
            t3 = group.create_task(task3())
    except:
        pass
    
    # Check the status of each task
    print(f"T1: done={t1.done()}, cancelled={t1.cancelled()}")
    print(f"T2: done={t2.done()}, cancelled={t2.cancelled()}")
    print(f"T3: done={t3.done()}, cancelled={t3.cancelled()}")
    
asyncio.run(main())