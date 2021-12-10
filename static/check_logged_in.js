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

if (document.getElementById("login-error").innerHTML != "None") {
    openLogin()
}


var login_error = document.getElementById("login-error")
if (login_error.innerHTML == "None") {
    login_error.style.display = "none"
}

const lst_posts = document.getElementsByClassName("post")
for (index in lst_posts) {
    console.log(lst_posts[index]);
    //dragElement(lst_posts[index]);
}

function dragElement(elmnt) {
  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  if (document.getElementById("postheader")) {
    document.getElementById("postheader").onmousedown = dragMouseDown;
  } else {
    elmnt.onmousedown = dragMouseDown;
    console.log("hello")
  }

  function dragMouseDown(e) {
    e = e || window.event;
    e.preventDefault();
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    // call a function whenever the cursor moves:
    document.onmousemove = elementDrag;
  }

  function elementDrag(e) {
    e = e || window.event;
    e.preventDefault();
    // calculate the new cursor position:
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    // set the element's new position:
    console.log(pos1)
    console.log(pos2)
    elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
    elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
  }

  function closeDragElement() {
    // stop moving when mouse button is released:
    document.onmouseup = null;
    document.onmousemove = null;
  }
}