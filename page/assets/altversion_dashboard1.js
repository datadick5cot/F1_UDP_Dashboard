// ===============================
// Global Telemetry State
// ===============================
let telemetryState = {};

const lastTelemetry = {
  m_gear: null,
  m_throttlePercent: null,
  m_brakePercent: null,
  starterLights: 0,
  m_revLightsPercent: null,
  eventCodeStr: null,
  ersEnergyPercent: null,
  ersDeployMode: null,
};


// ===============================
// Fetch Telemetry Data
// ===============================

async function fetchTelemetry() {
  try {
    const res = await fetch("http://localhost:8000/telemetry");
    telemetryState = await res.json();
  } catch (err) {
    console.error("Failed to fetch telemetry:", err);
  }
}


function renderFromState() {
  if (!telemetryState || Object.keys(telemetryState).length === 0) return;

  renderGear(telemetryState.m_gear);
  renderThrottle(telemetryState.m_throttle);
  renderBrake(telemetryState.m_brake);
  renderStarterLights(telemetryState.m_eventDetails?.numLights);
  renderRPM(telemetryState.m_revLightsPercent);
  renderEvents(telemetryState.m_eventStringCode);
  renderERSBattery(telemetryState.m_ersStoreEnergy);
  renderERSMode(telemetryState.m_ersDeployMode);
}


// ===============================
// Gears
// ===============================


const cylinder = document.getElementById('gearCylinder');
const items = cylinder ? cylinder.querySelectorAll('.gear-item') : [];
const itemCount = items.length || 1;
const angleStep = 360 / itemCount;


let currentIndex = 0;
let rotation = 0;

function updateActive() {
  items.forEach((item, i) => {
    item.classList.toggle('active', i === currentIndex);
  });
}

function rotateWheel() {
  if (!cylinder) return;

  rotation = -currentIndex * angleStep;
  cylinder.style.transform = `rotateY(${rotation}deg)`;
  updateActive();
}


const gearMap = {
  "R": 0,
  "N": 1,
  "1": 2,
  "2": 3,
  "3": 4,
  "4": 5,
  "5": 6,
  "6": 7,
  "7": 8,
  "8": 9
};

// Position items around the Y-axis
items.forEach((item, i) => {
  const angle = i * angleStep;
  // item.style.transform = `rotateY(${angle}deg) translateZ(100px)`;
  item.style.transform = `translate(-50%, -50%) rotateY(${angle}deg) translateZ(100px)`;

});


function renderGear(gear) {
  if (!gearMap.hasOwnProperty(gear)) return;
  if (gear === lastTelemetry.m_gear) return;

  currentIndex = gearMap[gear];
  rotateWheel();

  lastTelemetry.m_gear = gear;
}


// ===============================
// Throttle
// ===============================


function renderThrottle(value) {
  if (value == null) return;

  const percent = Math.round(value * 100);
  if (percent === lastTelemetry.m_throttlePercent) return;

  document.getElementById("throttle_div").textContent = `${percent}%`;
  lastTelemetry.m_throttlePercent = percent;
}

// ===============================
// Brake
// ===============================


function renderBrake(value) {
  if (value == null) return;

  const percent = Math.round(value * 100);
  if (percent === lastTelemetry.m_brakePercent) return;

  document.getElementById("brake_div").textContent = `${percent}%`;
  lastTelemetry.m_brakePercent = percent;
}

// ===============================
// Starter Lights
// ===============================



function starterlights(count) {
  const panel = document.getElementById("starterlightsPanel");
  if (!panel) return;

  panel.classList.toggle("starterlights_panel-on", count > 0);
  panel.classList.toggle("starterlights_panel-off", count === 0);

  for (let i = 1; i <= 5; i++) {
    const light = document.getElementById(`starter-light-${i}`);
    if (!light) continue;

    light.classList.toggle("on", i <= count);
    light.setAttribute("aria-checked", i <= count ? "true" : "false");
  }
}


function renderStarterLights(count = 0) {
  if (count === lastTelemetry.starterLights) return;

  starterlights(count);
  lastTelemetry.starterLights = count;
}
// ===============================
// RPM Lights
// ===============================

// ===============================
// RPM Lights Setup
// ===============================
const rpmBar = document.getElementById("rpmBar");
const rpmLights = [];

if (rpmBar) {
  for (let i = 0; i < 15; i++) {
    const light = document.createElement("div");
    light.className = "rpm-light";
    rpmBar.appendChild(light);
    rpmLights.push(light);
  }
}



function renderRpmLights(percent) {
  const activeLights = Math.min(15, Math.ceil(percent / (100 / 15)));

  rpmLights.forEach((light, i) => {
    let color;
    if (i < 5) color = i < activeLights ? '#00BFFF' : '#1E1E1E'; // Blue
    else if (i < 10) color = i < activeLights ? '#FFA500' : '#1E1E1E'; // Amber
    else color = i < activeLights ? '#FF0000' : '#1E1E1E'; // Red

    if (light.style.backgroundColor !== color) {
      light.style.backgroundColor = color;
    }
  });
}


