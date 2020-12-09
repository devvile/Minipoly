export { prepareBoard, giveMoney, makeMove, rollDice };
import { notify, game } from "./game.js";

function prepareBoard(boardSize) {
  const board = document.querySelectorAll(".game_field");
  let counter = 0;
  const bSize = boardSize - 1;

  board.forEach((elem) => {
    const field = document.createElement("div");
    field.classList.add("boardField");
    elem.appendChild(field);
    field.id = counter++;
  });
}

function giveMoney(player, money) {
  player.money += money;
  console.log(`${money} granted to ${player.name}`);
}

function makeMove(game, player, fileds_to_move) {
  if (player.name === game.turn_of_player) {
    if (player.moved === false) {
      let old_poss = player.position;
      let new_poss = player.position + fileds_to_move;
      if (new_poss >= 28) {
        new_poss -= 28;
        giveMoney(player, 400);
      }
      player.position = new_poss;

      renderMove(player, old_poss);

      player.moved = true;
      notify(`You moved ${fileds_to_move} fields!`);
      return player;
    } else {
      notify("You already moved!");
    }
  } else {
    notify("It's not your turn!");
  }
}
// po co tworzyc tylko przesuwac
function renderMove(player, old_poss) {
  let new_field = document.getElementById(player.position);
  let old_field = document.getElementById(old_poss);
  const pawn = document.getElementById(player.name);
  new_field.appendChild(pawn);
}

function rollDice(num) {
  setTimeout(setDice, 100, randomize());
  setTimeout(setDice, 300, randomize());
  setTimeout(setDice, 500, randomize());
  setTimeout(setDice, 750, randomize());
  setTimeout(setDice, 1000, num);

  function randomize() {
    let nr = Math.ceil(Math.random() * 6);
    return nr;
  }

  function setDice(nr) {
    const dice = document.querySelector(".dice");
    dice.src = `/static/img/dice${nr}.svg`;
  }
}
