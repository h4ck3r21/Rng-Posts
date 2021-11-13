console.log(document.getElementById("user").innerHTML)
console.log(document.getElementById("login-error").innerHTML)

if (document.getElementById("user").innerHTML == "None") {

        console.log("not signed in");
        document.getElementById("loginButton").style.display = "block";
        document.getElementsByClassName('signed-in');

} else {

    console.log("signed in");
    document.getElementById("loginButton").style.display = "none";
    document.getElementsByClassName('signed-in');

}

if (document.getElementById("login-error").innerHTML != "") {
    openLogin()
}