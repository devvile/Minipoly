export { makeInvisible, makeVisible, refreshPlayers };

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
