function main() {
  configGame();
}

function configGame() {
  const socket = "ws://" + window.location.host + window.location.pathname;
  const websocket = new WebSocket(socket);
  const playerName = document.querySelector(".playerName_header").textContent;

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

  function asignEvents() {
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
  }

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
      dataJson = JSON.parse(mess.data);
      dataJson = JSON.parse(dataJson.message);

      if (dataJson.action === "initial_state") {
        makeInitialState(dataJson);
      }
      if (dataJson.action === "player_ready") {
        playersReady(dataJson);
      }
      if (dataJson.action === "start_game") {
        startGame(dataJson);
      }
    };

    function playersReady(dataJson) {
      const playersReadyText = document.querySelector(".players_ready_text");
      playersReadyText.textContent = `Players ready: ${dataJson.players_ready}`;
    }

    function makeInitialState(dataJson) {
      (game.name = dataJson.name),
        (game.is_played = dataJson.is_played),
        (game.host = dataJson.host),
        (game.players_ready = dataJson.players_ready),
        (game.who_is_ready = dataJson.who_is_ready),
        (game.max_players = dataJson.max_players),
        (game.turn = dataJson.turn),
        (game.turn_of_player = dataJson.turn_of_player);

      console.log(game.host + " host");
      console.log(game.turn);
      return game;
    }

    function startGame(dataJson) {
      game.is_played = true;
      console.log(game.is_played);
    }

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

  openWebsocket();
  asignEvents();
  setWebsocket();
}

// Asigning Event Listneres to DOM ELEMENTS

function asignEvents() {
  const ready_btn = document.querySelector(".--ready_btn");
  const start_btn = document.querySelector(".--start_btn");
  ready_btn.addEventListener("click", () => {
    console.log("Ready");
  });
  start_btn.addEventListener("click", () => {
    console.log("Start");
  });
}

main();
