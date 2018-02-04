function getMachines(){
    request = new XMLHttpRequest();
    url = "http://169.234.81.18:8000/api/all_machine/Niebla%20laundry%20room/";
    console.log(url)

    request.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var machines = JSON.parse(this.responseText)["machines"];
            console.log(machines)
            addMachineButtons(machines);
        }
    };

    request.open("GET", url, true);
    request.send();
}

function addMachineButtons(machines){
    machine_div = document.getElementById("machines");

    for(var i = 0; i < machines.length; i++){
        link_url = "UserForm.html?machine=" + machines[i]["id"];
        name = machines[i]["name"];

        console.log(name);

        p = document.createElement("p");
        p.style = "text-align: center";
        link = document.createElement("a");
        link.href = link_url;
        button = document.createElement("button");
        button.className = "btn";
        button.type = "button";
        button.innerHTML = name;

        link.appendChild(button);
        p.appendChild(link);
        console.log(p);
        machine_div.appendChild(p);
    }
}
