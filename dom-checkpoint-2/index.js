const colorBox = document.getElementById("color-box");
const colorChangerBtn = document.getElementById("change-color-btn");

function generateRandomColor() {
  const randomColor = Math.floor(Math.random() * 16777215).toString(16);

  colorBox.style.backgroundColor = "#" + randomColor;
}

colorChangerBtn.addEventListener("click", generateRandomColor);
