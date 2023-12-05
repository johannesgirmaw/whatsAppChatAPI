import asyncio
import websockets
import json

async def room_chatroom():
    uri = "ws://localhost:8000/ws/text_chat/" + "1/"
    print(uri)
    async with websockets.connect(uri) as websocket:
        print(websocket)
        await websocket.send(json.dumps({
            'type': 'join',
        }))
        
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            if data['type'] == 'message':
                print(f"{data['username']}: {data['message']}")

            elif data['type'] == 'error':
                print(f"Error: {data['message']}")

# Run the event loop to execute the WebSocket communication
asyncio.get_event_loop().run_until_complete(room_chatroom())
