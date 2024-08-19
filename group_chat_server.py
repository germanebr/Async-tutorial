# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 13:51:45 2024

@author: GReyes15

Asyncio Mastery Book - Group Chat Client and Server
Chat server code
"""

import asyncio

#%%
# =============================================================================
# Broadcast to all clients

# Coroutine that sends concurrently a message to all connected clients on the group chat
# =============================================================================

async def broadcast_message(message):
    # Report locally
    print(f"Broadcast: {message.strip()}")
    
    # Parse the message into bytes
    msg_bytes = message.encode()
    
    # Enumerate all users and broadcast the message
    global ALL_USERS
    
    # Concurrent approach
    # Create a task for each write to client
    tasks = [asyncio.create_task(write_message(writer, msg_bytes))
             for _, (_, writer) in ALL_USERS.items()]
    
    # Wait for all writes to complete
    _ = await asyncio.wait(tasks)
    
    # Sequential approach (slower)
    # for _, (_, writer) in ALL_USERS.items():
    #     # Write the message to the selected user
    #     writer.write(msg_bytes)
        
    #     # Wait for the buffer to be empty
    #     await writer.drain()
    
#%%
# =============================================================================
# Coroutine to transmit a message concurrently to all users
# =============================================================================

async def write_message(writer, msg_bytes):
    # Write the message to the user
    writer.write(msg_bytes)
    
    # Wait for the buffer to empty
    await writer.drain()
    
#%%
# =============================================================================
# Connect a new client

# Send a welcome message to a new user and ask for their name
# =============================================================================

async def connect_user(reader, writer):
    # Get name message
    writer.write('Asyncio Chat Server\n'.encode())
    writer.write('Enter your name:\n'.encode())
    await writer.drain()
    
    # Ask the user for their name
    name_bytes = await reader.readline()
    
    # Convert name to string
    name = name_bytes.decode().strip()
    
    # Store the user details
    global ALL_USERS
    ALL_USERS[name] = (reader, writer)
    
    # Announce the user
    await broadcast_message(f"{name} has connected!\n")
    
    # Give the welcome message
    welcome = f"Welcome {name}. Send QUIT to disconnect.\n"
    writer.write(welcome.encode())
    await writer.drain()
    
    return name

#%%
# =============================================================================
# Disconnect a client

# Disconnect a client when requested
# =============================================================================

async def disconnect_user(name, writer):
    # Close the user's connection
    writer.close()
    await writer.wait_closed()
    
    # Remove from the dict of all users
    global ALL_USERS
    del ALL_USERS[name]
    
    # Broadcast the user has left
    await broadcast_message(f"{name} has left the room\n")
    
#%%
# =============================================================================
# Manage a client

# Coroutine for managing all the previous actions for a single user
# =============================================================================

async def handle_chat_client(reader, writer):
    print("Client connecting...")
    
    # Connect the user
    name = await connect_user(reader, writer)
    try:
        # Read messages from the user
        while True:
            # Read a line of data
            line_bytes = await reader.readline()
            
            # Convert to string
            line = line_bytes.decode().strip()
            
            # Check for exit
            if line == "QUIT":
                break
            
            # Broadcast a message
            await broadcast_message(f"{name}: {line}\n")
    
    finally:
        # Disconnect the user
        await disconnect_user(name, writer)
        
#%%
# =============================================================================
# Drive the server

# Coroutine for creating the main server
# =============================================================================

async def main():
     # Define the local host
     host_address, host_port = '127.0.0.1', 8887
     
     # Create the asyncio server
     server = await asyncio.start_server(handle_chat_client,
                                         host_address,
                                         host_port)
     
     # Run the server
     async with server:
         # Report a message
         print("Chat Server Running\nWaiting for chat clients...")
         
         # Accept connections
         await server.serve_forever()
         
#%%
# =============================================================================
# Start the event loop
# =============================================================================

# Define the dictionary for all the users
ALL_USERS = {}

# Start the event loop
asyncio.run(main())