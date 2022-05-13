function openLogin() {
  document.getElementById("loginPopUp").style.display = "block";
}

function closeLogin() {
  document.getElementById("loginPopUp").style.display = "none";
}

function removeRow(input) {
  document.getElementById('content').removeChild(input.parentNode);
}


