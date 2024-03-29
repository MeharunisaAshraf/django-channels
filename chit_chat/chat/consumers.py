from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


class ChatConsumer(WebsocketConsumer):
    room_group_name = None
    user = None

    def connect(self):
        self.user = self.scope['user'].username
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_username = text_data_json.get('username')

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_username': sender_username
            }
        )

    def chat_message(self, event):
        message = event['message']
        sender_username = event['sender_username']

        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'username': self.user if self.user != sender_username else None,  # Send sender's username if it's not the current user
            'sender_username': sender_username  # Include sender's username in the message
        }))
