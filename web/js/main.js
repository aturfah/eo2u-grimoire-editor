eel.expose(prompt_alerts);
function prompt_alerts(description) {
  alert(description);
}

// Set the elements in the grimoire dropdown list
async function setGrimoireDropdown() {
  let grimoireList = await eel.get_grimoire_dropdown_options()()

  const grimoireDropdown = document.getElementById("grimoire-dropdown");

  // In case we're re-calling this, delete
  while(grimoireDropdown.firstChild) {
    grimoireDropdown.removeChild(grimoireDropdown.firstChild)
  }

  // Fill the children
  grimoireList.forEach((name, idx) => {
    let opt = document.createElement("option");
    opt.value = idx;
    opt.innerHTML = name;
    grimoireDropdown.appendChild(opt);
  });

  // Set the value correctly
  grimoireDropdown.value = await eel.get_chosen_grimoire_idx()();
}

// Set the elements in the skill selection dropdown
async function setSkillNameDropdown() {
  let skillList = await eel.get_skill_names()()

  skillList.forEach(val => {
    const opt = document.createElement("option");
    opt.value = val;
    opt.innerHTML = val;
    document.getElementById("skill-name").appendChild(opt);
  });
}

// Set the elements in the grimoire bonus dropdown
async function setGrimoireBonusDropdown() {
  let bonusList = await eel.get_bonus_types()()

  bonusList.forEach(val => {
    const opt = document.createElement("option");
    opt.value = val;
    opt.innerHTML = val;
    document.getElementById("bonus-type").appendChild(opt);
  });
}

// Render the chosen Grimoire
async function renderChosenGrimoire() {
  const grimoireDatum = await eel.get_chosen_grimoire()()

  // Set the skill name
  let skillNameSelect = document.getElementById("skill-name");
  skillNameSelect.value = grimoireDatum["skill_name"];

  // Set the grimire level
  let skillLevelSelect = document.getElementById("skill-level")
  skillLevelSelect.value = String(grimoireDatum["skill_level"]);
  
  // Set the bonus type
  let bonusTypeSelect = document.getElementById("bonus-type");
  bonusTypeSelect.value = grimoireDatum["bonus_type"];

  // Set the bonus type level
  let bonusLevelSelect = document.getElementById("bonus-level")
  bonusLevelSelect.value = String(grimoireDatum["bonus_level"]);
}

// When the grimoire dropdown is changed, update the python class
async function grimoireSelectCallback() {
  const newIdx = document.getElementById("grimoire-dropdown").value;
  await eel.update_chosen_grimoire(newIdx)();
  
  // Update the panel
  renderChosenGrimoire();
}


// When the skill select dropdown is changed, update the python class
async function skillSelectCallback() {
  const newSkill = document.getElementById("skill-name").value;
  await eel.update_grimoire_skill(newSkill)();

  // Update the panel
  setGrimoireDropdown();
  renderChosenGrimoire();
}

// When the skill level is changed, update the python class
async function skillLevelCallback() {
  const newLevel = document.getElementById("skill-level").value;
  await eel.update_grimoire_skill_level(newLevel);

  // Update the panel
  setGrimoireDropdown();
  renderChosenGrimoire();
}

async function bonusTypeCallback() {
  const newBonus = document.getElementById("bonus-type").value;
  await eel.update_grimoire_bonus_type(newBonus);

  // Update the panel
  setGrimoireDropdown();
  renderChosenGrimoire();
}


async function bonusLevelCallback() {
  const newLevel = document.getElementById("bonus-level").value;
  await eel.update_grimoire_bonus_level(newLevel);

  // Update the panel
  setGrimoireDropdown();
  renderChosenGrimoire();
}


// Load the file from disk and prepare UI
async function loadMethod() {
  const success = await eel.load_file()();

  if (success === false) {
    return;
  }

  // Get everything prepared
  setGrimoireDropdown();
  setSkillNameDropdown();
  setGrimoireBonusDropdown();
  renderChosenGrimoire();

  // Reset/Save buttons are allowed
  document.getElementById("reset-button").removeAttribute("disabled")
  document.getElementById("save-button").removeAttribute("disabled")

  // Add functionality after load
  document.getElementById("save-button").addEventListener("click", ()=>{saveMethod()}, false);
  document.getElementById("reset-button").addEventListener("click", ()=>{resetMethod()}, false);
}

// Reset grimoire to original stats
async function resetMethod() {
  await eel.reset_grimoire()();

  // Update the panel
  setGrimoireDropdown();
  renderChosenGrimoire();
}

// Save file
async function saveMethod() {
  await eel.save_file()();

  // Update the panel
  setGrimoireDropdown();
  renderChosenGrimoire();
}


// Assign functionality to buttons
document.getElementById("load-button").addEventListener("click", ()=>{loadMethod()}, false);