function pcp_confirm(prompt,goto) {
	var answer = confirm(prompt)
	if (answer) window.location = goto;
}

function more(IDS) {
  var sel1 = document.getElementById(IDS);
  sel1.className = (sel1.className == 'less') ? 'more' : 'less';
  var sel2 = document.getElementById(IDS + "a");
  sel2.text = (sel2.text == 'less>') ? 'more>' : 'less>';
  return false;
}
