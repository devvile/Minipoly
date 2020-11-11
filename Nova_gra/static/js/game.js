import {
  playersReady,
  makeInitialState,
  startGame,
  game,
  endGame,
  endTurn,
} from "./receiver.js";

function main() {
  configGame();
}

function configGame() {
  const socket = "ws://" + window.location.host + window.location.pathname;
  const websocket = new WebSocket(socket);
  const playerName = document.querySelector(".playerName_header").textContent;

  function openWebsocket() {
    console.log("Establishing Websocket Connection...");
    websocket.onopen = () => {
      console.log("Websocket Connection Established!");
      checkState();
    };
  }

  // MESS RESPONSE

  function setWebsocket() {
    websocket.onmessage = (mess) => {
      console.log(`Message:  ${mess.data}`);
      let dataJson = JSON.parse(mess.data);
      let state = JSON.parse(dataJson.message);

      if (state.action === "initial_state") {
        makeInitialState(state);
      }
      if (state.action === "player_ready") {
        playersReady(state);
      }
      if (state.action === "start_game") {
        startGame(state);
      }
      if (state.action === "end_game") {
        endGame(state);
        notify(state.mess);
      }
      if (state.action === "end_turn") {
        endTurn(state);
      }
      if (state.action === "start_failure") {
        notify(state.mess);
      }
    };

    //INITIAL SETUP

    websocket.onclose = () => {
      console.log("Websocket Connection Terminated!");
    };
  }

  function notify(notification) {
    const notifBoard = document.querySelector(".notification-board");
    notifBoard.textContent = notification;
  }

  function checkState() {
    let mess = JSON.stringify({
      player: playerName,
      action: "initial state",
    });
    sendMess(mess);
  }

  function sendMess(messText) {
    websocket.send(messText);
  }

  //EVENTS ASSIGNMENT

  function asignEvents() {
    console.dir(game);

    if (game.is_played === false) {
      const ready_btn = document.querySelector(".--ready_btn");
      const start_btn = document.querySelector(".--start_btn");

      ready_btn.addEventListener("click", () => {
        let mess = JSON.stringify({
          player: playerName,
          action: "ready",
        });
        sendMess(mess);
      });

      start_btn.addEventListener("click", () => {
        let mess = JSON.stringify({
          player: playerName,
          action: "start",
        });
        sendMess(mess);
      });

      // GAME STARTED
    } else {
      const end_turn_btn = document.querySelector(".--end_turn_btn");
      const end_game_btn = document.querySelector(".--end_game_btn");
      const leave_game_btn = document.querySelector(".--leave_game_btn");

      end_turn_btn.addEventListener("click", () => {
        let mess = JSON.stringify({
          player: playerName,
          action: "end_turn",
        });
        sendMess(mess);
      });

      end_game_btn.addEventListener("click", () => {
        let mess = JSON.stringify({
          player: playerName,
          action: "end_game",
        });
        sendMess(mess);
      });
      leave_game_btn.addEventListener("click", () => {
        let mess = JSON.stringify({
          player: playerName,
          action: "leave_game",
        });
        sendMess(mess);
      });
    }
    console.log("Events Assigned!");
  }

  openWebsocket();
  setWebsocket();
  setTimeout(asignEvents, 700);
}
main();
