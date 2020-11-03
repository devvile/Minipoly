function main() {
  configGame();
}

function configGame() {
  const socket = "ws://" + window.location.host + "/";
  websocket = new WebSocket(socket);

  function asignEvents() {
    const ready_btn = document.querySelector(".--ready_btn");
    const start_btn = document.querySelector(".--start_btn");
    ready_btn.addEventListener("click", () => {
      sendMess("Ready");
    });
    start_btn.addEventListener("click", () => {
      sendMess("Start");
    });
  }

  function openWebsocket() {
    console.log("Establishing Websocket Connection...");
    websocket.onopen = () => {
      console.log("Websocket Connection Established!");
      console.log(websocket);
    };
  }
  function setWebsocket() {
    websocket.onmessage = (mess) => {
      dataJson = JSON.parse(mess.data);
      console.log(mess.data);
      console.log(`Message:  ${mess.data}`);
    };

    websocket.onclose = () => {
      console.log("Websocket Connection Terminated!");
    };
  }
  function sendMess(messText) {
    websocket.send(messText);
  }
  asignEvents();
  openWebsocket();
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
