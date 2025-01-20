from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from core.models import Messages
from asgiref.sync import sync_to_async
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Check if the user is authenticated (this is non-blocking)
        if not self.scope['user'].is_authenticated:
            print("User is not authenticated.")
            await self.close()
            return

        # Room name for the receiver
        self.room_name = self.scope['url_route']['kwargs']['receiver']
        
        # Sorted user names to determine group name (no async operation needed)
        user1 = self.scope['user'].username
        user2 = self.room_name
        self.sort_user = ''.join(sorted([user1, user2]))

        # Add the user to the group (this is an async operation)
        await self.channel_layer.group_add(self.sort_user, self.channel_name)

        # Accept the WebSocket connection
        print(f"User connected to room: {self.sort_user}")
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.sort_user, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        message = text_data['message']
        sender = self.scope['user']
        
        
        try:
            receiver = await sync_to_async(User.objects.get)(username=self.room_name)
        except User.DoesNotExist:
            await self.close()
            return

        
        await sync_to_async(Messages.objects.create)(
            sender=sender,
            receiver=receiver,
            content=message
        )

        # Send the message to the group asynchronously
        await self.channel_layer.group_send(
            self.sort_user, {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username,
                'receiver': receiver.username
            }
        )

    async def chat_message(self, event):
        print(event)
        message = event['message']
        sender = event['sender']
        receiver = event['receiver']
        

        
        await self.send(text_data=json.dumps({
            'sender': sender,
            'receiver': receiver,
            'message': message
        }))
