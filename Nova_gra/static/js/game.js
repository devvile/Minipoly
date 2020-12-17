export { notify, sendMess, game };

import {
  playersReady,
  makeInitialState,
  startGame,
  endGame,
  endTurn,
  refreshGame,
} from "./receiver.js";

import { makeMove, rollDice } from "./board.js";
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

      function asignPlayers(state) {
        if (state.is_played === true) {
          const players = preparePlayers(players_state);
          return players;
        } else {
          console.log("Players not asinged = game hasn't started yet");
        }
      }

      function getCurrentPlayer(players, state) {
        //TO REFACTOR
        if (state.is_played === true) {
          const currentPlayer = players.filter((value) => {
            return value.name == playerName;
          })[0];
          return currentPlayer;
        } else {
          const currentPlayer = document.querySelector(".playerName_header")
            .textContent;
          return currentPlayer;
        }
      }
      //gdy gra nie rozpoczeta problem z players
      // wziac stan gry
      // przypisac do obiektow player po stronie gracza
      // wyrenderowac
      refreshGame(dataJson);

      switch (state.action) {
        case "initial_state":
          window.board = makeInitialState(state);
          let players = asignPlayers(state); //need to refactor players/players_move + currentPlayer/playerPlaying
          let playerPlaying = getCurrentPlayer(players, state); //REAFACTOR it!
          refreshMoney(playerPlaying);
          renderPosition(players, state);
          break;
        case "player_ready":
          let players_ready = asignPlayers(state); //need to refactor players/players_move + currentPlayer/playerPlaying
          let playerReady = getCurrentPlayer(players_ready, state);
          if (playerReady.playing !== true) {
            playersReady(state);
            notify(state.mess);
          } else {
            notify(
              "You cannot join game because you are already playing in another one!"
            );
          }
          break;
        case "start_game":
          startGame(state);
          asignPlayers(state);
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
          let players_move = asignPlayers(state);
          let currentPlayer = getCurrentPlayer(players_move, state);
          if (currentPlayer.moved === false) {
            if (state.turn_of_player === currentPlayer.name) {
              rollDice(state.mess);
              setTimeout(makeMove, 1000, state, currentPlayer, state.mess);
              notify(`You move ${state.mess} fields!`);
              refreshMoney(currentPlayer);
            } else {
              notify(state.mess);
            }
          } else if (currentPlayer.moved === true) {
            notify(state.mess);
          }
          break;
        case "start_failure":
      }
    };
  }
  //INITIAL SETUP

  websocket.onclose = () => {
    console.log("Websocket Connection Terminated!");
  };

  function renderPosition(players, game) {
    if (game.is_played === false) {
      console.log("Position not rendered - game hasn't started yet!");
    } else {
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
  }

  function refreshMoney(player) {
    const moneyField = document.querySelector(".moneyField");
    moneyField.textContent = `Money: ${player.money}`;
  }

  openWebsocket();
  setWebsocket();
  setTimeout(asignEvents, 1000, game);
}

function main() {
  configGame();
}

main();
