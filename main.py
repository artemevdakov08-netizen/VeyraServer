import asyncio
import websockets
import json
import os

rooms = {}

async def handler(websocket):
    print("🔥 CLIENT CONNECTED")

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
                    rooms[room].remove(client)

    except:
        print("CLIENT DISCONNECTED")


# 💥 ВОТ ЭТО ДОБАВЛЯЕМ
async def process_request(path, request_headers):
    return (200, [], b"OK")


async def main():
    port = int(os.environ.get("PORT", 10000))

    print("SERVER STARTED ON", port)

    async with websockets.serve(
        handler,
        "0.0.0.0",
        port,
        process_request=process_request  # 💥 ВАЖНО
    ):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
