function main() {
  configGame();
}

// Musi istniec zapytanie wysyalne na poczatku aktualizujace stan

function configGame() {
  const socket = "ws://" + window.location.host + window.location.pathname;
  const websocket = new WebSocket(socket);
  const playerName = document.querySelector(".playerName_header").textContent;

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
      //Player Ready (jeszcze z max_players zrobic kontrolke)
      if (dataJson.action === "player_ready") {
        const playersReadyText = document.querySelector(".players_ready_text");
        playersReadyText.textContent = `Players ready: ${dataJson.players_ready}`;
      }
    };

    websocket.onclose = () => {
      console.log("Websocket Connection Terminated!");
    };
  }

  function checkState() {
    let mess = JSON.stringify({
      player: playerName,
      action: "game state",
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
