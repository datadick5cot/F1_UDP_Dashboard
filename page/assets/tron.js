

async function fetchTelemetry() {
  try {
    const res = await fetch("http://localhost:8000/telemetry");
    const data = await res.json();

    document.getElementById("speed").textContent = data.m_speed ?? "--";
    document.getElementById("gear").textContent = data.m_gear ?? "--";

    const throttlePercent = Math.round((data.m_throttle ?? 0) * 100);
    const brakePercent = Math.round((data.m_brake ?? 0) * 100);

    document.getElementById("Throttle").textContent = `${throttlePercent}%`;
    document.getElementById("Brake").textContent = `${brakePercent}%`;
 
    const eventCode = data.m_eventStringCode;

    if (eventCode === "STLG" && data.m_eventDetails && typeof data.m_eventDetails.numLights === "number") {
      starterlights(data.m_eventDetails.numLights);
    } else {
      starterlights(0); // fallback or hide lights
    }

    const rpmPercent = data.m_revLightsPercent ?? 0;
    renderRpmLights(rpmPercent);

    const eventCodes = Array.isArray(data.m_eventStringCode)
      ? data.m_eventStringCode
      : [data.m_eventStringCode];


    const bsegments = document.querySelectorAll(`#${"brakeBar"} .bar-segment`);
    const btotal = bsegments.length;

    bsegments.forEach((seg, index) => {
      // Fill from the bottom: check against total - value
      if (index >= btotal - brakePercent) {
        seg.className = "bar-segment filled " + type;
      } else {
        seg.className = "bar-segment blankfilled";
      }
    });
      
    const tsegments = document.querySelectorAll(`#${"throttleBar"} .bar-segment`);
    const ttotal = tsegments.length;

    tsegments.forEach((seg, index) => {
      // Fill from the bottom: check against total - value
      if (index >= ttotal - throttlePercent) {
        seg.className = "bar-segment filled " + type;
      } else {
        seg.className = "bar-segment blankfilled";
      }
    });



    renderAlertBar(eventCodes);
  } catch (err) {
    console.error("Failed to fetch telemetry:", err);
  }
}

  setInterval(fetchTelemetry, 100); // Poll every 100ms



// Create 100 segments
const brakeBar = document.getElementById("brakeBar");
for (let i = 0; i < 100; i++) {
  const segment = document.createElement("div");
  segment.classList.add("bar-segment", "blankfilled"); // default state
  brakeBar.appendChild(segment);
}

// Utility to build a bar container with N segments
function buildBar(containerId, segments = 100) {
  const container = document.getElementById(containerId);
  container.innerHTML = ""; // clear any existing
  for (let i = 0; i < segments; i++) {
    const segment = document.createElement("div");
    segment.classList.add("bar-segment", "blankfilled"); // default state
    container.appendChild(segment);
  }
}



function updateBar(containerId, value, type) {
  const segments = document.querySelectorAll(`#${containerId} .bar-segment`);
  const total = segments.length;

  segments.forEach((seg, index) => {
    // Fill from the bottom: check against total - value
    if (index >= total - value) {
      seg.className = "bar-segment filled " + type;
    } else {
      seg.className = "bar-segment blankfilled";
    }
  });
}


// Build both bars once
buildBar("brakeBar", 100);
buildBar("throttleBar", 100);


// Example usage
updateBar("brakeBar", 30, "brake");     // 30% brake applied
updateBar("throttleBar", 65, "accel");  // 65% throttle applied