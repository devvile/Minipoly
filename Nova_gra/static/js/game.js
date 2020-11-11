import { playersReady, makeInitialState, startGame, game } from "./receiver.js";

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
      console.log("state ation: " + state.action);

      if (state.action === "initial_state") {
        makeInitialState(state);
      }
      if (state.action === "player_ready") {
        playersReady(state);
      }
      if (state.action === "start_game") {
        startGame(state);
      }
    };

    //INITIAL SETUP

    websocket.onclose = () => {
      console.log("Websocket Connection Terminated!");
    };
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
    console.log("AsSINGING EVENTS");
    console.dir(game);

    //TUTAJ TRZEBA TO PRZESPISAC ASYNCHRONICZNIE
    if (game.is_played === false) {
      console.log("GRA NIE ZACZETa");
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
        console.log("send ready");
      });
    } else {
      console.log("Gra Zaczęta");
    }
  }

  openWebsocket();
  setWebsocket();
  // dopiero po skonczeniu wykonywania jakos
  setTimeout(asignEvents, 2000);
}
main();
