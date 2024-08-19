# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 13:49:30 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 22
"""

import asyncio
import time
import math

from concurrent.futures import ProcessPoolExecutor

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# Blocking tasks

# Calling regular functions and methods in asyncio programs will block the asyncio event loop.
# Luckily asyncio provides ways to execute blocking function calls in a way that simulates an
# asynchronous call that can be awaited, allowing other asyncio tasks to run and make progress.

# The solution is to run blocking function calls in a separate thread or process.

# There are two ways of running a blocking task in asyncio:
#     asyncio.to_thread()
#     loop.run_in_executor()
# =============================================================================

# =============================================================================
# Run task in thread

# asyncio.to_thread() will execute a target function in a thread separate from the thread that is
# executing the asyncio event loop.

# The to_thread() function takes the name of a blocking function to execute and any arguments
# to the function. It then returns a coroutine that can be awaited to get the return value from
# the function, if any.

# The blocking function will not be executed in a new thread until it is awaited or executed indirectly

# is specifically designed to execute blocking I/O functions,
# not CPU-bound functions that might also block the asyncio event loop.
# =============================================================================

# Create a coroutine for a blocking function
blocking_coro = asyncio.to_thread(blocking,
                                  arg1,
                                  arg2)

result = await blocking_coro

#%%
# =============================================================================
# Run task in executor

# Instead, we can use the run_in_executor() method on the event loop.
# This is part of the low-level asyncio API and first requires access to the event loop, such as
# via the asyncio.get_running_loop() function.

# The loop.run_in_executor() function takes an executor and a function to execute.
# If None is provided for the executor, then the default executor is used, which is a thread pool
# provided by the ThreadPoolExecutor class.

# The loop.run_in_executor() function returns an awaitable that can be awaited directly.
# The task will begin executing immediately, so the returned awaitable does not need to be
# awaited or scheduled for the blocking call to start executing.

# For CPU-bound tasks we must create and supply a process pool via an instance of the
# ProcessPoolExecutor class.
# =============================================================================

# Create a process pool
with ProcessPoolExecutor() as exe:
    # Get the event loop
    loop = asyncio.get_running_loop()
    
    # Execute a function in a separate thread
    await loop.run_in_executor(exe, task)
# Process pool is shutdown automatically

#%%
# =============================================================================
# Example of blocking the asyncio event loop

# This first example runns the blocking function directly in the asyncio event loop
# Regular functions block all the asyncio event loop and its corresponding tasks
# =============================================================================

def blocking_task():
    print("\tTask is running...")
    
    # Block the event loop
    time.sleep(2)
    
    print("\tTask is done")
    
async def background():
    i = 0
    while i < 15:
        print("\t>Background task running")
        
        await asyncio.sleep(0.5)
        
        i += 1
        
async def main():
    # Run the background task
    _ = asyncio.create_task(background())
    
    # Execute the blocking call
    blocking_task()
    
asyncio.run(main())

#%%
# =============================================================================
# Example of running a function in a thread

# The first example prevents any other coroutines from running while the blocking call is blocked
# and waiting. This example allows other coroutines to run while the blocking call is blocked
# and waiting, as seen in the program output.
# =============================================================================

def blocking_task():
    print("\tTask is running")
    
    # Block event loop
    time.sleep(2)
    
    print("\tTask is done!")
    
async def background():
    i = 0
    while i < 15:
        print("\t>Background task running")
        
        await asyncio.sleep(0.5)
        
        i += 1
        
async def main():
    # Run the background task
    _ = asyncio.create_task(background())
    
    # Create a coroutine for the blocking function call
    coro = asyncio.to_thread(blocking_task)
    
    # Execute the call in a new thread and await
    await coro
    
asyncio.run(main())

#%%
# =============================================================================
# Example of running a function in a process

# This example only works executing directly on Anaconda cmd (comment rest of examples)
# =============================================================================

# Create a CPU-bound task
def blocking_task():
    print("Task starting", flush = True)
    
    # Block for a while
    data = [math.sqrt(i) for i in range(50000000)]
    
    print("Task done!", flush = True)
    
async def main():
    print("Main running the blocking task")
    
    # Get the event loop
    loop = asyncio.get_running_loop()
    
    # Create the executor with 4 worker child processes
    exe = ProcessPoolExecutor(4)
    
    # Schedule the function to run
    awaitable = loop.run_in_executor(exe, blocking_task)
    
    print("Main doing other things")
    
    await asyncio.sleep(1)
    
    # Await the CPU-bound task
    await awaitable
    
    # Close the process pool
    exe.shutdown()
    
# Protect the entry point
if __name__ == '__main__':
    asyncio.run(main())