function renderRPM(percent) {
  if (percent == null) return;
  if (percent === lastTelemetry.m_revLightsPercent) return;

  renderRpmLights(percent);
  lastTelemetry.m_revLightsPercent = percent;
}

// ===============================
// Event Notifications
// ===============================


// ===============================
// Alert Bar
// ===============================
function renderAlertBar(eventCodeList) {
  const eventcodes = {
    'SSTA': 'Session Started',
    'SEND': 'Session Ended',
    'FTLP': 'Fastest Lap',
    'RTMT': 'Retirement',
    'DRSE': 'DRS enabled',
    'DRSD': 'DRS disabled',
    'TMPT': 'Team mate in pits',
    'CHQF': 'Chequered flag',
    'RCWN': 'Race Winner',
    'PENA': 'Penalty Issued',
    'SPTP': 'Speed Trap Triggered',
    'STLG': 'Start lights',
    'LGOT': 'Lights out',
    'DTSV': 'Drive through served',
    'SGSV': 'Stop go served',
    'FLBK': 'Flashback',
    'BUTN': 'Button status',
    'RDFL': 'Red Flag',
    'OVTK': 'Overtake',
    'SCAR': 'Safety Car',
    'COLL': 'Collision'
  };

  const eventcolours = {
    'SSTA': '#00FF00',
    'SEND': '#808080',
    'FTLP': '#800080',
    'RTMT': '#FF0000',
    'DRSE': '#0000FF',
    'DRSD': '#FFA500',
    'TMPT': '#000000',
    'CHQF': '#CCCCCC',
    'RCWN': '#CCCCCC',
    'PENA': '#FF0000',
    'SPTP': '#FFD700',
    'STLG': '#00FF00',
    'LGOT': '#00FF00',
    'DTSV': '#00FF00',
    'SGSV': '#00FF00',
    'FLBK': '#0000FF',
    'BUTN': '#000000',
    'RDFL': '#FF0000',
    'OVTK': '#00FF00',
    'SCAR': '#FFA500',
    'COLL': '#FF0000'
  };

// Utility to determine readable text color
function getTextColor(bgColor) {
  const r = parseInt(bgColor.substr(1, 2), 16);
  const g = parseInt(bgColor.substr(3, 2), 16);
  const b = parseInt(bgColor.substr(5, 2), 16);
  const brightness = (r * 299 + g * 587 + b * 114) / 1000;
  return brightness > 125 ? "#000000" : "#FFFFFF";
}


  const container = document.getElementById("alertBarContainer");

  eventCodeList.forEach(code => {
    if (!code) return;

    // Avoid duplicates
    if (!container.querySelector(`[data-code="${code}"]`)) {
      const text = eventcodes[code] || "";
      const bgColor = eventcolours[code] || "#444";
      const textColor = getTextColor(bgColor);

      const div = document.createElement("div");
      div.textContent = text;
      div.style.backgroundColor = bgColor;
      div.style.color = textColor;
      div.style.padding = "10px";
      div.style.margin = "5px";
      div.style.borderRadius = "5px";
      div.style.fontWeight = "bold";
      div.style.textAlign = "center";
      div.setAttribute("data-code", code);

      container.appendChild(div);
    }
  });
}

function renderEvents(codes) {
  if (!codes) return;

  const list = Array.isArray(codes) ? codes : [codes];
  const codeStr = list.join(",");

  if (codeStr === lastTelemetry.eventCodeStr) return;

  renderAlertBar(list);
  lastTelemetry.eventCodeStr = codeStr;
}

// ===============================
// ERS
// ===============================

// ERS Battery
const MAX_ERS = 4000000;

function renderERSBattery(joules) {
  if (joules == null) return;

  const percent = Math.round((joules / MAX_ERS) * 100);
  if (percent === lastTelemetry.ersEnergyPercent) return;

  const fill = document.querySelector(".battery-level");
  if (!fill) return;

  fill.style.height = `${percent}%`;
  fill.style.backgroundColor =
    percent > 60 ? "#00FF00" :
    percent > 30 ? "#FFD700" :
    "#FF0000";

  lastTelemetry.ersEnergyPercent = percent;
}

// ERS Mode

const ersMap = {
  0: { label: "None",     color: "#ffffff" },
  1: { label: "Medium",   color: "#ddbe50" },
  2: { label: "Hotlap",   color: "#e24927" },
  3: { label: "Overtake", color: "#a40808" },
};

function renderERSMode(modeNumber = 0) {
  if (modeNumber === lastTelemetry.ersDeployMode) return;

  const el = document.querySelector(".ers-Deploy-Mode");
  if (!el) return;

  const mode = ersMap[modeNumber] ?? { label: "Unknown", color: "#fff" };

  el.textContent = mode.label;
  el.style.color = mode.color;

  lastTelemetry.ersDeployMode = modeNumber;
}



// Loop

setInterval(fetchTelemetry, 100);    // 10 Hz
setInterval(renderFromState, 250);  // 4 Hz
