eel.expose(prompt_alerts);
function prompt_alerts(description) {
  alert(description);
}

// Set the elements in the grimoire dropdown list
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

// Set the elements in the skill selection dropdown
eel.expose(setSkillNameDropdown)
function setSkillNameDropdown(skillList) {
  skillList.forEach(val => {
    const opt = document.createElement("option");
    opt.value = val;
    opt.innerHTML = val;
    document.getElementById("skill-name").appendChild(opt);
  });
}

// Set the elements in the grimoire bonus dropdown
eel.expose(setGrimoireBonusDropdown)
function setGrimoireBonusDropdown(bonusList) {
  bonusList.forEach(val => {
    const opt = document.createElement("option");
    opt.value = val;
    opt.innerHTML = val;
    document.getElementById("bonus-type").appendChild(opt);
  });
}

// Set the bonus for the 

// Render the
eel.expose(renderChosenGrimoire)
function renderChosenGrimoire(grimoireDatum) {
  // Set the skill name
  const skillNameSelect = document.getElementById("skill-name")
  skillNameSelect.setAttribute("value", grimoireDatum["skill_name"]);
  skillNameSelect.dispatchEvent(new Event('change'));

  // Set the bonus type
  const bonusTypeSelect = document.getElementById("bonus-type")
  bonusTypeSelect.setAttribute("value", grimoireDatum["bonus_type"]);
  bonusTypeSelect.dispatchEvent(new Event('change'));
}


// Load the file from disk
function loadMethod() {
  new Promise((resolve, reject) => {
    console.log('Load File');
    eel.load_file()
    resolve();
  })
  .then(() => {
    console.log("Prepare UI")
    eel.prepare_ui();
  })
  .then(() => {
      console.log("Step #4")
      document.getElementById("reset-button").removeAttribute("disabled")
  })
  .catch(() => {
      console.error('Error');
  })
  .then(() => {
      console.log('Finished');
  });
}

// Assign functionality to buttons
document.getElementById("load-button").addEventListener("click", ()=>{loadMethod()}, false);
document.getElementById("save-button").addEventListener("click", ()=>{eel.get_date()}, false);
