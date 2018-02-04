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


function startTimer(duration) {
    var timer = duration, minutes, seconds;
    setInterval(function () {
        minutes = parseInt(timer / 60, 10)
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        document.getElementById("minutes").innerHTML = minutes;
        document.getElementById("seconds").innerHTML = seconds;

        if (--timer < 0) {
            timer = duration;
        }
    }, 1000);
}
       

// ACTIVITY LOG CODE

// Generates a table row
function generate_row(data, rowNum){
    var row = document.createElement("tr");

    machine_info = data[rowNum]

    th = document.createElement("th");
    th.scope = "row";
    th_text = document.createTextNode(machine_info["name"]);
    th.appendChild(th_text);
    row.appendChild(th);

    type = document.createElement("td");
    type_txt = document.createTextNode(machine_info["type"]);
    type.appendChild(type_txt);
    row.appendChild(type);

    user = document.createElement("td");
    user_txt = document.createTextNode(machine_info["last_user"]["name"]);
    user.appendChild(user_txt);
    row.appendChild(user);

    user_email = document.createElement("td");
    user_email_txt = document.createTextNode(machine_info["last_user"]["email"]);
    user_email.appendChild(user_email_txt);
    row.appendChild(user_email);

    return row;
}

function generate_all_rows(data){
    var rows = [];

    for (var i = 0; i < data.length; i++){
        rows.push(generate_row(data, i));
    }

    return rows;
}

// Updates the table
function update_table(tbl, rows){
    // add all of the rows to the body
    for (var r = 0; r < rows.length; r++){
        tbl.appendChild(rows[r]);
    }
}

// Loads activity log
function loadActivityLog(table, data){
    rows = generate_all_rows(data)
    update_table(table, rows);
}
