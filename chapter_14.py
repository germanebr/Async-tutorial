# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 12:51:37 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 14
"""

import asyncio

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# Running multiple tasks

# the command asyncio.gather() takes one or more coroutines or tasks, waits
# until they are all done, and returns an iterable of return values
# =============================================================================

# You can use the command to run multiple coroutines or tasks
asyncio.gather(coro1(), task1(), coro2())

# If you have the awaitables (tasks and coroutines) in a list, you need to unpack the list with *
awaitables = [coro1(), coro2(), task1()]

asyncio.gather(*awaitables)

# You can use a return_exceptions() with gather to catch any possible exception and prevent sending them to the main loop
results = await asyncio.gather(coro1(), coro2(),
                               return_exceptions = True)

#%%
# =============================================================================
# Example of gather with a list of coroutines

# It is common to create multiple coroutines beforehand and then gather them later.
# This allows a program to prepare the tasks that are to be executed concurrently and then
# trigger their concurrent execution all at once and wait for them to complete.
# =============================================================================

async def task_coro(value):
    print(f"\t>Task {value} executing...")
    
    await asyncio.sleep(1)
    
async def main():
    print("Main starting")
    
    # Create a list of coroutines
    coros = [task_coro(i) for i in range(10)]
    
    # Execute and wait for all tasks to be done
    await asyncio.gather(*coros)
    
    print("Main done")
    
asyncio.run(main())

#%%
# =============================================================================
# Example of gather with return values
# =============================================================================

async def task_coro(value):
    print(f"\t>Task {value} executing...")
    
    await asyncio.sleep(1)
    
    return value * 10
    
async def main():
    print("Main starting")
    
    # Create a list of coroutines
    tasks = [asyncio.create_task(task_coro(i)) for i in range(10)]
    
    # run the tasks
    values = await asyncio.gather(*tasks)
    print(values)
    
    print("Main done")
    
asyncio.run(main())

#%%
# =============================================================================
# Example of gather with returned exceptions
# =============================================================================

async def task_coro(value):
    print(f"\t>Task {value} executing...")
    
    await asyncio.sleep(1)
    
    if value == 0:
        raise Exception("Something bad happened")
    
    return value * 10
    
async def main():
    print("Main starting")
    
    # Create a list of coroutines
    tasks = [asyncio.create_task(task_coro(i)) for i in range(10)]
    
    # run the tasks
    values = await asyncio.gather(*tasks,
                                  return_exceptions = True)
    print(values)
    
    print("Main done")
    
asyncio.run(main())