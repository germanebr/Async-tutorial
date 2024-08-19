# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 14:54:42 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 4
"""

import asyncio

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# Hello world using asyncio
# =============================================================================

# Define the coroutine
async def main():
    # Report a message
    print("Hello world!")
    
# Start the asyncio event loop
asyncio.run(main())

# Call the coroutine directly
main() #Will generate a warning

#%%
# =============================================================================
# Since coroutines are objects, we can assign them to a variable

# We need to run them anyways, or we'll get the warning as above
# =============================================================================

coro = main()

# Execute the coroutine
asyncio.run(coro) #Commenting this will generate the warning again

#%%
# =============================================================================
# An awaitable is another coroutine object that runs the __await__() method

# We can suspend a coroutine and do nothing via the asyncio.sleep() function

# The await expression can only be used within a coroutine to execute and wait on an awaitable
# =============================================================================

async def main():
    # Sleep for a second (don't forget to await the action or you'll get another warning)
    await asyncio.sleep(1)
    
    # Report the message
    print("Hello world!")
    
asyncio.run(main())