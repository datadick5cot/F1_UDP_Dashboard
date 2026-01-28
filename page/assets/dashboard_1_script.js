// ===============================
// Telemetry Dashboard Script
// ===============================

// ===============================
// Global State
// ===============================
// Shared telemetry snapshot
let telemetryState = {};

// Cache last values to prevent flicker and unnecessary DOM updates
const lastTelemetry = {
  tyrewear: [null, null, null, null],
  tyreinnertemp: [null, null, null, null],
  tyresurfacetemp: [null, null, null, null],
  braketemp: [null, null, null, null],
  slipangle: [null, null, null, null],
  drs: null,
  drsActive: null, // Ensure this is initialized
  brakebias: null,
  batteryFill: null,
  fuelremaining: null,
  m_gear: null,
  m_throttlePercent: null,
  m_brakePercent: null,
  m_revLightsPercent: null,
  eventCode: null,
  starterLights: 0,
  pitStopRejoinPosition: null,
  ersDeployMode: null,
};


// ===============================
// Fetch Telemetry & Trigger Render
// ===============================
async function fetchAndRender() {
  try {
    const res = await fetch("http://localhost:8000/telemetry");
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    const data = await res.json();
    telemetryState = data;
    renderFromState(); // Render the new state
  } catch (err) {
    console.error("Failed to fetch or render telemetry:", err);
  }
}

// ===============================
// DOM Update Helpers
// ===============================
function updateText(elementId, value, unit = "") {
  const element = document.getElementById(elementId);
  if (element && value !== null && value !== undefined) {
    const text = `${value}${unit}`;
    if (element.textContent !== text) {
      element.textContent = text;
    }
  }
}

