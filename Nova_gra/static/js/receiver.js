export {
  playersReady,
  makeInitialState,
  startGame,
  endTurn,
  endGame,
  refreshGame,
  setState,
};

import { prepareBoard, makeMove } from "./board.js";
import { game } from "./game.js";

import {
  makeInvisible,
  makeVisible,
  refreshPlayers,
  Game,
  Board,
} from "./prepare.js";

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

  function prepareFields(dataJson) {
    let fields = JSON.parse(dataJson.mess);
    const board = new Board(fields);
    return board;
  }

  aquireInitialState(dataJson);
  renderInitialState(game);
  let boardFields = prepareFields(dataJson);
  prepareBoard();
  return boardFields;
}

function gameRender(game) {
  if (game.is_played === true) {
    makeVisible(game);
  } else {
    makeInvisible();
  }
  playersReady(game);
}

function startGame(dataJson) {
  makeVisible();
  game.turn_of_player = dataJson.turn_of_player;
  game.who_is_playing = dataJson.who_is_playing;
  game.is_played = true;
  refreshPlayers(dataJson);
  console.log("Game starting");
}

function endGame(dataJson) {
  makeInvisible();
  game.is_played = false;
  console.log("endGame");
}

async function setState(game) {
  refreshPlayers(game);
}

function refreshGame(dataJson) {
  {
    (game.name = dataJson.name),
      (game.is_played = dataJson.is_played),
      (game.host = dataJson.host),
      (game.who_is_ready = dataJson.who_is_ready),
      (game.who_is_playing = dataJson.who_is_playing),
      (game.max_players = dataJson.max_players),
      (game.turn = dataJson.turn),
      (game.turn_of_player = dataJson.turn_of_player);
  }
}

function endTurn(state) {
  setTimeout(setState, 200, state);
}
