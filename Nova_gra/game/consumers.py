from channels.generic.websocket import AsyncWebsocketConsumer
import json, random
from django.core import serializers
from channels.db import database_sync_to_async
from .models import Game, Field
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
    def get_players_state(self, game):
        players = [i for i in game.who_is_playing.all()]
        res = serializers.serialize("json", players)
        return res

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
    def get_player_game_name(self, player):
        return player.in_game

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
    def get_config(self, game):
        return game.config

    @database_sync_to_async
    def get_fields(self, fields_nr):
        return serializers.serialize("json", Field.objects.all()[:fields_nr])

    @database_sync_to_async
    def get_whose_turn(self, game):
        return game.turn_of_player.nick

    @database_sync_to_async
    def get_player_position(self, player):
        return player.position

    @database_sync_to_async
    def get_players_positions(self, game):
        x = {i.nick: i.position for i in game.who_is_playing.all()}
        print(x)
        return x

    @database_sync_to_async
    def get_players(self, game):
        x = [i for i in game.who_is_playing.all()]
        return serializers.serialize("json", x)

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
    def set_player_position(self, player, position):
        player.position = position

    @database_sync_to_async
    def set_player_moved(self, player):
        player.moved = True

    @database_sync_to_async
    def set_player_not_moved(self, player):
        player.moved = False

    @database_sync_to_async
    def set_first_player_turn(self, game):
        game.turn_of_player = game.first_player

    @database_sync_to_async
    def set_player_game(self, game, player):
        player.in_game = game.name

    @database_sync_to_async
    def set_player_game_to_none(self, player):
        player.in_game = "none"

    @database_sync_to_async
    def set_player_ready(self, player):
        player.set_ready()

    @database_sync_to_async
    def set_player_not_ready(self, player):
        player.set_not_ready()

    @database_sync_to_async
    def set_game_played(self, game):
        game.is_played = True

    @database_sync_to_async
    def set_game_ended(self, game):
        game.is_played = False

    @database_sync_to_async
    def set_next_turn(self, game):
        game.turn_of_player = game.next_player

    @database_sync_to_async
    def set_player_money(self, player, money):
        player.money += money


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
        game_state = "Game state not assigned!"

        if action == "ready":
            if not game.is_played and how_many_players_ready < max_players and not player.ready:
                if game.name != player.in_game:
                    await self.add_player_to_game(player, game)
                    await self.set_player_ready(player)
                    await self.set_player_game(game,player)
                    mess = "You're ready!"
                else:
                    mess = "Can't set status to 'ready', because you're playing in another game"
            elif not game.is_played and player.ready and game.name == player.in_game:
                await self.remove_player_from_ready_players(player, game)
                await self.set_player_not_ready(player)
                await self.set_player_game_to_none(player)
                mess = "You left the game!"
            else:
                mess = "Cannot join game, probably you're already in different game"
            game_state = await self.get_state(game, "player_ready", mess)


        elif action == "start":
            if how_many_players_ready >1 and host == player.nick:
                await self.set_game_played(game)
                ready_players = await self.get_players_ready(game)
                for i in ready_players:
                    i = await self.get_player(i)
                    await self.add_player_to_players_playing(i, game)
                    await self.set_player_position(i, 0)
                    await self.remove_player_from_ready_players(i, game)
                await self.set_first_player_turn(game)
                game_state = await self.get_state(game, "start_game", "Game Started!")

            else:
                game_state = await self.get_state(game, "start_failure", "Failed to start game, you're not a host, or there is not enough players")

        elif action == "initial state":
            config = await self.get_config(game)
            fields_nr = config.nr_of_fields
            fields = await self.get_fields(fields_nr)
            game_state = await self.get_state(game, "initial_state", fields)

        elif action == "end_turn":
            whose_turn = await self.get_player(await self.get_whose_turn(game))
            if game.player == whose_turn:
                if game.player.moved is True:
                    await self.set_next_turn(game)
                    await self.set_player_not_moved(player)
                    game_state = await self.get_state(game, "end_turn", "Turn Ended!")
                else:
                    game_state = await self.get_state(game, "end_turn", "First roll a dice!")
            else:
                game_state = await self.get_state(game, "end_turn", "It's not your turn!")

        elif action == "end_turn_timeout":
            await self.set_next_turn(game)
            await self.set_player_not_moved(player)
            game_state = await self.get_state(game, "end_turn", "Turn Ended!")

        elif action == "roll_dice":
            if player == game.turn_of_player and player.moved is False:
                move = random.randint(1, 6)
                old_pos = await self.get_player_position(player)
                new_pos = old_pos + move
                config = await self.get_config(game)
                fields_nr = config.nr_of_fields
                if new_pos >= fields_nr:
                    new_pos -= fields_nr
                await self.set_player_position(player, new_pos)
                await self.set_player_moved(player)
                game_state = await self.get_state(game, "roll_dice", move)
            elif player != game.turn_of_player:
                game_state = await self.get_state(game, "roll_dice", "It's not your turn!")
            else:
                game_state = await self.get_state(game, "roll_dice", "You already moved! Please end your turn.")

        elif action == "change_money":
            money_change = message['amount']
            await self.set_player_money(player, money_change)

        elif action == "leave_game":
            if player != host:
                await self.remove_player_from_game(player, game)
                await self.set_player_game_to_none(player)
                game_state = await self.get_state(game, "leave_game", "You left game!")
            else:
                game_state = await self.get_state(game, "leave_game", "Host Cannot leave game")

        elif action == "end_game":
            if number_of_players_playing > 1 and host == player.nick:
                await self.set_game_ended(game)
                await self.remove_players_from_game(game)
                await self.set_player_game_to_none(player)
                game_state = await self.get_state(game, "end_game", "Game Ended!")

            elif player != host:
                game_state = await self.get_state(game, "end_game", "Only Host can end game!")

            else:
                game_state = await self.get_state(game, "end_game", "You cannot end game while players are playing!")

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


    async def get_state(self, game, action, mess):
        game.is_played = await self.get_game_is_played(game)
        if game.is_played:
            whose_turn = await self.get_whose_turn(game)
        else:
            whose_turn = "Game hasn't started yet!"
        game_state = dict(action=action, name=game.name, host=await self.get_host(game),
                          who_is_ready=await self.get_players_ready(game),
                          who_is_playing=await self.get_who_is_playing(game), is_played=game.is_played,
                          max_players=await self.get_max_players(game), turn=await self.get_turn(game),
                          turn_of_player=whose_turn, players_state=await self.get_players_state(game), mess=mess)
        return game_state


    async def disconnect(self, close_code):
        await (self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        await self.close()