// ===============================
// Render From State (decoupled)
// ===============================
function renderFromState() {
  console.log("Current telemetryState:", telemetryState); // Log the entire telemetry state
  if (!telemetryState || Object.keys(telemetryState).length === 0) return;

  // ===============================
  //  Gear Cylinder
  // ===============================
  const gearMap = { "R": 0, "N": 1, "1": 2, "2": 3, "3": 4, "4": 5, "5": 6, "6": 7, "7": 8, "8": 9 };
  const gear = telemetryState.m_gear ?? "N";
  if (gear !== lastTelemetry.m_gear) {
    const gearIndex = gearMap[gear];
    if (gearIndex !== undefined) {
      rotateWheel(gearIndex);
      lastTelemetry.m_gear = gear;
    }
  }

  // ===============================
  // Throttle & Brake
  // ===============================
  const throttlePercent = telemetryState.m_throttle != null ? Math.round(telemetryState.m_throttle * 100) : 0;
  if (throttlePercent !== lastTelemetry.m_throttlePercent) {
    updateText("throttle_div", throttlePercent, "%");
    lastTelemetry.m_throttlePercent = throttlePercent;
  }

  const brakePercent = telemetryState.m_brake != null ? Math.round(telemetryState.m_brake * 100) : 0;
   if (brakePercent !== lastTelemetry.m_brakePercent) {
    updateText("brake_div", brakePercent, "%");
    lastTelemetry.m_brakePercent = brakePercent;
  }

  // ===============================
  // Rev, Start Lights, Alerts
  // ===============================
  const revLightsPercent = telemetryState.m_revLightsPercent ?? 0;
  if (revLightsPercent !== lastTelemetry.m_revLightsPercent) {
    renderRpmLights(revLightsPercent);
    lastTelemetry.m_revLightsPercent = revLightsPercent;
  }
  
  const numLights = telemetryState.m_eventDetails?.StartLights?.numLights ?? 0;
  if (numLights !== lastTelemetry.starterLights) {
    starterlights(numLights);
    lastTelemetry.starterLights = numLights;
  }

  const eventCode = telemetryState.m_eventStringCode;
  if (eventCode && eventCode !== lastTelemetry.eventCode) {
    renderAlertBar([eventCode]);
    lastTelemetry.eventCode = eventCode;
  }

  // ===============================
  // ERS, DRS, Brake Bias, etc.
  // ===============================
  const drsAllowed = telemetryState.m_drsAllowed ?? 0;
  const drsActive = telemetryState.m_drs ?? 0;

  if (drsAllowed !== lastTelemetry.drs || drsActive !== lastTelemetry.drsActive) {
    console.log(`DRS State Change Detected: Allowed=${drsAllowed}, Active=${drsActive}`);
    let drsText = "";
    let drsColor = "";

    if (drsAllowed === 0) {
      drsText = "Not Allowed";
      drsColor = "#808080"; // Grey
    } else {
      if (drsActive === 1) {
        drsText = "DRS ACTIVE";
        drsColor = "#00FF00"; // Green
      } else {
        drsText = "Allowed";
        drsColor = "#FFFFFF"; // White
      }
    }

      const drsElement = document.getElementById("drs_div");
      if (drsElement) {                                                           
        drsElement.textContent = drsText;                                         
        drsElement.style.color = drsColor;                                        
        } else {  console.error("DRS element with ID 'drs_div' not found.");                
         }                                                                           
         lastTelemetry.drs = drsAllowed;                                             
         lastTelemetry.drsActive = drsActive;  

  }
  
  const brakeBias = telemetryState.m_brakeBias ?? 50;
  if (brakeBias !== lastTelemetry.brakebias) {
      updateText("metricC", brakeBias, "%");
      lastTelemetry.brakebias = brakeBias;
  }

  const ersDeployMode = telemetryState.m_ersDeployMode ?? 0;
  if (ersDeployMode !== lastTelemetry.ersDeployMode) {
    const ersMap = { 0: "None", 1: "Medium", 2: "Hotlap", 3: "Overtake" };
    const ersdeploy = document.querySelector('.ers-Deploy-Mode');
    if(ersdeploy) ersdeploy.textContent = ersMap[ersDeployMode] || "---";
    lastTelemetry.ersDeployMode = ersDeployMode;
  }

  const ersStoreEnergy = telemetryState.m_ersStoreEnergy ?? 0;
  const MAX_ERS = 4000000;
  const ersPercent = Math.max(0, Math.min(100, (ersStoreEnergy / MAX_ERS) * 100));
  const batteryFill = document.querySelector('.battery-level');
  if (batteryFill && ersPercent !== lastTelemetry.batteryFill) {
      batteryFill.style.height = ersPercent + "%";
      if (ersPercent > 60) batteryFill.style.backgroundColor = "#00FF00";
      else if (ersPercent > 30) batteryFill.style.backgroundColor = "#FFD700";
      else batteryFill.style.backgroundColor = "#FF0000";
      lastTelemetry.batteryFill = ersPercent;
  }

  // ===============================
  // Other Metrics
  // ===============================
  // Note: 'metricD' is used for three different things in the HTML. This should be fixed.
  // For now, I'll just update one of them.
  const fuelRemaining = telemetryState.m_fuelRemainingLaps?.toFixed(1) ?? 0.0;
  if (fuelRemaining !== lastTelemetry.fuelremaining) {
      const fuelElements = document.querySelectorAll("#metricD"); // This will select all elements with this ID
      if(fuelElements.length > 2) {
        fuelElements[2].textContent = `${fuelRemaining} Laps`;
      }
      lastTelemetry.fuelremaining = fuelRemaining;
  }
  
  const tyresAge = telemetryState.m_tyresAgeLaps ?? 0;
  const tyresAgeElement = document.querySelectorAll("#metricD");
  if (tyresAgeElement.length > 0) {
      tyresAgeElement[0].textContent = `${tyresAge} Laps`;
  }
  
  const rejoinPosition = telemetryState.m_pitStopRejoinPosition ?? 0;
  const rejoinElement = document.querySelectorAll("#metricD");
  if (rejoinElement.length > 1) {
      rejoinElement[1].textContent = `P${rejoinPosition}`;
  }

  const slipAngleRL = telemetryState.m_wheelSlipAngle?.[0]?.toFixed(2) ?? '--';
  const slipAngleRR = telemetryState.m_wheelSlipAngle?.[1]?.toFixed(2) ?? '--';
  updateText("sliprl", slipAngleRL);
  updateText("sliprr", slipAngleRR);

}


