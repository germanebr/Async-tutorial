# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 15:30:42 2024
@author: GReyes15

AsyncIO Mastery Ebook - Chapter 26
"""

import asyncio

from random import random

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# Asynchronous Queues

# A queue is a helpful data structure where items can be added and removed.
# Queues are generally used in concurrent programs to connect tasks, such as between threads
# and between processes.

# Asyncio also provides a queue, specifically tailored to share data between coroutines and
# tasks where blocking operations such as placing items on the queue and removing them can
# be awaited, spending the caller.

# Asynchronous queues are of FIFO type
# =============================================================================

# In general, queues have no size limit
queue = asyncio.Queue()

# You can specify a size limit
queue = asyncio.Queue(maxsize = 100)

# You can get the size of the queue as well
print(queue.maxsize)

# You can also check if the queue is empty or not. The method will get a boolean response
empty = queue.empty()

# Same thing to check if it's empty
full = queue.full()

# Adding items on the queue is a coroutine function that MUST be awaited
await queue.put(item)

# You can use put_nowait without blocking the event loop. Needs to handle the exception of the queue being full
try:
    # Attempt to add an item
    queue.put_nowait(item)
except asyncio.QueueFull:
    # ...
    pass

# Items can be retrieved by calling the get() method.
# It will be the oldest item since its FIFO. Needs to handle an empty queue exception
item = await queue.get()

# You can also call without blocking with get_nowait()
# Needs to handle the empty queue exception
try:
    item = queue.get_nowait()
except asyncio.QueueEmpty:
    pass

# =============================================================================
# Other coroutines may be interested to know when all items added to the queue have been
# retrieved and marked as done.
# This can be achieved by the coroutine awaiting the join() coroutine on the queue.
# The join() coroutine will not return until all items added to the queue prior to the call have
# been marked as done.
# =============================================================================

# wait for all items on the queue to be marked as done
await queue.join()

#%%
# =============================================================================
# Example of asyncio queue blocking the loop
# =============================================================================

# Coroutine to generate work
async def producer(queue):
    print("Producer: running")
    
    # Generate work
    for i in range(10):
        value = random()
        await asyncio.sleep(value)
        # Add to the queue
        await queue.put(value)
        
    # Send an all done signal
    await queue.put(None)
    print("Producer: Done")
    
# Coroutine to consume work
async def consumer(queue):
    print("Consumer: running")
    
    # Consume work
    while True:
        # Get a unit of work
        item = await queue.get()
        print(f"\t>Consumer with {item}")
        
        # Check for stop signal
        if item is None:
            break
        
        print(f"\t>Got {item}")
        
    # All done
    print("Consumer: Done")
    
# Entry point coroutine
async def main():
    # Create the shared queue
    queue = asyncio.Queue()
    
    # Run the producer and consumers
    await asyncio.gather(producer(queue),
                         consumer(queue))
    
asyncio.run(main())

#%%
# =============================================================================
# Example of queue without blocking

# We can get values from the asyncio.Queue without blocking.
# This might be useful if we wish to use busy waiting in the consumer coroutine to check other
# state or perform other tasks while waiting for data to arrive on the queue.
# =============================================================================

async def producer(queue):
    print("Producer: running")
    
    # Generate work
    for i in range(10):
        value = random()
        await asyncio.sleep(value)
        # Add to the queue
        await queue.put(value)
        
    # Send an all done signal
    await queue.put(None)
    print("Producer: Done")

async def consumer(queue):
    print("Consumer running")
    
    while True:
        try:
            item = queue.get_nowait()
        except asyncio.QueueEmpty:
            print("\t>Consumer: got nothing... waiting")
            await asyncio.sleep(0.5)
            continue
        
        # Check for stop
        if item is None:
            break
        
        print(f"\t>Got {item}")
    
    print("Consumer done")
    
async def main():
    # Create the shared queue
    queue = asyncio.Queue()
    
    # Run the producer and consumer
    await asyncio.gather(producer(queue),
                         consumer(queue))
    
asyncio.run(main())

#%%
# =============================================================================
# Example of asyncio queue join and task done

# In the previous examples, we have sent a special message (None) into the queue to indicate
# that all tasks are done.
# An alternative approach is to have coroutines wait on the queue directly and to have the
# consumer coroutine mark tasks as done.

# This can be achieved via the join() and task_done() functions on the asyncio.Queue.
# The producer coroutine can be updated to no longer send a None value into the queue to
# indicate no further tasks.
# =============================================================================

async def producer(queue):
    print("Producer running")
    
    # Generate work
    for i in range(10):
        value = random()
        await asyncio.sleep(value)
        
        # Add to the queue
        await queue.put(value)
        
    print("Producer done")
    
async def consumer(queue):
    print("Consumer running")
    
    while True:
        item = await queue.get()
        print(f"\t>Got {item}")
        
        # Block while processing
        if item:
            await asyncio.sleep(item)
        
        # Mark the task as done
        queue.task_done()
        
async def main():
    # Create a shared queue
    queue = asyncio.Queue()
    
    # Start the consumer
    _ = asyncio.create_task(consumer(queue))
    
    # Start the producer and wait for it to finish
    await asyncio.create_task(producer(queue))
    
    # Wait for all items to be processed
    await queue.join()
    
asyncio.run(main())