from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import Game
from player.models import Player

class GameEventsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        game_id = (self.scope['url_route']['kwargs']['id'])
        self.game = await self.get_game(id=game_id)
        self.room_group_name = self.game.name


        await (self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    @database_sync_to_async
    def get_game(self,id):
        return Game.objects.get(pk=id)

    @database_sync_to_async
    def get_player(self, usr):
        return Player.objects.get(nick=usr)

    @database_sync_to_async
    def get_game_is_played(self, game):
        return game.is_played

    @database_sync_to_async
    def get_player_in_game(self,player):
        return player.in_game

    @database_sync_to_async
    def get_how_many_players_ready(self,game):
        return game.how_many_players_ready

    @database_sync_to_async
    def get_players_ready(self, game):
        x = [i.nick for i in game.who_is_ready.all()]
        return x

    @database_sync_to_async
    def get_max_players(self, game):
        return game.max_players

    @database_sync_to_async
    def get_host(self, game):
        return game.host

    @database_sync_to_async
    def add_player_to_game(self, player, game):
        return game.who_is_ready.add(player)

    @database_sync_to_async
    def remove_player_from_game(self, player, game):
        return game.who_is_ready.remove(player)

    @database_sync_to_async
    def set_player_game_status_ready(self, player):
        player.set_player_in_game()

    @database_sync_to_async
    def set_player_game_status_off(self, player):
        player.set_player_leave_game()

    @database_sync_to_async
    def set_game_played(self, game):
        game.is_played = True



    async def receive(self, text_data):

        game = self.game
        message = json.loads(text_data)
        action = message['action']
        game.player = await self.get_player(message['player'])
        player = game.player
        game.is_played = await self.get_game_is_played(game)
        player.in_game = await self.get_player_in_game(player)
        how_many_players_ready = await self.get_how_many_players_ready(game)
        max_players = await self.get_max_players(game)
        host = await self.get_host(game)
        gameState = {'Error': "WRONG GAME STATE!"}


        if action=="ready":
            if not game.is_played and not player.in_game and how_many_players_ready < max_players:
                await self.add_player_to_game(player, game)
                await self.set_player_game_status_ready(player)
            elif not game.is_played and player.in_game:
                await self.remove_player_from_game(player, game)
                await self.set_player_game_status_off(player)

            gameState = {
                "action": "player_ready",
                "players_ready": await self.get_players_ready(game),
            }

        elif action=="start":
            if how_many_players_ready >1 and host == player.nick :
                print("We can start game")
                await self.set_game_played(game)
                ready_players = await self.get_players_ready(game)
                for i in ready_players:
                    print(i)

                gameState = {
                    "action": "start_game",
                    "game_played": await self.get_game_is_played(game),
                    "players_ready": await self.get_players_ready(game),
                    "mess": "start, Conditions matched!",
                }
            else:
                gameState = {
                    "action": "start_game",
                    "game_played": await self.get_game_is_played(game),
                    "players_ready": await self.get_players_ready(game),
                    "mess": "start_failure conditions cannot be matched",
                }


        elif action=="initial state":
            print("Initial state!")
            gameState = {
                "name": game.name,
                "action": "initial_state",
                "players_ready": await self.get_players_ready(game),
                "mess": "Initial State sent",
            }

        await database_sync_to_async(game.save)()
        await database_sync_to_async(player.save)()
        print (self.get_players_ready(game))
        stateSend = json.dumps(gameState)
        await (self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'game_message',
                'message': stateSend,
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
