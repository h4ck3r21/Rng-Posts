console.log(document.getElementById("user").innerHTML)
console.log(document.getElementById("login-error").innerHTML)
console.log(document.getElementsByClassName('signed-in'))

if (document.getElementById("user").innerHTML == "None") {

        console.log("not signed in");
        document.getElementById("loginButton").style.display = "block";
        document.getElementById('signed-in').style.display = "none";
        document.getElementById("not-signed-in").style.display = "block";

} else {

    console.log("signed in");
    document.getElementById("loginButton").style.display = "none";
    document.getElementById('signed-in').style.display = "block";
    document.getElementById("not-signed-in").style.display = "none";

}

login_error = document.getElementById("login-error").innerHTML
if (login_error != "") {
    console.log("test")
    openLogin()
}

const lst_posts = document.getElementsByClassName("post")
for (index in lst_posts) {
    console.log(lst_posts[index]);
    //dragElement(lst_posts[index]);
}
