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
    def get_who_is_playing(self, game):
        x = [i.nick for i in game.who_is_playing.all()]
        return x

    @database_sync_to_async
    def get_how_many_players_playing(self, game):
        return game.how_many_players_playing

    @database_sync_to_async
    def get_max_players(self, game):
        return game.max_players

    @database_sync_to_async
    def get_host(self, game):
        return game.host

    @database_sync_to_async
    def get_turn(self, game):
        return game.turn

    @database_sync_to_async
    def add_player_to_game(self, player, game):
        return game.who_is_ready.add(player)

    @database_sync_to_async
    def add_player_to_players_playing(self, player, game):
        return game.who_is_playing.add(player)


    @database_sync_to_async
    def remove_player_from_ready_players(self, player, game):
        return game.who_is_ready.remove(player)

    @database_sync_to_async
    def remove_players_from_game(self, game):
        for i in game.who_is_playing.all():
            game.who_is_playing.remove(i)

    @database_sync_to_async
    def remove_players_from_players_ready(self, game):
        for i in game.who_is_ready.all():
            game.who_is_ready.remove(i)

    @database_sync_to_async
    def set_player_game_status_ready(self, player):
        player.set_player_in_game()

    @database_sync_to_async
    def set_player_game_status_off(self, player):
        player.set_player_leave_game()

    @database_sync_to_async
    def set_game_played(self, game):
        game.is_played = True

    @database_sync_to_async
    def set_game_ended(self, game):
        game.is_played = False


    async def receive(self, text_data):

        game = self.game
        message = json.loads(text_data)
        action = message['action']
        game.player = await self.get_player(message['player'])
        player = game.player
        game.is_played = await self.get_game_is_played(game)
        player.in_game = await self.get_player_in_game(player)
        how_many_players_ready = await self.get_how_many_players_ready(game)
        number_of_players_playing = await self.get_how_many_players_playing(game)
        print(number_of_players_playing)
        max_players = await self.get_max_players(game)
        game.turn = await self.get_turn(game)
        host = await self.get_host(game)
        gameState = {'Error': "WRONG GAME STATE!"}

        if action == "ready":
            if not game.is_played and not player.in_game and how_many_players_ready < max_players:
                await self.add_player_to_game(player, game)
                await self.set_player_game_status_ready(player)
            elif not game.is_played and player.in_game:
                await self.remove_player_from_ready_players(player, game)
                await self.set_player_game_status_off(player)

            gameState = {
                "action": "player_ready",
                "is_played": await self.get_game_is_played(game),
                "who_is_ready": await self.get_players_ready(game),
            }

        elif action == "start":
            if how_many_players_ready >1 and host == player.nick:
                await self.set_game_played(game)
                ready_players = await self.get_players_ready(game)
                for i in ready_players:
                    i = await self.get_player(i)
                    await self.add_player_to_players_playing(i, game)
                    await self.remove_player_from_ready_players(i, game)

                gameState = {
                    "action": "start_game",
                    "is_played": await self.get_game_is_played(game),
                    "who_is_ready": await self.get_players_ready(game),
                    "mess": "start, Conditions matched!",
                }
            else:
                gameState = {
                    "action": "start_failure",
                    "mess": "Failed to start game, you're not a host, or there is not enough players"
                }

        elif action == "initial state":
            print("Initial state!")
            gameState = {
                "action": "initial_state",
                "name": game.name,
                "host" : game.host,
                "who_is_ready": await self.get_players_ready(game),
                "who_is_playing": await self.get_who_is_playing(game),
                "is_played": game.is_played,
                "max_players": game.max_players,
                "turn" : game.turn,
                "turn_of_player" : "tu bedzie czyja tura",
                "mess": "Initial State sent",
            }

        elif action=="end_game":
            if self.number_of_players_playing > 2 and host == player.nick:
                print("END GAME!")
                await self.set_game_ended(game)
                await self.remove_players_from_game(game)
                gameState = {
                    "action": "end_game",
                    "name": game.name,
                    "host" : game.host,
                    "who_is_ready": await self.get_players_ready(game),
                    "who_is_playing": await self.get_who_is_playing(game),
                    "is_played": game.is_played,
                    "max_players": game.max_players,
                    "turn" : 1,
                    "turn_of_player" : "tu bedzie czyja tura",
                    "mess": "Game Ended!",
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
