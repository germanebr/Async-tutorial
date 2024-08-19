# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 15:01:13 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 24
"""

import asyncio

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# Asynchronous generators

# A generator is a Python function that returns a value via a yield expression
# for producing a series of values # usable in a for-loop or that can be
# retrieved one at a time with the next() function.

# The following example creates an asynchronous generator and steps it one time
# =============================================================================

# Define an ashynchronous generator
async def async_generator():
    # Normal loop
    for i in range(10):
        # Block to simulate doing work
        await asyncio.sleep(1)
        
        # Yield the result
        yield i
        
async def main():
    # Create the async generator
    gen = async_generator()
    
    # Step the generator one iteration
    print("Checking only first iteration:")
    awaitable = anext(gen)
    # Get the result from one iteration
    result = await awaitable
    print(result)
    
    # Loop over async generator with an async for loop
    print("\nUsing async for loop:")
    async for item in async_generator():
        print(item)
        
    # Use list comprehension
    print("\nUsing list comprehension:")
    results = [item async for item in async_generator()]
    print(results)
    
asyncio.run(main())