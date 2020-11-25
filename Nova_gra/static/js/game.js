export { notify };

import {
  playersReady,
  makeInitialState,
  startGame,
  game,
  endGame,
  endTurn,
  refreshGame,
} from "./receiver.js";

import { makeMove, renderPosition } from "./board.js";
import { preparePlayers } from "./prepare.js";

//FUNCTIONS TO EXPORT

function notify(notification) {
  const notifBoard = document.querySelector(".notification-board");
  notifBoard.textContent = notification;
}

function configGame() {
  //socket
  const socket = "ws://" + window.location.host + window.location.pathname;
  const websocket = new WebSocket(socket);
  const players = preparePlayers({ who_is_playing: ["dottore", "elizka"] });

  //player
  const playerName = document.querySelector(".playerName_header").textContent;
  const currentPlayer = players.filter((value) => {
    return value.name == playerName;
  })[0];

  function checkState() {
    sendMess({
      player: playerName,
      action: "initial state",
    });
  }

  function sendMess(messObj) {
    const mess = JSON.stringify(messObj);
    websocket.send(mess);
  }

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
      refreshGame(dataJson);

      //players def

      switch (state.action) {
        case "initial_state":
          window.board = makeInitialState(state);
          console.dir(window.board["fields"]);
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

  //EVENTS ASSIGNMENT

  function asignEvents() {
    console.dir(game);

    if (game.is_played === false) {
      const ready_btn = document.querySelector(".--ready_btn");
      const start_btn = document.querySelector(".--start_btn");

      ready_btn.addEventListener("click", () => {
        sendMess({
          player: playerName,
          action: "ready",
        });
      });

      start_btn.addEventListener("click", () => {
        sendMess({
          player: playerName,
          action: "start",
        });
      });

      // GAME STARTED
    } else {
      const end_turn_btn = document.querySelector(".--end_turn_btn");
      const end_game_btn = document.querySelector(".--end_game_btn");
      const leave_game_btn = document.querySelector(".--leave_game_btn");
      const roll_dice_btn = document.querySelector(".--roll_btn");

      end_turn_btn.addEventListener("click", () => {
        sendMess({
          player: playerName,
          action: "end_turn",
        });
      });

      end_game_btn.addEventListener("click", () => {
        sendMess({
          player: playerName,
          action: "end_game",
        });
      });

      leave_game_btn.addEventListener("click", () => {
        sendMess({
          player: playerName,
          action: "leave_game",
        });
      });

      roll_dice_btn.addEventListener("click", () => {
        sendMess({
          player: playerName,
          action: "roll_dice",
        });
      });

      console.log("Events Assigned!");
    }
  }
  openWebsocket();
  setWebsocket();
  setTimeout(asignEvents, 1000);
}

function main() {
  configGame();
}

main();
