import { sendMess } from "./game.js";
import { preparePlayers } from "./prepare.js";

export { asignEvents, checkState, currentPlayer, players };

const players = preparePlayers({ who_is_playing: ["dottore", "elizka"] });
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

function asignEvents(game) {
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
