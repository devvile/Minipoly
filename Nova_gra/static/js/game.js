export { notify, sendMess, game };

import {
  playersReady,
  makeInitialState,
  startGame,
  endGame,
  endTurn,
  refreshGame,
} from "./receiver.js";

import { makeMove, renderPosition } from "./board.js";
import { preparePlayers, Game } from "./prepare.js";
import { asignEvents, checkState, currentPlayer, players } from "./buttons.js";

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
  //functions

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
      refreshGame(dataJson);

      //players def

      switch (state.action) {
        case "initial_state":
          window.board = makeInitialState(state);
          //wyparsowac state.players_state
          console.log(players_state);
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
    //INITIAL SETUP

    websocket.onclose = () => {
      console.log("Websocket Connection Terminated!");
    };
  }
  openWebsocket();
  setWebsocket();
  setTimeout(asignEvents, 1000, game);
}

function main() {
  configGame();
}
1;
main();
