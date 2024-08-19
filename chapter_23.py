# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 14:36:42 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 23
"""

import asyncio

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# Asynchronous iterators

# Iterators provide a way to traverse structures like lists of items in a linear way.
# The problem is that conventional iterators are not well suited to asyncio programs. The
# reason is that we cannot have each item in the iterator retrieved asynchronously.
# Instead, we can use asynchronous iterators along with the async for expression to automatically
# await the retrieval of the next item in the iteration.

# The following example shows how to create an asynchronous iterator and step it one time
# =============================================================================

# Create the asynchronous iterator
class AsyncIterator():
    # Constructor, define some state
    def __init__(self):
        self.counter = 0
        
    # Create an instance of the iterator
    def __aiter__(self):
        return self
    
    # Return the next awaitable
    async def __anext__(self):
        # Check for no further items
        if self.counter >= 10:
            raise StopAsyncIteration
        
        # Increment the counter
        self.counter += 1
        
        # Simulate work
        await asyncio.sleep(1)
        
        # Return the counter value
        return self.counter
    
# Main coroutine
async def main():
    # Create the async iterator
    it = AsyncIterator()
    
    # Step the iterator one iteration
    awaitable = anext(it)
    
    # Get the result from one iteration
    result = await awaitable
    print(result)
    
asyncio.run(main())

#%%
# =============================================================================
# Example of an async iterator with for loop

# In this example, we will update the previous example to traverse the iterator to completion
# using an async for loop.
# This loop will automatically await each awaitable returned from the iterator, retrieve the
# returned value, and make it available within the loop body so that in this case it can be
# reported.
# =============================================================================

# Create the asynchronous iterator
class AsyncIterator():
    # Constructor, define some state
    def __init__(self):
        self.counter = 0
        
    # Create an instance of the iterator
    def __aiter__(self):
        return self
    
    # Return the next awaitable
    async def __anext__(self):
        # Check for no further items
        if self.counter >= 10:
            raise StopAsyncIteration
        
        # Increment the counter
        self.counter += 1
        
        # Simulate work
        await asyncio.sleep(1)
        
        # Return the counter value
        return self.counter
    
async def main():
    # Loop over async iterator with async for loop
    async for item in AsyncIterator():
        print(item)
        
    # You can also use it with comprehension
    print("\nChecking now with list comprehension\n")
    results = [item async for item in AsyncIterator()]
    print(results)
        
asyncio.run(main())