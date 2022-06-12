document.getElementById("load-button").addEventListener("click", ()=>{eel.get_random_number()}, false);
document.getElementById("save-button").addEventListener("click", ()=>{eel.get_date()}, false);


eel.expose(prompt_alerts);
function prompt_alerts(description) {
  alert(description);
}