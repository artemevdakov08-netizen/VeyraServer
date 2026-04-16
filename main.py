import asyncio
import websockets

clients = set()

rooms = {}

async def handler(websocket):
    async for message in websocket:
        data = json.loads(message)

        room = data["room"]
        text = data["text"]

        if room not in rooms:
            rooms[room] = set()

        # добавляем клиента в комнату
        rooms[room].add(websocket)

        # пересылаем только в эту комнату
        for client in rooms[room]:
            await client.send(json.dumps(data))

async def main():
    async with websockets.serve(handler, "0.0.0.0", 10000):
        print("Server started")
        await asyncio.Future()  # run forever

asyncio.run(main())
