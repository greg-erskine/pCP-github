function pcp_confirm(prompt,goto) {
	var answer = confirm(prompt)
	if (answer) window.location = goto;
}

// Used for more/less help
function more(elementID) {
	var sel1 = document.getElementById(elementID);
	sel1.className = (sel1.className == 'less') ? 'more' : 'less';
	var sel2 = document.getElementById(elementID + "a");
	sel2.text = (sel2.text == 'less>') ? 'more>' : 'less>';
	return false;
}
// Used for LMS Controls Buttons
function ctrlmore(elementID) {
	var sel1 = document.getElementById(elementID);
	sel1.className = (sel1.className == 'ctrlless') ? 'ctrlmore' : 'ctrlless';
	var sel2 = document.getElementById(elementID + "a");
	sel2.text = (sel2.text == '\u25B2') ? "\u25BC" : "\u25B2";
	return false;
}

function setbg(elementID,color) {
	document.getElementById(elementID).style.background=color;
}

function pcp_copy_click_to_input(inputID,clickID) {
	document.getElementById(inputID).value = document.getElementById(clickID).innerHTML;
}

function pcp_redirect(delay,returnURL) {
	var duration = delay;
	showDuration();
	function showDuration() {
		document.getElementById("countdown").innerHTML = "Redirection in " + duration + " seconds.";
		duration--;
		if (duration >=0) {
			window.setTimeout(showDuration, 1000);
		}
		else {
			window.location.href = returnURL;
		}
	}
}

function pcp_delete_query_string() {
	if (history.pushState) {
		var newurl = window.location.origin + window.location.pathname;
		window.history.pushState({path:newurl},"",newurl);
	}
}

function makeArgs() {
	return arguments;
}

function lms_controls_send() {
	var lmsip = arguments[0];
	var lmsport = arguments[1];
	var playername = arguments[2];
	var xhttp = new XMLHttpRequest();
	xhttp.open("POST", "http://" + lmsip + ":" + lmsport + "/jsonrpc.js", true);
	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	var data = {"id":1,"method":"slim.request","params": [ playername, [ "" ]]};
	for (var i = 0; i < (arguments.length - 3); i++) {
		data.params[1][i] = arguments[i+3];
	}
	var jsondata = JSON.stringify(data);
	try {
		xhttp.send(jsondata);
	} catch(err) {
		console.log (err);
	}
	return;
}

