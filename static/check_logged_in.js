console.log(document.getElementById("user").innerHTML)
        if (document.getElementById("user").innerHTML == "None") {
            console.log("not signed in")
            document.getElementById("loginButton").style.display = "block";
        } else {
            console.log("signed in")
            document.getElementById("loginButton").style.display = "none";
        }