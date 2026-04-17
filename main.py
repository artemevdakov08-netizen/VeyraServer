import asyncio
import websockets
import json
import os

rooms = {}

async def handler(websocket):
    print("CLIENT CONNECTED")

    try:
        async for message in websocket:
            data = json.loads(message)

            room = data.get("room")

            if room not in rooms:
                rooms[room] = set()

            rooms[room].add(websocket)

            for client in list(rooms[room]):
                try:
                    await client.send(json.dumps(data))
                except:
                    rooms[room].discard(client)

    except:
        print("CLIENT DISCONNECTED")


async def main():
    port = int(os.environ["PORT"])  # 💥 ТОЛЬКО ТАК

    print("SERVER STARTED ON", port)

    server = await websockets.serve(handler, "0.0.0.0", port)

    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main())
