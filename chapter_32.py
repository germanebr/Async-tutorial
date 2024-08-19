# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 13:23:26 2024

AsyncIO Mastery Ebook - Chapter 32
"""

import asyncio
import signal

# This allows to run asyncio on an IDE and prevent RuntimeError
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# Subprocesses

# Asyncio provides a way to run commands in subprocesses and to read and write from the
# subprocesses without blocking. This can be helpful when porting Python programs that run
# local commands as subprocesses to asyncio and in developing new programs that are required
# to interact with separate programs.

# You can create a subprocess directly by using the create_subprocess_exec() function
# This function creates a coroutine and must be awaited

# The example below executes the echo command in a subprocess that prints out the provided
# string.
# The subprocess is started, then the details of the subprocess are then reported.

# The echo command is not available on all platforms (generates NotImplementedError).
# When run in a cmd, it first specifies the process number and then the hello world message
# subprocess: <Process 51822>
# Hello World
# =============================================================================

async def main():
    # Create a subprocess
    process = await asyncio.create_subprocess_exec('echo', 'Hello world')
    
    # Report the details of the subprocess
    print(f"Subprocess: {process}")
    
asyncio.run(main())

#%%
# =============================================================================
# A subprocess can also be awaited. The caller will be suspended until the subprocess
# is terminated, normally or otherwise.

# The following example we execute the sleep command and sleep for three seconds.
# The caller will then wait for the subprocess to complete before resuming.
# =============================================================================

async def main():
    # Create as a subprocess
    process = await asyncio.create_subprocess_shell('sleep 3')
    
    # Wait for the subprocess to terminate
    await process.wait()
    
asyncio.run(main())

#%%
# =============================================================================
# Write data to a subprocess

# Writing data to the subprocess via the communicate() method requires that the stdin
# argument in the create_subprocess_shell() or create_subprocess_exec() functions
# were set to PIPE.

# We can explore how to write data to a subprocess in asyncio.
# In the example below we will run the cat command that outputs the data provided to it.
# When called without an argument it will echo data from stdin.
# =============================================================================

async def main():
     # Create a subprocess
     process = await asyncio.create_subprocess_exec('cat', stdin = asyncio.subprocess.PIPE)
     
     # Write data to the subprocess
     _ = await process.communicate(b"Hello world\n")
     
asyncio.run(main())

#%%
# =============================================================================
# Read data from a subprocess

# Reading data from the subprocess requires that the stdout or stderr arguments of the
# create_subprocess_shell() or create_subprocess_exec() functions was set to PIPE.
# No argument is provided and the method returns a tuple with input from stdout and stderr.
# Data is read until an end of file (EOF) character is received.
# =============================================================================

async def main():
    # Create a subprocess
    process = await asyncio.create_subprocess_shell('echo Hello World',
                                                    stdout = asyncio.subprocess.PIPE)
    
    # Read data from the subprocess
    data, _ = await process.communicate()
    
    # Report the data
    print(data)
    
asyncio.run(main())

#%%
# =============================================================================
# How to stop subprocesses

# Sometimes we need to forcefully terminating the subprocess or even kill it.
# Some ways we can stop a subprocess include:
# 1. Sending a signal to the subprocess.
# 2. Terminating the subprocess.
# 3. Killing the subprocess.

# Once stopped, terminated or otherwise, we can then retrieve the return code and check if the
# subprocess completed normally or with an error.

# We can send a signal to the subprocess via the send_signal() method.
# The method takes a specific signal type, such as SIGINT to interrupt the subprocess or
# SIGKILL to kill the subprocess.
# =============================================================================
async def main():
    # Create the subprocess
    process = await asyncio.create_subprocess_shell('sleep 3')
    
    # Wait a moment
    await asyncio.sleep(1)
    
    # Send a signal to the process
    process.send_signal(signal.SIGKILL)
    
asyncio.run(main())

#%%
# =============================================================================
# We can terminate a subprocess as well
# =============================================================================
async def main():
    # Create the subprocess
    process = await asyncio.create_subprocess_shell('sleep 3')
    
    # Wait a moment
    await asyncio.sleep(1)
    
    # Terminate the subprocess
    process.terminate()
    
asyncio.run(main())

#%%
# =============================================================================
# Kill a subprocess

# On most platforms, this will send the SIGKILL signal to the subprocess in order to stop it
# immediately.
# Unlike the terminate() method that sends the SIGTERM signal, the SIGKILL signal cannot
# be handled by the subprocess. This means it is assured to stop the subprocess.
# =============================================================================
async def main():
    # Create a subprocess
    process = await asyncio.create_subprocess_shell('sleep 3')
    
    # Wait a moment
    await asyncio.sleep(1)
    
    # Kill the subprocess
    process.kill()
    
asyncio.run(main())

#%%
# =============================================================================
# Get a subprocess return code

# The return code is only available after the process has terminated, otherwise, the value is
# None.
# A return code of zero (0) indicates a successful exit. Any other value indicates an unsuccessful
# exit.
# =============================================================================
async def main():
    # Create the subprocess
    process = await asyncio.create_subprocess_shell('sleep 1')
    
    # Wait for the process to finish
    await process.wait()
    
    # Get the return code from the process
    print(process.returncode)
    
asyncio.run(main())