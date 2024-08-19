# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 15:12:32 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 25
"""

import asyncio

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# Asynchronous context managers

# Context managers are a helpful construct for automatically executing common code before
# and after a block.

# An asynchronous context manager is like a regular context manager, except it can be awaited
# on entry and exit.

# The following example is for a manual async context manager
# =============================================================================

# Define an asynchronous context manager
class AsyncContextManager():
    # enter the async context manager
    async def __aenter__(self):
        print(f"\t>Entering the context manager")
        
        await asyncio.sleep(0.5)
        
    # Exit the async context manager
    async def __aexit__(self, exc_type, exc, tb):
        print("\t>Exiting the context manager")
        await asyncio.sleep(0.5)
         
# Define a simple coroutine
async def custom_coroutine():
    # Create and use the asynchronous context manager
    manager = AsyncContextManager()
    
    # get the awaitable for entering the manager
    enter_awaitable = manager.__aenter__()
    
    # Await the entry
    await enter_awaitable
    
    # Execute the body
    print("Within the manager...")
    
    # Get the awaitable for exiting the manager
    exit_awaitable = manager.__aexit__(None, None, None)
    await exit_awaitable
    
asyncio.run(custom_coroutine())

#%%
# =============================================================================
# Example of an asynchronous context manager
# =============================================================================

# Define an asynchronous context manager
class AsyncContextManager():
    # enter the async context manager
    async def __aenter__(self):
        print(f"\t>Entering the context manager")
        await asyncio.sleep(0.5)
        
    # Exit the async context manager
    async def __aexit__(self, exc_type, exc, tb):
        print("\t>Exiting the context manager")
        await asyncio.sleep(0.5)
        
async def custom_coroutine():
    # Create and use the asynchronous context manager
    async with AsyncContextManager() as manager:
        print("Within the manager")
    
asyncio.run(custom_coroutine())

#%%
# =============================================================================
# Example of exception in async context manager

# This example highlights that the exit coroutine of an asynchronous context manager is awaited,
# regardless of how the inner block of the context manager is exited, such as with an unhandled
# exception.
# =============================================================================

# Define an asynchronous context manager
class AsyncContextManager():
    # enter the async context manager
    async def __aenter__(self):
        print(f"\t>Entering the context manager")
        await asyncio.sleep(0.5)
        
    # Exit the async context manager
    async def __aexit__(self, exc_type, exc, tb):
        print("\t>Exiting the context manager")
        await asyncio.sleep(0.5)
        
async def custom_coroutine():
    async with AsyncContextManager() as manager:
        print("Within the manager")
        
        # Fail with an exception
        raise Exception("Something bad happened!")
        
asyncio.run(custom_coroutine())