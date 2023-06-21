import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message

import json

from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'chat'
        self.room_group_name = "testroom"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    @database_sync_to_async
    def create_message(self, message, username):
        message_obj = Message.objects.create(
            content=message,
            username=username,
        )
        return message_obj

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Create a new message object and save it to the database
        message_obj = await self.create_message(message, 'testuser')
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": 'callback', "message": message_obj.content

            },
        )

    async def callback(self, event):
        await self.send(text_data=json.dumps(event["message"]))
