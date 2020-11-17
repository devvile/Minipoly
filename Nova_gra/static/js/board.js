export { prepareBoard };

function prepareBoard() {
  const board = document.querySelectorAll(".game_field");

  board.forEach((elem) => {
    const field = document.createElement("div");
    field.classList.add("boardField");
    elem.appendChild(field);
  });
}
