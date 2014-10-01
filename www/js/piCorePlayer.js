function pcp_confirm(prompt,goto) {
	var answer = confirm(prompt)
	if (answer)	window.location = goto;
}

