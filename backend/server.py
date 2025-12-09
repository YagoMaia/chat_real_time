import asyncio

from websockets.asyncio.server import ServerConnection, serve

from core.db import mongo_connection
from model import Message

CLIENTS : dict[str, ServerConnection] = {}

async def enter_chat(websocket: ServerConnection, user: str):
    """
    Function for client enter the chat.
    """
    CLIENTS[user] = websocket
    messages = await mongo_connection.get_all_no_delivered_messages(user)
    print(f"{user} enter the chat - Checking offline messages...")
    for msg in messages:
        await websocket.send(f"[{msg.user_from}]: {msg.message}")
        await mongo_connection.mark_message_as_delivered(msg.id)

async def handle(websocket: ServerConnection):
    """
    Function for handle websocket connections.
    """
    user = None
    try:
        # Websocket connect
        user = await websocket.recv()
        if not isinstance(user, str):
            return
        await enter_chat(websocket, user)

        # Websocket messages sent
        async for msg in websocket:
            if not isinstance(msg, str):
                continue
            user_to, message = msg.split(":", 1)
            if user_to in CLIENTS:
                socket_user_to = CLIENTS[user_to]
                message_db = Message(user_to=user_to, user_from = user, message = message, delivered=True)
                await mongo_connection.insert_message(message_db)
                await socket_user_to.send(f"[{user}]: {message}")
            else:
                message_db = Message(user_to=user_to, user_from = user, message = message, delivered=False)
                await mongo_connection.insert_message(message_db)
                # await websocket.send(f"[System]: {user_to} isn't online")
    except Exception as error:
        await websocket.send(f"[System]: ERROR with {user}: {str(error)}")
    finally:
        if isinstance(user, str):
            del CLIENTS[user]
            print(f"User {user} made logout")

async def main():
    """
    Main function to run server.
    """
    print("Running Server!")
    async with serve(handle, "localhost", 8765) as server:
        await server.serve_forever()

asyncio.run(main())
