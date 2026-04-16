import asyncio
import websockets
import json
import os

clients = set()
rooms = {}

async def handler(websocket):
    print("Client connected")
    try:
        async for message in websocket:
            data = json.loads(message)

            room = data.get("room")
            text = data.get("text")

            if not room:
                continue

            if room not in rooms:
                rooms[room] = set()

            rooms[room].add(websocket)

            payload = json.dumps({
                "room": room,
                "text": text
            })

            for client in list(rooms[room]):
                try:
                    await client.send(payload)
                except:
                    rooms[room].remove(client)

    except:
        pass
    finally:
        print("Client disconnected")
        for r in rooms:
            rooms[r].discard(websocket)

async def main():
    port = int(os.environ.get("PORT", 10000))

    print(f"Server starting on port {port}")

    async with websockets.serve(handler, "0.0.0.0", port):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
    async with websockets.serve(handler, "0.0.0.0", 10000):
        print("Server started")
        await asyncio.Future()  # run forever

asyncio.run(main())
