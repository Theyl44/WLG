import asyncio

import websockets
from generator import Generator
import sys
import os

clients = set()
generatorWords = Generator()


async def clientHandler(websocket, path):
    clients.add(websocket)
    try:
        async for message in websocket:
            print("[SERVER] Message receive : " + message)
            action = message.split(":")[0]
            print("action : " + action)
            if action == "generate":
                generate(message)
            elif action == "resultGeneration":
                resultGeneration()

    finally:
        clients.remove(websocket)


def generate(message):
    words = message.split(":")[1].split(";")

    temporaryList = "file.txt"
    if os.path.exists(temporaryList):
        os.remove(temporaryList)

    generateList = "result.txt"
    if os.path.exists(generateList):
        os.remove(generateList)

    generatorWords.write_file(file_path=temporaryList, word_list=words)
    generatorWords.steps()
    words = generatorWords.open_file(file_path=generateList)
    for word in words:
        print("word : " + word)
        if clients:
            await asyncio.wait([client.send(word) for client in clients])
    print("Generation finish")
    if clients:
        await asyncio.wait([client.send("end:blabla") for client in clients])


def resultGeneration():
    print("Want the result file")
    if os.path.exists("result.txt"):
        if clients:
            await asyncio.wait([client.send("/s:") for client in clients])

        print("File downloading")
        nameFile = "result.txt"

        if clients:
            await asyncio.wait([client.send("/q:") for client in clients])


start_server = websockets.serve(clientHandler, "localhost", 9000)
print("Server is running")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
