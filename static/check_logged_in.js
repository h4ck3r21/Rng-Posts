console.log(document.getElementById("user").innerHTML)
console.log(document.getElementById("login-error").innerHTML)
console.log(document.getElementsByClassName('signed-in'))

if (document.getElementById("user").innerHTML == "None") {

        console.log("not signed in");
        document.getElementById("loginButton").style.display = "block";
        document.getElementById('signed-in').style.display = "none";

} else {

    console.log("signed in");
    document.getElementById("loginButton").style.display = "none";
    document.getElementById('signed-in').style.display = "block";

}

if (document.getElementById("login-error").innerHTML != "None") {
    openLogin()
}


var login_error = document.getElementById("login-error")
if (login_error.innerHTML == "None") {
    login_error.style.display = "none"
}