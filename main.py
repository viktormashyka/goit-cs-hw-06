import asyncio
import websockets
import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId

# MongoDB connection
client = MongoClient(
    "mongodb+srv://vmashyka:0gdAJopgSfzuVUPW@cluster0.q0h5hq6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&tlsAllowInvalidCertificates=true",
    server_api=ServerApi('1')
)
db = client.test

async def handler(websocket): # add path as second argument if needed
    async for message in websocket:
        try:
            data = json.loads(message)
            print(f"Received data: {data}")

            # Ensure data is a dictionary
            if not isinstance(data, dict):
                raise ValueError("Data is not a dictionary")

            # Store data in MongoDB
            print("Storing data in MongoDB")
            result = db.messages.insert_one(data)
            print(f"Data inserted with id: {result.inserted_id}")

            # Verify insertion
            stored_data = db.messages.find_one({"_id": result.inserted_id})
            if stored_data:
                print(f"Data stored in MongoDB: {stored_data}")
            else:
                print("Data not found in MongoDB after insertion")

            # Convert ObjectId to string for JSON serialization
            stored_data['_id'] = str(stored_data['_id'])

        except Exception as e:
            print(f"Error processing message: {e}")
            stored_data = {"status": "error", "message": str(e)}

        # Process the data as needed
        response = {"status": "success", "data": stored_data}
        await websocket.send(json.dumps(response))

async def main():
    async with websockets.serve(handler, "localhost", 8080):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
