import asyncio
import websockets

clients = set()


async def clientHandler(websocket, path):
    clients.add(websocket)
    try:
        async for message in websocket:
            print("[SERVEUR] Message Reçu : " + message)
            if clients:
                await asyncio.wait([client.send(message) for client in clients])
    finally:
        clients.remove(websocket)
        if clients:
            await asyncio.wait([client.send("Un utilisateur a quitté le canal de discussion") for client in clients])


start_server = websockets.serve(clientHandler, "localhost", 12345)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
