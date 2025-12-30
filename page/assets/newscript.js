// ===============================
// Telemetry Dashboard Script
// ===============================

// Shared telemetry snapshot
let telemetryState = null;

// ===============================
// DEBUG OVERLAY
// ===============================
const debugOverlay = document.getElementById("debugOverlay");

function debugLog(label, value, level = "info") {
  if (!debugOverlay) return;

  const line = document.createElement("div");
  const ts = new Date().toLocaleTimeString();

  line.textContent =
    `[${ts}] ${label}: ${typeof value === "object"
      ? JSON.stringify(value).slice(0, 120)
      : value}`;

  if (level === "error") line.className = "error";
  if (level === "warn") line.className = "warn";

  debugOverlay.prepend(line);

  // Limit lines
  while (debugOverlay.children.length > 25) {
    debugOverlay.removeChild(debugOverlay.lastChild);
  }
}

debugLog("JS", "loaded"); 


async function fetchTelemetry() {
  debugLog("Fetch", "tick");
  try {
    const res = await fetch("http://localhost:8000/telemetry");
    telemetryState = await res.json();
    debugLog("Telemetry", telemetryState);
  } catch (err) {
    debugLog("Fetch error", err.message, "error");
  }
}


debugLog("Fetch", "tick");

debugLog("Render", telemetryState ? "active" : "waiting");


// Cache last values to prevent flicker
const lastTelemetry = {
  tyrewear: [null, null, null, null],
  tyreinnertemp: [null, null, null, null],
  tyresurfacetemp: [null, null, null, null],
  braketemp: [null, null, null, null],
  slipsngle: [null, null, null, null],
  drs: null,
  brakebias: null,
  batteryFill: null,
  fuelremaining: null,
  gear: null,
  throttle: null,
  brake: null,
  rpm: null,
  eventCode: null,
  starterLights: 0,
  pitStopRejoinPosition: null,
  ersDeployMode: null
};



// ===============================
// Gear display (UNCHANGED LOGIC)
// ===============================
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

const cylinder = document.getElementById("gearCylinder");
const items = cylinder.querySelectorAll(".gear-item");
const itemCount = items.length;
const angleStep = 360 / itemCount;

let currentIndex = 3;
let rotation = 0;

items.forEach((item, i) => {
  const angle = i * angleStep;
  item.style.transform =
    `translate(-50%, -50%) rotateY(${angle}deg) translateZ(100px)`;
});

function updateActive() {
  items.forEach((item, i) =>
    item.classList.toggle("active", i === currentIndex)
  );
}

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
    SSTA: "Session Started",
    SEND: "Session Ended",
    FTLP: "Fastest Lap",
    RTMT: "Retirement",
    DRSE: "DRS enabled",
    DRSD: "DRS disabled",
    TMPT: "Team mate in pits",
    CHQF: "Chequered flag",
    RCWN: "Race Winner",
    PENA: "Penalty Issued",
    SPTP: "Speed Trap Triggered",
    STLG: "Start lights",
    LGOT: "Lights out",
    DTSV: "Drive through served",
    SGSV: "Stop go served",
    FLBK: "Flashback",
    BUTN: "Button status",
    RDFL: "Red Flag",
    OVTK: "Overtake",
    SCAR: "Safety Car",
    COLL: "Collision"
  };

  const eventcolours = {
    SSTA: "#00FF00",
    SEND: "#808080",
    FTLP: "#800080",
    RTMT: "#FF0000",
    DRSE: "#0000FF",
    DRSD: "#FFA500",
    TMPT: "#000000",
    CHQF: "#CCCCCC",
    RCWN: "#CCCCCC",
    PENA: "#FF0000",
    SPTP: "#FFD700",
    STLG: "#00FF00",
    LGOT: "#00FF00",
    DTSV: "#00FF00",
    SGSV: "#00FF00",
    FLBK: "#0000FF",
    BUTN: "#000000",
    RDFL: "#FF0000",
    OVTK: "#00FF00",
    SCAR: "#FFA500",
    COLL: "#FF0000"
  };

  const container = document.getElementById("alertBarContainer");
  if (!container) return;

  eventCodeList.forEach(code => {
    if (!code) return;
    if (container.querySelector(`[data-code="${code}"]`)) return;

    const div = document.createElement("div");
    const bg = eventcolours[code] || "#444";

    div.textContent = eventcodes[code] || "";
    div.style.backgroundColor = bg;
    div.style.color = getTextColor(bg);
    div.style.padding = "10px";
    div.style.margin = "5px";
    div.style.borderRadius = "5px";
    div.style.fontWeight = "bold";
    div.style.textAlign = "center";
    div.dataset.code = code;

    container.appendChild(div);
  });
}

