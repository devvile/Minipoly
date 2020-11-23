export { prepareBoard, giveMoney, makeMove };

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

function makeMove(player, fileds_to_move) {
  let old_field = document.getElementById(player.position);
  old_field.style.backgroundColor = "grey";
  let new_poss = player.position + fileds_to_move;
  if (new_poss >= 28) {
    new_poss -= 28;
    giveMoney(player, 400);
  }
  player.position = new_poss;
  renderMove(player);
}

function renderMove(player) {
  let new_field = document.getElementById(player.position);
  let color = player.color;
  new_field.style.backgroundColor = color;
}
