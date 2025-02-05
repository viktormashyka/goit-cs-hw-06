import asyncio
import json
import logging
from aiohttp import web
import websockets
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Configure logging
logging.basicConfig(level=logging.INFO)

# MongoDB connection
client = MongoClient(
    "mongodb+srv://vmashyka:0gdAJopgSfzuVUPW@cluster0.q0h5hq6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&tlsAllowInvalidCertificates=true",
    server_api=ServerApi('1')
)
db = client.test

async def handler(websocket): # add "path" as second argument if needed
    async for message in websocket:
        try:
            data = json.loads(message)
            result = db.messages.insert_one(data)
            stored_data = db.messages.find_one({"_id": result.inserted_id})
            if stored_data:
                logging.info(f"Data stored in MongoDB: {stored_data}")
            else:
                logging.info("Data not found in MongoDB after insertion")

            # Convert ObjectId to string for JSON serialization
            stored_data['_id'] = str(stored_data['_id'])

            # Write data to data.json
            with open('/app/data.json', 'w') as f:
                json.dump(stored_data, f)

        except Exception as e:
            logging.error(f"Error processing message: {e}")
            stored_data = {"status": "error", "message": str(e)}

        # Process the data as needed
        response = {"status": "success", "data": stored_data}
        await websocket.send(json.dumps(response))

async def websocket_server():
    logging.info("Starting WebSocket server on port 5000")
    async with websockets.serve(handler, "0.0.0.0", 5000):
        await asyncio.Future()  # run forever

async def http_handler(request):
    return web.Response(text="Hello, this is the HTTP server!")

async def serve_static(request):
    return web.FileResponse('./message.html')

async def init_http_server():
    logging.info("Starting HTTP server on port 3000")
    app = web.Application()
    app.router.add_get('/', http_handler)
    app.router.add_get('/message.html', serve_static)
    app.router.add_static('/static', './')
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 3000)
    await site.start()

async def main():
    await asyncio.gather(
        websocket_server(),
        init_http_server()
    )

if __name__ == "__main__":
    logging.info("Starting servers...")
    asyncio.run(main())