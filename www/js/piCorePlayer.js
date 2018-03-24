function pcp_confirm(prompt,goto) {
	var answer = confirm(prompt)
	if (answer) window.location = goto;
}

function more(elementID) {
	var sel1 = document.getElementById(elementID);
	sel1.className = (sel1.className == 'less') ? 'more' : 'less';
	var sel2 = document.getElementById(elementID + "a");
	sel2.text = (sel2.text == 'less>') ? 'more>' : 'less>';
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

