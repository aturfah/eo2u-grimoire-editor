eel.expose(prompt_alerts);
function prompt_alerts(description) {
  alert(description);
}

// Set the elements in the dropdown list
eel.expose(setGrimoireDropdown)
function setGrimoireDropdown(grimoireList) {
  const grimoireDropdown = document.getElementById("grimoire-dropdown");

  grimoireList.forEach((name, idx) => {
    let opt = document.createElement("option");
    opt.value = idx;
    opt.innerHTML = name;
    grimoireDropdown.appendChild(opt);
  })
}

// Load the file from disk
function loadMethod() {
  eel.load_file();
  setGrimoireDropdown();
}

// Assign functionality to buttons
document.getElementById("load-button").addEventListener("click", ()=>{loadMethod()}, false);
document.getElementById("save-button").addEventListener("click", ()=>{eel.get_date()}, false);
