export {
  makeInvisible,
  makeVisible,
  refreshPlayers,
  preparePlayers,
  Game,
  Player,
  Board,
};

class Game {
  constructor(
    name,
    host,
    is_played,
    who_is_ready,
    max_players,
    turn,
    turn_of_player
  ) {
    this.name = name;
    this.host = host;
    this.is_played = is_played;
    this.who_is_ready = who_is_ready;
    this.max_players = max_players;
    this.turn = turn;
    this.turn_of_player = turn_of_player;
  }
}

class Board {
  constructor(...args) {
    this.fields = args[0];
  }
}

class Player {
  constructor(name, color, money, position, moved, estates, playing) {
    this.name = name;
    this.color = color;
    this.money = money;
    this.position = position;
    this.moved = moved;
    this.estates = estates;
    this.playing = playing;
  }
}

function preparePlayers(...args) {
  args = args[0];
  let players_total = args.length;
  if (players_total === 2) {
    let player1data = args[0]["fields"];
    let player2data = args[1]["fields"];
    let player1 = new Player(
      player1data.nick,
      "red",
      player1data.money,
      player1data.position
    );
    let player2 = new Player(
      player2data.nick,
      "blue",
      player2data.money,
      player2data.position
    );

    let players = [player1, player2];
    return players;
  }
}

function makeVisible(game) {
  const gamePlayed = document.querySelector(".--game_state");
  const visList = document.querySelectorAll(".--vis");
  const inVisList = document.querySelectorAll(".--invis");
  const menu = document.querySelector(".__sidebar_menu_column");

  gamePlayed.textContent = " GAME ALREADY STARTED!";

  visList.forEach((elem) => (elem.style.display = "none"));
  inVisList.forEach((elem) => (elem.style.display = "block"));
  menu.style.display = "flex";

  refreshPlayers(game);
}

function makeInvisible() {
  const visList = document.querySelectorAll(".--vis");
  const inVisList = document.querySelectorAll(".--invis");
  const gamePlayed = document.querySelector(".--game_state");

  gamePlayed.textContent = " GAME HASN'T STARTED YET!";
  visList.forEach((elem) => (elem.style.display = "block"));
  inVisList.forEach((elem) => (elem.style.display = "none"));
}

function refreshPlayers(game) {
  const playerTurnText = document.querySelector(".player_turn_text");
  const playersInGame = document.querySelector(".players_in_game");

  playerTurnText.textContent = ` ${game.turn_of_player} turn!`;
  playersInGame.textContent = ` Players in game: ${game.who_is_playing}`;
}
