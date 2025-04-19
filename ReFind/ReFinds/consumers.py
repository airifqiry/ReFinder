import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat, Message
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if data.get("type") == "typing":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'show_typing',
                    'username': self.scope["user"].username,
                }
            )
        elif data.get("type") == "reaction":
            await self.update_reaction(data["message_id"], data["reaction"])
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'reaction_update',
                    'message_id': data["message_id"],
                    'reaction': data["reaction"]
                }
            )
        else:
            message = data['message']
            sender = self.scope["user"]
            image_url = data.get("image", "")

            msg_obj = await self.save_message(message, sender.id, image_url)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender.username,
                    'timestamp': msg_obj.timestamp.strftime("%H:%M %d.%m.%Y"),
                    'image': image_url,
                    'msg_id': msg_obj.id
                }
            )

    async def show_typing(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'username': event['username'],
        }))

    async def reaction_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'reaction',
            'message_id': event['message_id'],
            'reaction': event['reaction'],
        }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp'],
            'image': event['image'],
            'msg_id': event['msg_id'],
        }))

    @database_sync_to_async
    def save_message(self, text, sender_id, image_url):
        chat = Chat.objects.get(id=self.chat_id)
        sender = User.objects.get(id=sender_id)
        return Message.objects.create(chat=chat, sender=sender, text=text)

    @database_sync_to_async
    def update_reaction(self, message_id, reaction):
        msg = Message.objects.get(id=message_id)
        msg.reactions[reaction] = msg.reactions.get(reaction, 0) + 1
        msg.save()
