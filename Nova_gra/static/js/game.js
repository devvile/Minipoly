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

    //MESS RESPONSE FUNCTIONS

    function playersReady(game) {
      const playersReadyText = document.querySelector(".players_ready_text");
      playersReadyText.textContent = `Players ready: ${game.who_is_ready}`;
    }

    //INITIAL SETUP

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
        console.log("Rendering Initial State");
        playersReady(game);
        console.log(typeof game);
      }

      aquireInitialState(dataJson);
      renderInitialState(game);
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

  //EVENTS ASSIGNMENT

  function asignEvents() {
    console.log("AsSINGING EVENTS");

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
    }
  }

  openWebsocket();
  setWebsocket();
  // dopiero po skonczeniu wykonywania jakos
  asignEvents();
}

main();
