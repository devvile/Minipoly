export { prepareBoard };

class Board {
  constructor(...args) {
    this.fields = args[0];
  }
}

const lista = [
  { nr: 1, value: 500 },
  { nr: 2, value: 1500 },
  { nr: 3, value: 200 },
];

const game_board = new Board(lista);

console.log(game_board.fields[1]["value"]);

function prepareBoard(boardSize) {
  const board = document.querySelectorAll(".game_field");
  let counter = 1;
  const bSize = boardSize - 1;

  board.forEach((elem) => {
    const field = document.createElement("div");
    field.classList.add("boardField");
    elem.appendChild(field);
    if (counter <= bSize * 2) {
      field.id = counter++;
    }
    //(boardsize -1) * 2
  });
  let x = document.getElementById("12");
  x.style.backgroundColor = "red";
}
