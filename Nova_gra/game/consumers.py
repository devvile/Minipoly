from channels.generic.websocket import AsyncWebsocketConsumer
import json, random
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
    def get_first_player(self, game):
        temp = game.first_player
        return temp.nick

    @database_sync_to_async
    def get_next_player(self, game):
        return game.next_player

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
        game.who_is_ready.remove(player)

    @database_sync_to_async
    def remove_player_from_game(self, player, game):
        game.who_is_playing.remove(player)
        player.in_game = False

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
        max_players = await self.get_max_players(game)
        game.turn = await self.get_turn(game)
        host = await self.get_host(game)
        game_state = {'Error': "WRONG GAME STATE!"}

        if action == "ready":
            if not game.is_played and not player.in_game and how_many_players_ready < max_players:
                await self.add_player_to_game(player, game)
                await self.set_player_game_status_ready(player)
            elif not game.is_played and player.in_game:
                await self.remove_player_from_ready_players(player, game)
                await self.set_player_game_status_off(player)

            game_state = {
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

                game_state = {
                    "action": "start_game",
                    "is_played": await self.get_game_is_played(game),
                    "who_is_ready": await self.get_players_ready(game),
                    "turn": game.turn,
                    "turn_of_player": await self.get_first_player(game),
                    "mess": "start, Conditions matched!",
                }
            else:
                game_state = {
                    "action": "start_failure",
                    "mess": "Failed to start game, you're not a host, or there is not enough players"
                }

        elif action == "initial state":
            game_state = {
                "action": "initial_state",
                "name": game.name,
                "host" : game.host,
                "who_is_ready": await self.get_players_ready(game),
                "who_is_playing": await self.get_who_is_playing(game),
                "is_played": game.is_played,
                "max_players": game.max_players,
                "turn" : game.turn,
                "turn_of_player" : "Game hasn't started yet!",
                "mess": "Initial State sent",
            }

        elif action == "end_turn":
            turn_of_player = await self.get_next_player(game)
            print(turn_of_player)
            game_state = {
                "action": "end_turn",
                "name": game.name,
                "host" : game.host,
                "who_is_ready": await self.get_players_ready(game),
                "who_is_playing": await self.get_who_is_playing(game),
                "is_played": game.is_played,
                "max_players": game.max_players,
                "turn" : game.turn,
                "turn_of_player" : turn_of_player,
                "mess": "Turn Ended!",
            }
        elif action == "roll_dice":
            move = random.randint(1,6)
            game_state = {
                "action": "roll_dice",
                "name": game.name,
                "host" : game.host,
                "who_is_ready": await self.get_players_ready(game),
                "who_is_playing": await self.get_who_is_playing(game),
                "is_played": game.is_played,
                "max_players": game.max_players,
                "turn" : game.turn,
                "turn_of_player" : "tu bedzie czyja tura",
                "mess": "You move " + str(move) + " fields",
            }

        elif action == "leave_game":
            if player != host:
                await self.remove_player_from_game(player,game)
                game_state = {
                    "action": "leave_game",
                    "name": game.name,
                    "host" : game.host,
                    "who_is_ready": await self.get_players_ready(game),
                    "who_is_playing": await self.get_who_is_playing(game),
                    "is_played": game.is_played,
                    "max_players": game.max_players,
                    "turn" : 1,
                    "turn_of_player" : "tu bedzie czyja tura",
                    "mess": "You left game!",
                }
            else:
                game_state = {"action": "leave_game", "mess": " Host Cannot leave game"}

        elif action == "end_game":
            if  number_of_players_playing > 1 and host == player.nick:
                await self.set_game_ended(game)
                await self.remove_players_from_game(game)
                game_state = {
                        "action": "end_game",
                        "name": game.name,
                        "host": game.host,
                        "who_is_ready": await self.get_players_ready(game),
                        "who_is_playing": await self.get_who_is_playing(game),
                        "is_played": game.is_played,
                        "max_players": game.max_players,
                        "turn": 1,
                        "turn_of_player": "tu bedzie czyja tura",
                        "mess": "Game Ended!",
                    }
            elif player != host:
                game_state = {
                "action": "end_game", "mess": "Only Host can end game!"
                }
            else:
                game_state = {
                "action": "end_game",
                "mess": "You cannot end game while players are playing!"
                }

        await database_sync_to_async(game.save)()
        await database_sync_to_async(player.save)()
        stateSend = json.dumps(game_state)
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
