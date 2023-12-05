
    # chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from .entitys import Chatroom

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["id"]
        # room_name = Chatroom.objects.get(pk=self.room_name)
        print(self.scope.get("headers", {}))
            # Find the Authorization header and extract the token
        authorization_header = next((header for header in self.scope.get("headers", {}) if header[0].lower() == b'authorization'), None)
        if authorization_header:
            token = authorization_header[1].decode('utf-8').split('Token ')[1]
            print("Authorization Token:", token)
        else:
            print("Authorization header not found")

        user = await get_user_from_token(self, token)

        self.room_group_name = "chat_%s" % self.room_name
        print("-----------------------------------", user, self.room_group_name)
        
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        print("===========Messages:", text_data)
        if text_data:
            if isinstance(text_data, str):
                message = text_data
            else:
                text_data_json = json.loads(text_data)
                message = text_data_json["message"]

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat_message", "message": message}
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        print("===========message:", message)
        await self.send(text_data=json.dumps({"message": message}))

from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token

@database_sync_to_async
def get_user_from_token(self, token):
    try:
        return Token.objects.get(key=token).user
    except Token.DoesNotExist:
        return None