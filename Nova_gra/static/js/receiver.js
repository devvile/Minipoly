export { playersReady, makeInitialState, startGame, endTurn, endGame, game };

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

const game = new Game();

function playersReady(state) {
  if (state.is_played === false) {
    const playersReadyText = document.querySelector(".players_ready_text");
    playersReadyText.textContent = `Players ready: ${state.who_is_ready}`;
  } else {
    console.log("GAME ALREADY STARTED CANNOT MAKE PLAYER READY");
  }
}

function makeInitialState(dataJson) {
  function aquireInitialState(dataJson) {
    (game.name = dataJson.name),
      (game.is_played = dataJson.is_played),
      (game.host = dataJson.host),
      (game.who_is_ready = dataJson.who_is_ready),
      (game.who_is_playing = dataJson.who_is_playing),
      (game.max_players = dataJson.max_players),
      (game.turn = dataJson.turn),
      (game.turn_of_player = dataJson.turn_of_player);
  }

  function renderInitialState(game) {
    gameRender(game);
  }

  aquireInitialState(dataJson);
  renderInitialState(game);
  return game;
}

function gameRender(game) {
  console.log("Rendering game state!");
  console.log("GAME IS PLAYED:" + game.is_played);
  if (game.is_played === true) {
    makeVisible();
  } else {
    console.log("making invisible");
    makeInvisible();
  }
  playersReady(game);
}

function startGame(dataJson) {
  makeVisible();
  game.is_played = true;
  console.log("Game starting");
}

function endGame(dataJson) {
  makeInvisible();
  game.is_played = false;
  console.log("endGame");
}

function endTurn(dataJson) {
  console.log("endTurn");
}

function makeVisible() {
  const playerOptions = document.querySelector(".__sidebar_menu_column");
  playerOptions.style.display = "flex";
}

function makeInvisible() {
  const playerOptions = document.querySelector(".__sidebar_menu_column");
  playerOptions.style.display = "none";
}
