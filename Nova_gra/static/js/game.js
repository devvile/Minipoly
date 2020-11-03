function main() {
  configWebsocket();
  asignEvents();
}

function configWebsocket() {
  const socket = "ws://" + window.location.host + "/";
  websocket = new WebSocket(socket);

  function openWebsocket() {
    console.log("Establishing Websocket Connection...");
    websocket.onopen = () => {
      console.log("Connection Established!");
      console.log(websocket);
    };
    openWebsocket();
  }
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
