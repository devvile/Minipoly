from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import Game
from player.models import Player

class GameEventsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        game_id = (self.scope['url_route']['kwargs']['id'])
        self.game = await database_sync_to_async(self.get_game)(id=game_id)
        self.room_group_name = self.game.name

        await (self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()


    def get_game(self,id):
        return Game.objects.get(pk=id)

    async def receive(self, text_data):
        """
        if text_data == "klik":
            self.counter.klik +=1
        elif text_data == "klak":
            self.counter.key += 1
            """
        message = json.loads(text_data)
        if message['action']=="ready":
            print("Bingo!")
        elif message['action']=="start":
            print("Starto!")
        await database_sync_to_async(self.game.save)()
        await (self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'game_message',
                'message': message,
            }
        )

    async def game_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message,
        }))

    async def disconnect(self, close_code):
        await (self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        await self.close()
