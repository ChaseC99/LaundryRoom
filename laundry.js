function findMachineId(){
    m = location.href.split('?');
    f = m[1].split('=');    
    document.write(f[1]);
}

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
    washer_div = document.getElementById("Washers");
    dryer_div = document.getElementById("Dryers");
    console.log(dryer_div);

    for(var i = 0; i < machines.length; i++){
        link_url = "UserForm.html?machine=" + machines[i]["id"];
        id = machines[i]["id"];
        action = "machineSelected(" + id + ")";
        name = machines[i]["name"];
        type = machines[i]["type"];

        console.log(name);
        console.log(action)

        p = document.createElement("p");
        p.style = "text-align: center";
        link = document.createElement("a");
        link.href = link_url;
        button = document.createElement("button");
        button.addEventListener('click', function(){
            machineSelected(id);
        });
        button.className = "btn";
        button.type = "button";
        button.innerHTML = name;

        link.appendChild(button);
        p.appendChild(link);
        console.log(p);
        console.log(type);
        if(type == "washer"){
            washer_div.appendChild(p);
        } else if(type == "dryer"){
            dryer_div.appendChild(p);
        }
    }
}

function machineSelected(id){
    request = new XMLHttpRequest();
    url = "http://169.234.81.18:8000/api/machine_info/1";
    console.log(url)

    request.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var machine_info = JSON.parse(this.responseText);
            console.log(machine_info)

            end_time = machine_info["start_time"]/1000;
            console.log(end_time);
        }
    };

    request.open("GET", url, true);
    request.send();
}
