# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 13:15:15 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 15
"""

import asyncio

from random import random

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# Wait on tasks on a specific condition

# It is better to use wait rather than gather() if WE DON'T REQUIRE THE RESULTS FROM TASKS
# Wait also supports other conditions that gather does not.
# =============================================================================

# Waiting for tasks give two sets: one for the cdone tasks, and another for the pending
done, pending = await asyncio.wait(tasks)

# You can also specify when to return the values. The default is when all tasks are done
done, pending = await asyncio.wait(tasks,
                                   return_when = asyncio.ALL_COMPLETED)

# You can return the values when the first task is completed
done, pending = await asyncio.wait(tasks,
                                   return_when = asyncio.FIRST_COMPLETED)

# You can return the values when the first task failed
done, pending = await asyncio.wait(tasks,
                                   return_when = asyncio.FIRST_EXCEPTION)

# We can specify a timeout for completing the tasks. If time runs out, returns everything that was completed by that time
done, pending = await asyncio.wait(tasks,
                                   timeout = 3)

#%%
# =============================================================================
# Example of waiting for all tasks
# =============================================================================

async def task_coro(arg):
    # Generate a random value between 0 and 1
    value = random()
    
    # Block for that random time
    await asyncio.sleep(value)
    
    print(f"\t>Task {arg} done with {value}")
    
async def main():
    # Create many tasks
    tasks = [asyncio.create_task(task_coro(i)) for i in range(10)]
    
    # Wait for all tasks to complete
    done, pending = await asyncio.wait(tasks)
    
    print("All done")
    
asyncio.run(main())

#%%
# =============================================================================
# Example of waiting for first task

# NOTE: this code finishes running the rest of tasks because of Spyder running everything.
# Code will cancel the rest of the tasks when running on a regular python script or cmd
# =============================================================================

async def task_coro(arg):
    # Generate a random value between 0 and 1
    value = random()
    
    # Block for that random time
    await asyncio.sleep(value)
    
    print(f"\t>Task {arg} done with {value}")
    
async def main():
    # Create many tasks
    tasks = [asyncio.create_task(task_coro(i)) for i in range(10)]
    
    # Wait for the first task to complete (the rest wil be in pending variable)
    done, pending = await asyncio.wait(tasks,
                                       return_when = asyncio.FIRST_COMPLETED)
    
    print("First done")
    
    # Ge the first task to coplete
    first = done.pop()
    print(first)
    
asyncio.run(main())

#%%
# =============================================================================
# Example of waiting for first task failure
# =============================================================================

async def task_coro(arg):
    # Generate a random value between 0 and 1
    value = random()
    
    # Block for that random time
    await asyncio.sleep(value)
    
    print(f"\t>Task {arg} done with {value}")
    
    # Conditionally fail
    if value < 0.5:
        raise Exception(f"Something bad happened in {arg}")
    
async def main():
    # Create many tasks
    tasks = [asyncio.create_task(task_coro(i)) for i in range(10)]
    
    # Wait for the first task to complete (the rest wil be in pending variable)
    done, pending = await asyncio.wait(tasks,
                                       return_when = asyncio.FIRST_EXCEPTION)
    
    print("First done")
    
    # Ge the first task to coplete
    first = done.pop()
    print(first)
    
asyncio.run(main())

#%%
# =============================================================================
# Example of waiting with a timeout
# =============================================================================

async def task_coro(arg):
    # Generate a random value between 0 and 1
    value = random() * 10
    
    # Block for that random time
    await asyncio.sleep(value)
    
    print(f"\t>Task {arg} done with {value}")
    
async def main():
    # Create many tasks
    tasks = [asyncio.create_task(task_coro(i)) for i in range(10)]
    
    # Wait for the first task to complete (the rest wil be in pending variable)
    done, pending = await asyncio.wait(tasks,
                                       timeout = 5)
    
    # Report results
    print(f"Done {len(done)} tasks in time")
    
asyncio.run(main())