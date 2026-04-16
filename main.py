import asyncio
import websockets

clients = set()

async def handler(websocket):
    clients.add(websocket)
    print("Client connected")

    try:
        async for message in websocket:
            # пересылаем всем
            for client in clients:
                if client != websocket:
                    await client.send(message)
    except:
        pass
    finally:
        clients.remove(websocket)
        print("Client disconnected")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 10000):
        print("Server started")
        await asyncio.Future()  # run forever

asyncio.run(main())
