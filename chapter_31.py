# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 12:30:26 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 31
"""

import asyncio

from random import random

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# Barriers

# is used to coordinate the behavior of concurrent tasks at one point, on the barrier itself.
# Once all expected parties arrive at the barrier, the barrier is lifted and all waiting tasks are
# able to resume their activity.
# =============================================================================

# Create a barrirer
barrier = asyncio.Barrier()

# The wait method returns an integer indicating the number of parties remaining to arrive
position = await barrier.wait()

# Perform an action if last to leave the barrier
if position == 0:
    # do something
    
# Aborting a barrier will generate a BrokenBarrierError
await barrier.abort()

# Reset a broken (aborted) barrier
await barrier.reset()

#%%
# =============================================================================
# Example of using an asyncio barrier
# =============================================================================

async def work(barrier, number):
    value = random() * 10
    
    # Suspend for a moment to simulate work
    await asyncio.sleep(value)
    
    print(f"\t-> Task {number} done! Got {value}, and waiting.")
    
    # Wait on all other tasks complete
    await barrier.wait()
    
async def main():
    # Create a barrier (it's 0 inclusive)
    n_tasks = 5
    
    barrier = asyncio.Barrier(n_tasks + 1)
    
    # Issue all the tasks
    _ = [asyncio.create_task(work(barrier, i))
         for i in range(n_tasks)]
    
    # Wait for all tasks to finish
    print("Main is waiting on all results...")
    async with barrier:
        # Report once all tasks are done
        print("All tasks have their result!")
        
asyncio.run(main())