// ===============================
//  Gear Cylinder
// ===============================
const gearCylinder = document.getElementById('gearCylinder');
const gearItems = gearCylinder.querySelectorAll('.gear-item');
const gearItemCount = gearItems.length;
const angleStep = 360 / gearItemCount;

// Position items around the Y-axis
gearItems.forEach((item, i) => {
  const angle = i * angleStep;
  item.style.transform = `translate(-50%, -50%) rotateY(${angle}deg) translateZ(100px)`;
});

function rotateWheel(index) {
  if (!gearCylinder) return;
  const rotation = -index * angleStep;
  gearCylinder.style.transform = `rotateY(${rotation}deg)`;
  // Update active highlight
  gearItems.forEach((item, i) => {
    item.classList.toggle('active', i === index);
  });
}

// ===============================
// Alert Bar
// ===============================
function renderAlertBar(eventCodeList) {
    const eventcodes = { 'SSTA': 'Session Started', 'SEND': 'Session Ended', 'FTLP': 'Fastest Lap', 'RTMT': 'Retirement', 'DRSE': 'DRS enabled', 'DRSD': 'DRS disabled', 'TMPT': 'Team mate in pits', 'CHQF': 'Chequered flag', 'RCWN': 'Race Winner', 'PENA': 'Penalty Issued', 'SPTP': 'Speed Trap Triggered', 'STLG': 'Start lights', 'LGOT': 'Lights out', 'DTSV': 'Drive through served', 'SGSV': 'Stop go served', 'FLBK': 'Flashback', 'BUTN': 'Button status', 'RDFL': 'Red Flag', 'OVTK': 'Overtake', 'SCAR': 'Safety Car', 'COLL': 'Collision' };
    const container = document.getElementById("alertBarContainer");

    eventCodeList.forEach(code => {
        if (!code || container.querySelector(`[data-code="${code}"]`)) return;
        const div = document.createElement("div");
        div.textContent = eventcodes[code] || "Unknown Event";
        div.style.padding = "10px";
        div.setAttribute("data-code", code);
        container.appendChild(div);
        setTimeout(() => div.remove(), 5000); // Remove after 5 seconds
    });
}

// ===============================
// RPM Lights
// ===============================
const rpmBar = document.getElementById("rpmBar");
const rpmLights = Array.from({ length: 15 }, () => {
  const light = document.createElement("div");
  light.className = "rpm-light";
  rpmBar.appendChild(light);
  return light;
});

function renderRpmLights(percent) {
  const activeLights = Math.min(15, Math.ceil(percent / (100 / 15)));
  rpmLights.forEach((light, i) => {
    let color;
    if (i < 5) color = i < activeLights ? '#00BFFF' : '#1E1E1E';
    else if (i < 10) color = i < activeLights ? '#FFA500' : '#1E1E1E';
    else color = i < activeLights ? '#FF0000' : '#1E1E1E';
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
  if(!panel) return;
  panel.style.display = count > 0 ? 'flex' : 'none';

  for (let i = 1; i <= 5; i++) {
    const light = document.getElementById(`starter-light-${i}`);
    if (light) {
        light.style.backgroundColor = i <= count ? 'red' : '#333';
    }
  }
}

// ===============================
// Loop Control
// ===============================
// Initial call to get data and render immediately
fetchAndRender(); 
// Then poll at a regular interval
setInterval(fetchAndRender, 100); // 10 Hz polling