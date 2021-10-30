function openLogin() {
  document.getElementById("loginPopUp").style.display = "block";
}

function closeLogin() {
  document.getElementById("loginPopUp").style.display = "none";
}

function checkSignedIn() {
    if (document.getElementById("user").innerHTML === undefined) {
        document.getElementById("loginButton").style.display = "block";
    } else {
        document.getElementById("loginButton").style.display = "none";
    }
}
