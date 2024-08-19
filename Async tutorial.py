# =============================================================================
# Tutorial followed from https://realpython.com/async-io-python/
# 
# A coroutine is a function that can suspend its execution before reaching return, and can indirectly pass control to another coroutine for some time.
# =============================================================================
import asyncio
import time
import random

#%%
# =============================================================================
# The async/await syntax and native coroutines
# A coroutine is a function that can suspend its execution before reaching return, and can indirectly pass control to another coroutine for some time.
# =============================================================================

async def count():
    print("One")
    await asyncio.sleep(1)
    print("Two")

async def main():
    await asyncio.gather(count(), count(), count())
    
if __name__ == "__main__":
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
    
#%%
def count():
    print("One")
    time.sleep(1)
    print("Two")

def main():
    for _ in range(3):
        count()
        
if __name__ == "__main__":
    s = time.perf_counter()
    main()
    elapsed = time.perf_counter() - s
    print(f"Synchronous code executed in {elapsed:0.2f} seconds.")