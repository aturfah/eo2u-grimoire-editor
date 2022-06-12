function loadMethod() {
  eel.load_file()
  setGrimoireDropdown()
}

document.getElementById("load-button").addEventListener("click", ()=>{loadMethod()}, false);
document.getElementById("save-button").addEventListener("click", ()=>{eel.get_date()}, false);


eel.expose(prompt_alerts);
function prompt_alerts(description) {
  alert(description);
}

eel.expose(setGrimoireDropdown)
function setGrimoireDropdown(grimoireList) {
  // console.log(grimoireList)
  const grimoireDropdown = document.getElementById("grimoire-dropdown")

  grimoireList.forEach((name, idx) => {
    console.log(idx, name)
    let opt = document.createElement("option");
    opt.value = idx;
    opt.innerHTML = name;
    grimoireDropdown.appendChild(opt);
  })
}