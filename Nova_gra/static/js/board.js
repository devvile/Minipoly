/*
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
*/
