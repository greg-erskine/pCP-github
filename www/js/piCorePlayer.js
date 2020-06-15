var theme;
var repo;

function pcp_confirm(prompt,goto) {
	var answer = confirm(prompt)
	if (answer) window.location = goto;
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

function pcp_switch_label(switchId,labelOn,labelOff) {
	var checkBox = document.getElementById(switchId);
	if (checkBox.checked == true){
		document.getElementById(switchId+"l").innerHTML=labelOn;
	} else {
		document.getElementById(switchId+"l").innerHTML=labelOff;
	}
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

function setplayertabs() {
	if ( document.getElementById("PlayerTabsAfter") === null ) {
		if ( document.readyState == "complete" ) return;
		setTimeout(setplayertabs, 100);
	} else {
		var url="http://" + window.location.hostname + "/cgi-bin/playerstabs.cgi";

		let request = new XMLHttpRequest();
		request.onreadystatechange = function () {
			if (this.readyState === 4) {
				if (this.status === 200) {
					document.getElementById("PlayerTabsAfter").insertAdjacentHTML('afterend', this.responseText);
				} else if (this.response == null && this.status === 0) {
					console.log("Error getting playertab data.");
				}
			}
		};
		request.open("GET", url, true);
		request.send(null);
	}
}

function loadcssfile(filename){
	var date = new Date();
	var timestamp = date.getTime();
	var fileref=document.createElement("link");
	fileref.setAttribute("rel", "stylesheet");
	fileref.setAttribute("type", "text/css");
	fileref.setAttribute("href", filename + '?' + timestamp);
	if (typeof fileref!="undefined")
		document.getElementsByTagName("head")[0].appendChild(fileref);
}

function removecssfile(filename){
	var targetelement="link";
	var targetattr="href";
	var allsuspects=document.getElementsByTagName(targetelement);
	for (var i=allsuspects.length; i>=0; i--){ 
		if (allsuspects[i] && allsuspects[i].getAttribute(targetattr)!=null && allsuspects[i].getAttribute(targetattr).indexOf(filename)!=-1)
			allsuspects[i].parentNode.removeChild(allsuspects[i]);
	}
}

function switchtheme(){
	if ( theme == 0 ) {
		loadcssfile("../css/Dark.css");
		theme = 1;
	} else {
		removecssfile("../css/Dark.css");
		theme = 0;
	}
	document.getElementById("Theme").innerHTML = ( theme == 0 )? "Light Theme" : "Dark Theme";
	document.getElementById("Theme").title = ( theme == 0 )? "Click to use Dark Theme" : "Click to use Light Theme";

	var xhttp = new XMLHttpRequest();
	var link="http://" + window.location.hostname + "/cgi-bin/writetopcpconfig.cgi?THEME=" + ((theme == 0)? "Light" : "Dark")
	xhttp.open("GET", link, true);
	try {
		xhttp.send(null);
	} catch(err) {
		console.log (err);
	}
}

function setcurrenttheme( th ){
	theme = (th == "Light")? 0 : 1;
}

function setcurrentrepo( r ){
	repo = r;
}

function switchrepo(){
	if ( repo == 1 ){
		repo = 2;
	} else {
		repo = 1;
	}
	document.getElementById("Repo").innerHTML = ( repo == 1)? "pCP Main Repo" : "pCP Mirror Repo";
	document.getElementById("Repo").title = ( repo == 1)? "Click to use pCP Mirror Repo" : "Click to use pCP Main Repo";
	var xhttp = new XMLHttpRequest();
	var link="http://" + window.location.hostname + "/cgi-bin/writetopcpconfig.cgi?PCP_CUR_REPO=" + repo;
	xhttp.open("GET", link, true);
	try {
		xhttp.send(null);
	} catch(err) {
		console.log (err);
	}
}
