// ===============================
// Telemetry Dashboard Script
// ===============================

// Cache last values to prevent flicker
const lastTelemetry = {tyrewear : [null, null, null, null],
                      tyreinnertemp : [null, null, null, null],
                      tyresurfacetemp : [null, null, null, null],
                      braketemp : [null, null, null, null],
                      slipsngle: [null, null, null, null],
                      drs : null,
                      brakebias: null,
                      batteryFill: null,
                      fuelremaining : null,
                      gear: null,
                      throttle: null,
                      brake: null,
                      rpm: null,
                      eventCode: null,
                      starterLights: 0,
                      pitStopRejoinPosition : null,
                      };

// Shared telemetry snapshot
let telemetryState = null;

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


const cylinder = document.getElementById('gearCylinder');
const items = cylinder.querySelectorAll('.gear-item');
const itemCount = items.length;
const angleStep = 360 / itemCount;
let currentIndex = 3; // start at "4"
let rotation = 0;

// Position items around the Y-axis
items.forEach((item, i) => {
  const angle = i * angleStep;
  // item.style.transform = `rotateY(${angle}deg) translateZ(100px)`;
  item.style.transform = `translate(-50%, -50%) rotateY(${angle}deg) translateZ(100px)`;

});

// Update active highlight
function updateActive() {
  items.forEach((item, i) => {
    item.classList.toggle('active', i === currentIndex);
  });
}

// Rotate cylinder so active item is centered
function rotateWheel() {
  rotation = -currentIndex * angleStep;
  cylinder.style.transform = `rotateY(${rotation}deg)`;
  updateActive();
}




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

// Utility to determine readable text color
function getTextColor(bgColor) {
  const r = parseInt(bgColor.substr(1, 2), 16);
  const g = parseInt(bgColor.substr(3, 2), 16);
  const b = parseInt(bgColor.substr(5, 2), 16);
  const brightness = (r * 299 + g * 587 + b * 114) / 1000;
  return brightness > 125 ? "#000000" : "#FFFFFF";
}

// ===============================
// RPM Lights (pre-created)
// ===============================
const rpmBar = document.getElementById("rpmBar");
const rpmLights = [];

for (let i = 0; i < 15; i++) {
  const light = document.createElement("div");
  light.className = "rpm-light";
  rpmBar.appendChild(light);
  rpmLights.push(light);
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

// ===============================
// Starter Lights
// ===============================
function starterlights(count) {
  const panel = document.getElementById("starterlightsPanel");

  if (count > 0) {
    panel.classList.remove("starterlights_panel-off");
    panel.classList.add("starterlights_panel-on");
  } else {
    panel.classList.remove("starterlights_panel-on");
    panel.classList.add("starterlights_panel-off");
  }

  for (let i = 1; i <= 5; i++) {
    const light = document.getElementById(`starter-light-${i}`);
    if (light) {
      if (i <= count) {
        light.classList.add("on");
        light.setAttribute("aria-checked", "true");
      } else {
        light.classList.remove("on");
        light.setAttribute("aria-checked", "false");
      }
    }
  }
}

// ===============================
// Fetch Telemetry (polling only)
// ===============================
async function fetchTelemetry() {
  try {
    const res = await fetch("http://localhost:8000/telemetry");
    const data = await res.json();
    telemetryState = data;
  } catch (err) {
    console.error("Failed to fetch telemetry:", err);
  }
}





// ===============================
// Render From State (decoupled)
// ===============================
function renderFromState() {
  if (!telemetryState) return;


  // tyrewear
  // tyreinnertemp
  // tyresurfacetemp
  // braketemp
  // slipsngle
  // drs
  // brakebias
  // fuelremaining


  // Gear
  const gearValue = telemetryState.m_gear ?? lastTelemetry.gear ?? "0";
        if (gearMap.hasOwnProperty(gearValue)) {
        currentIndex = gearMap[gearValue];
        rotateWheel();
        }

  // Throttle
  const throttlePercent = telemetryState.m_throttle != null ? Math.round(telemetryState.m_throttle * 100) : null;
  if (throttlePercent != null && throttlePercent !== lastTelemetry.throttle) {
    document.getElementById("Throttle").textContent = `${throttlePercent}%`;
    lastTelemetry.throttle = throttlePercent;
  }

  // Brake
  const brakePercent = telemetryState.m_brake != null ? Math.round(telemetryState.m_brake * 100) : null;
  if (brakePercent != null && brakePercent !== lastTelemetry.brake) {
    document.getElementById("Brake").textContent = `${brakePercent}%`;
    lastTelemetry.brake = brakePercent;
  }

  // Starter lights – prevent unnecessary toggles
  const numLights = telemetryState.m_eventDetails?.numLights ?? 0;
  if (numLights !== lastTelemetry.starterLights) {
    starterlights(numLights);
    lastTelemetry.starterLights = numLights;
  }

  // RPM lights
  if (telemetryState.m_revLightsPercent != null && telemetryState.m_revLightsPercent !== lastTelemetry.rpm) {
    renderRpmLights(telemetryState.m_revLightsPercent);
    lastTelemetry.rpm = telemetryState.m_revLightsPercent;
  }

  // Event codes
  const eventCodes = Array.isArray(telemetryState.m_eventStringCode)
    ? telemetryState.m_eventStringCode
    : [telemetryState.m_eventStringCode];

  const eventCodeStr = eventCodes.filter(c => c != null).join(",");
  if (eventCodeStr && eventCodeStr !== lastTelemetry.eventCode) {
    renderAlertBar(eventCodes);
    lastTelemetry.eventCode = eventCodeStr;
  }


  
const MAX_ERS = 4000000;

// ERS Battery
if (telemetryState.m_ersStoreEnergy != null) {
  const joules = telemetryState.m_ersStoreEnergy;
  const percent = Math.max(0, Math.min(100, (joules / MAX_ERS) * 100));

  const batteryFill = document.querySelector('.battery-level');
  if (!batteryFill) return;

  batteryFill.style.height = percent + "%";

  if (percent > 60) {
    batteryFill.style.backgroundColor = "#00FF00";
  } else if (percent > 30) {
    batteryFill.style.backgroundColor = "#FFD700";
  } else {
    batteryFill.style.backgroundColor = "#FF0000";
  }
}

}

// ===============================
// Loop Control
// ===============================
setInterval(fetchTelemetry, 100);   // 10 Hz polling
setInterval(renderFromState, 250); // 4 Hz rendering
