eel.expose(prompt_alerts);
function prompt_alerts(description) {
  alert(description);
}

// Set the elements in the grimoire dropdown list
async function setGrimoireDropdown() {
  let grimoireList = await eel.get_grimoire_dropdown_options()()

  const grimoireDropdown = document.getElementById("grimoire-dropdown");
  grimoireList.forEach((name, idx) => {
    let opt = document.createElement("option");
    opt.value = idx;
    opt.innerHTML = name;
    grimoireDropdown.appendChild(opt);
  })
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


// Load the file from disk
function loadMethod() {
  // Review this: https://github.com/ChrisKnott/Eel#return-values
  new Promise((resolve, reject) => {
    console.log('Load File');
    eel.load_file();
    resolve();
  })
  .then(() => {
    console.log("Prepare UI")
    setGrimoireDropdown();
    setSkillNameDropdown();
    setGrimoireBonusDropdown();
    renderChosenGrimoire();
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
      // Change Event
      const skillNameSelect = document.getElementById("skill-name")
      console.log(skillNameSelect.value);
      const bonusTypeSelect = document.getElementById("bonus-type");
      console.log(bonusTypeSelect.value);
  });
}

// Assign functionality to buttons
document.getElementById("load-button").addEventListener("click", ()=>{loadMethod()}, false);
document.getElementById("save-button").addEventListener("click", ()=>{eel.get_date()}, false);
