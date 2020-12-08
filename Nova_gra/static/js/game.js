export { notify, sendMess, game };

import {
  playersReady,
  makeInitialState,
  startGame,
  endGame,
  endTurn,
  refreshGame,
} from "./receiver.js";

import { makeMove } from "./board.js";
import { preparePlayers, Game } from "./prepare.js";
import { asignEvents, checkState, playerName } from "./buttons.js";

//FUNCTIONS TO EXPORT

function notify(notification) {
  const notifBoard = document.querySelector(".notification-board");
  notifBoard.textContent = notification;
}

function sendMess(messObj) {
  const mess = JSON.stringify(messObj);
  websocket.send(mess);
}

const game = new Game();

const socket = "ws://" + window.location.host + window.location.pathname;
const websocket = new WebSocket(socket);

function configGame() {
  function openWebsocket() {
    console.log("Establishing Websocket Connection...");
    websocket.onopen = () => {
      console.log("Websocket Connection Established!");
      checkState();
    };
  }

  function setWebsocket() {
    websocket.onmessage = (mess) => {
      console.log(`Message:  ${mess.data}`);
      let dataJson = JSON.parse(mess.data);
      let state = JSON.parse(dataJson.message);
      let players_state = JSON.parse(state.players_state);

      const players = preparePlayers(players_state);
      console.dir(players);

      const currentPlayer = players.filter((value) => {
        return value.name == playerName;
      })[0];
      console.log(currentPlayer);

      // wziac stan gry
      // przypisac do obiektow player po stronie gracza
      // wyrenderowac

      refreshGame(dataJson);

      switch (state.action) {
        case "initial_state":
          window.board = makeInitialState(state);
          renderPosition(players);
          break;
        case "player_ready":
          playersReady(state);
          break;
        case "start_game":
          startGame(state);
          break;
        case "end_game":
          endGame(state);
          notify(state.mess);
          break;
        case "end_turn":
          endTurn(state);
          notify(state.mess);
          break;
        case "roll_dice":
          makeMove(state, currentPlayer, state.mess);
          break;
        case "start_failure":
          notify(state.mess);
      }
    };
  }
  //INITIAL SETUP

  websocket.onclose = () => {
    console.log("Websocket Connection Terminated!");
  };

  function renderPosition(players) {
    players.forEach((player) => {
      let position = document.getElementById(player.position);
      const pawn = document.createElement("div");
      pawn.setAttribute("id", player.name);
      pawn.classList.add("pawn");
      position.appendChild(pawn);
      let color = player.color;
      pawn.style.backgroundColor = color;
    });
  }

  openWebsocket();
  setWebsocket();
  setTimeout(asignEvents, 1000, game);
}

function main() {
  configGame();
}

main();
