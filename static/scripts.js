function openLogIn() {
  document.getElementById("logInPopUp").style.display = "block";
}

function closeLogIn() {
  document.getElementById("logInPopUp").style.display = "none";
}

function checkSignedIn(user) {
    if (user === undefined) {
        document.getElementById("logInButton").style.display = "block";
    } else {
        document.getElementById("logInButton").style.display = "none";
    }
}