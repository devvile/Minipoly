export { prepareBoard, giveMoney, makeMove, renderPosition };

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
  let old_poss = player.position;
  let new_poss = player.position + fileds_to_move;
  if (new_poss >= 28) {
    new_poss -= 28;
    giveMoney(player, 400);
  }
  player.position = new_poss;
  console.log("old poss " + old_poss);
  console.log("player poss " + new_poss);
  renderMove(player, old_poss);
  return player;
}
// po co tworzyc tylko przesuwac
function renderMove(player, old_poss) {
  let new_field = document.getElementById(player.position);
  let old_field = document.getElementById(old_poss);
  const pawn = document.getElementById(player.name);
  new_field.appendChild(pawn);
}

function renderPosition(players) {
  players.forEach((player) => {
    let position = document.getElementById(player.position);
    const pawn = document.createElement("div");
    pawn.setAttribute("id", player.name);
    pawn.classList.add("pawn");
    position.appendChild(pawn);
    let color = player.color;
    pawn.style.backgroundColor = color;
  });
}
