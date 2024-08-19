# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 14:26:45 2024

@author: GReyes15
Asyncio Mastery Book - Group Chat Client and Server
Chat client code
"""

import asyncio
import sys

#%%
# =============================================================================
# Read and transmit user messages

# Coroutine that reads messages and transmits to the chat server
# =============================================================================

async def write_messages(writer):
    while True:
        # Read from the stdin
        message = await asyncio.to_thread(sys.stdin.readline)
        
        # Encode the string message to bytes
        msg_bytes = message.encode()
        
        # Transmit the message to the server
        writer.write(msg_bytes)
        
        # Wait for the buffer to be empty
        await writer.drain()
        
        # Check if the user wants to quit the chat
        if message.strip() == "QUIT":
            break
        
    # Report the program is being terminated
    print("Quitting...")
    
#%%
# =============================================================================
# Read and report server messages

# Coroutine that will read messages sent from the server and report them to the user
# =============================================================================

async def read_messages(reader):
    while True:
        # Read the message from the server
        result_bytes = await reader.readline()
        
        # Decode and report the response
        response = result_bytes.decode()
        print(response.strip())
        
#%%
# =============================================================================
# Drive connection with server

# Manage both user actions and connection with the server
# =============================================================================

async def main():
    # Define the server details
    host, port = '127.0.0.1', 8887
    
    # Report progress to the user
    print(f"Connecting to {host}:{port}...")
    
    # Open a connection to the server
    reader, writer = await asyncio.open_connection(host, port)
    
    # Report progress to the user
    print("Connected!")
    
    # Read and report messages from the server
    read_task = asyncio.create_task(read_messages(reader))
    
    # Write messages to the server
    await write_messages(writer)
    
    # Cancel the read messages task
    read_task.cancel()
    
    # Report progress to the user
    print("Disconnecting from the server...")
    
    # Close the stream writer
    writer.close()
    
    # Wait for the tcp connection to close
    await writer.wait_closed()
    
    # Report progress to the user
    print("Done.")
    
#%%
# Run the event loop
asyncio.run(main())