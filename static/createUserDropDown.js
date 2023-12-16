function createDropDown(menu, dropDownID)
{
    var dropdown = document.getElementById(dropDownID);
    console.log(menu);
    for (index in menu) {
        let option =  document.createElement("option");
        option.text = menu[index][0];
        option.value = menu[index][1]
        dropdown.add(option);
        console.log(option);
    }
}

function setupUserList(users)
{
    if (users != "[]") {
        users = users.substring(5, users.length - 5);
        users = users.split("&gt;, &lt;");
        var userList = []
        console.log(users);
        for (index in users) {
                let user = users[index];
                parts = user.split(" ");
                userList.push([parts[1], parts[0].substring(4)])
        }
        return userList;
    }
}