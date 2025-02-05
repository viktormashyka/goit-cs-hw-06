import asyncio
import websockets
import json

async def handler(websocket): # add path as second argument if needed
    async for message in websocket:
        data = json.loads(message)
        print(f"Received data: {data}")
        # Process the data as needed
        response = {"status": "success", "data": data}
        await websocket.send(json.dumps(response))

async def main():
    async with websockets.serve(handler, "localhost", 8080):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
