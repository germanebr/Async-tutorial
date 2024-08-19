# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 14:23:51 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 3
"""

import asyncio

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# A coroutine is a function that can be stopped and re executed at a given time

# The await expression schedules a coroutine inside another coroutine to run, and suspends the current coroutine.
# In this example, the await expression schedules (runs) the coroutine of sleep, stopping the coroutine main until the sleep ends.
# =============================================================================

# Define the coroutine
async def main():
    # Await another coroutine
    await asyncio.sleep(1)
    
# =============================================================================
# We can execute a coroutine within a synchronous function using the .run() function
# =============================================================================

asyncio.run(main())