base_url = "http://169.234.81.18:8000"

// Find Machine ID
// This method pulls the machine id from the url
//
// pre: url must contain a query string with the first parameter being the id
// 	ex: www.laundryRoom.com/?id=10
// post: returns str of id num
function findMachineId(){
    m = location.href.split('?');
    f = m[1].split('=');
    return f[1];
}

// Get Machines
// Sends a request to the server for the machines
// Recieves a json object containing information about the machines
// 
// onload: calls the addMachineButtons func to add machines to the page
function getMachines(){
    request = new XMLHttpRequest();
    url = base_url + "/api/all_machine/Nieblalaundryroom/";
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

// Add Machine Buttons
// Adds the machines to the index page
//
// pre: machines is a json object containing info about machines
// post: buttons for each machine are added to the page
function addMachineButtons(machines){
    // Get the divs for washer and dryer
    washer_div = document.getElementById("Washers");
    dryer_div = document.getElementById("Dryers");

	// Loop through the machines
    for(var i = 0; i < machines.length; i++){
        // Get information about machine from json
		id = machines[i]["id"];
        action = "machineSelected(" + id + ")";
        name = machines[i]["name"];
        type = machines[i]["type"];

		// Generate the html for the machine
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
		
		// put machine under either washer or dryer
        if(type == "washer"){
            washer_div.appendChild(p);
        } else if(type == "dryer"){
            dryer_div.appendChild(p);
        }
    }
}

// Add Machine Name
// Adds a machines name to an element based off of the given id
//
// post: element's inner html is set to the machine's name
function addMachineName(id, element){
    request = new XMLHttpRequest();
    url = base_url + "/api/machine_info/" + id;

    request.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var machine_info = JSON.parse(this.responseText);
            element.innerHTML = machine_info["machine_name"];
        }
    };

    request.open("GET", url, true);
    request.send();
}


// Machine Selected
// Determines whether to redirect the page to machinebusy or UserForm
// Checks current time against the machine's end time
//		if now is before the end time, machinebusy is displayed
//		if now is after the end time, UserForm is displayed
//
// post: redirected to a new page
function machineSelected(id){
    request = new XMLHttpRequest();
    url = base_url + "/api/machine_info/" + id;

    request.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var machine_info = JSON.parse(this.responseText);

			// Check current time against now
            end_time = machine_info["start_time"] + machine_info["duration"]*60*1000;
            current_time = + new Date();

			// If now is less than end time, display machine busy
			//	else display UserForm
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


// Start Timer
// Creates the timer on machinebusy
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

// Generate all rows
// Calls generate_row on all rows
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
