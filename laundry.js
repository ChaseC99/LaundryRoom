function findMachineId(){
    m = location.href.split('?');
    f = m[1].split('=');
    return f[1];
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

    for(var i = 0; i < machines.length; i++){
        id = machines[i]["id"];
        action = "machineSelected(" + id + ")";
        name = machines[i]["name"];
        type = machines[i]["type"];

        p = document.createElement("p");
        p.style = "text-align: center";
        link = document.createElement("a");
        button = document.createElement("button");
        button.addEventListener('click', function(){
            machineSelected(this.value);
        });
        button.className = "btn";
        button.value = id;
        button.type = "button";
        button.innerHTML = name;

        link.appendChild(button);
        p.appendChild(link);

        if(type == "washer"){
            washer_div.appendChild(p);
        } else if(type == "dryer"){
            dryer_div.appendChild(p);
        }
    }
}

function addMachineName(id, element){
    request = new XMLHttpRequest();
    url = "http://169.234.81.18:8000/api/machine_info/" + id;

    request.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var machine_info = JSON.parse(this.responseText);
            element.innerHTML = machine_info["machine_name"];
        }
    };

    request.open("GET", url, true);
    request.send();
}

function machineSelected(id){
    request = new XMLHttpRequest();
    url = "http://169.234.81.18:8000/api/machine_info/" + id;

    request.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var machine_info = JSON.parse(this.responseText);

            end_time = machine_info["start_time"] + machine_info["duration"]*60*1000;
            current_time = + new Date();

            if (current_time < end_time){
                window.location.href = "machinebusy.html?machine=" + id;
            } else {
                window.location.href = "UserForm.html?machine=" + id;
            }
        }
    };

    request.open("GET", url, true);
    request.send();
}



function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    setInterval(function () {
        minutes = parseInt(timer / 60, 10)
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            timer = duration;
        }
    }, 1000);
}

window.onload = function () {
    var Minutes = 60 * 1 ,
        display = document.querySelector('#time');
    startTimer(Minutes, display);
};
       

