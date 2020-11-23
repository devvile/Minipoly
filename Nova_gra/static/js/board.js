export { prepareBoard };

function prepareBoard(boardSize) {
  const board = document.querySelectorAll(".game_field");
  let counter = 1;
  const bSize = boardSize - 1;

  board.forEach((elem) => {
    const field = document.createElement("div");
    field.classList.add("boardField");
    elem.appendChild(field);
    field.id = counter++;
  });
  let x = document.getElementById("16");
  x.style.backgroundColor = "red";
}
