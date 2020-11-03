function main() {
  openWebsocket();
  asignEvents();
}

function openWebsocket() {
  console.log("Establishing Websocket Connection...");
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
