from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import Game

class GameEventsConsumer(AsyncWebsocketConsumer):
   async def connect(self):
        self.room_group_name = 'main_room'
        self.counter = await database_sync_to_async(self.get_game)()

        await (self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()


   def get_game(self):
       return Game.objects.all()[0]

   async def receive(self, text_data):
        if text_data == "klik":
            self.counter.klik +=1
        elif text_data == "klak":
            self.counter.key += 1
        await database_sync_to_async(self.counter.save)()
        klik = self.counter.klik
        klak = self.counter.key
        await (self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'klik': klik,
                'klak': klak
            }
        )

   async def chat_message(self, event):
        message_klik = event['klik']
        message_klak = event['klak']
        await self.send(text_data=json.dumps({
            'klik': message_klik,
            'klak': message_klak
        }))

   async def disconnect(self, close_code):
        await (self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        await self.close()