function getTextColor(bgColor) {
  const r = parseInt(bgColor.substr(1, 2), 16);
  const g = parseInt(bgColor.substr(3, 2), 16);
  const b = parseInt(bgColor.substr(5, 2), 16);
  return (r * 299 + g * 587 + b * 114) / 1000 > 125
    ? "#000000"
    : "#FFFFFF";
}

// ===============================
// RPM Lights
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
  const active = Math.min(15, Math.ceil(percent / (100 / 15)));
  rpmLights.forEach((light, i) => {
    let color = "#1E1E1E";
    if (i < active) {
      color = i < 5 ? "#00BFFF" : i < 10 ? "#FFA500" : "#FF0000";
    }
    light.style.backgroundColor = color;
  });
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
  }
}

// ===============================
// Fetch Telemetry
// ===============================
async function fetchTelemetry() {
  try {
    const res = await fetch("http://localhost:8000/telemetry");
    telemetryState = await res.json();
  } catch (err) {
    console.error("Telemetry fetch failed:", err);
  }
}

// ===============================
// Render From State
// ===============================
function renderFromState() {
  if (!telemetryState) return;

  // ---- Gear (unchanged logic) ----
  const gearValue = telemetryState.m_gear ?? lastTelemetry.gear ?? "0";
  if (gearMap.hasOwnProperty(gearValue)) {
    currentIndex = gearMap[gearValue];
    rotateWheel();
  }

  // Throttle
  if (telemetryState.m_throttle != null) {
    const v = Math.round(telemetryState.m_throttle * 100);
    if (v !== lastTelemetry.throttle) {
      document.getElementById("Throttle").textContent = `${v}%`;
      lastTelemetry.throttle = v;
    }
  }

  // Brake
  if (telemetryState.m_brake != null) {
    const v = Math.round(telemetryState.m_brake * 100);
    if (v !== lastTelemetry.brake) {
      document.getElementById("Brake").textContent = `${v}%`;
      lastTelemetry.brake = v;
    }
  }

  // Starter lights
  const lights = telemetryState.m_eventDetails?.numLights ?? 0;
  if (lights !== lastTelemetry.starterLights) {
    starterlights(lights);
    lastTelemetry.starterLights = lights;
  }

  // RPM
  if (telemetryState.m_revLightsPercent != null &&
      telemetryState.m_revLightsPercent !== lastTelemetry.rpm) {
    renderRpmLights(telemetryState.m_revLightsPercent);
    lastTelemetry.rpm = telemetryState.m_revLightsPercent;
  }

  // Events
  const codes = [].concat(telemetryState.m_eventStringCode || []);
  const codeStr = codes.join(",");
  if (codeStr && codeStr !== lastTelemetry.eventCode) {
    renderAlertBar(codes);
    lastTelemetry.eventCode = codeStr;
  }

  // ERS Battery
  if (telemetryState.m_ersStoreEnergy != null) {
    const percent = Math.min(
      100,
      Math.max(0, telemetryState.m_ersStoreEnergy / 4_000_000 * 100)
    );
    const fill = document.querySelector(".battery-level");
    if (fill) {
      fill.style.height = percent + "%";
      fill.style.backgroundColor =
        percent > 60 ? "#00FF00" :
        percent > 30 ? "#FFD700" : "#FF0000";
    }
  }

  // ERS Deploy Mode
  const ersMap = {
    0: { label: "None", color: "#ffffff" },
    1: { label: "Medium", color: "#ddbe50" },
    2: { label: "Hotlap", color: "#e24927" },
    3: { label: "Overtake", color: "#a40808" }
  };

  const modeNum =
    telemetryState.m_ersDeployMode ?? lastTelemetry.ersDeployMode ?? 0;

  if (modeNum !== lastTelemetry.ersDeployMode) {
    const el = document.querySelector(".ers-Deploy-Mode");
    const mode = ersMap[modeNum];
    if (el && mode) {
      el.textContent = mode.label;
      el.style.color = mode.color;
    }
    lastTelemetry.ersDeployMode = modeNum;
  }
}

// ===============================
// Loop Control
// ===============================
setInterval(fetchTelemetry, 100);
setInterval(renderFromState, 250);
