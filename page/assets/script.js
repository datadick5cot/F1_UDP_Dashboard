
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
  container.innerHTML = ""; // Clear previous alerts

  eventCodeList.forEach(code => {
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

    container.appendChild(div);



    
  });
}

// Utility to determine readable text color
function getTextColor(bgColor) {
  // Convert hex to RGB
  const r = parseInt(bgColor.substr(1, 2), 16);
  const g = parseInt(bgColor.substr(3, 2), 16);
  const b = parseInt(bgColor.substr(5, 2), 16);
  const brightness = (r * 299 + g * 587 + b * 114) / 1000;
  return brightness > 125 ? "#000000" : "#FFFFFF";
}


  function renderRpmLights(percent) {
    const rpmBar = document.getElementById("rpmBar");
    rpmBar.innerHTML = "";

    const activeLights = Math.min(15, Math.ceil(percent / (100 / 15)));

    for (let i = 1; i <= 15; i++) {
      let color;
      if (i <= 5) {
        color = i <= activeLights ? '#00BFFF' : '#1E1E1E'; // Blue
      } else if (i <= 10) {
        color = i <= activeLights ? '#FFA500' : '#1E1E1E'; // Amber
      } else {
        color = i <= activeLights ? '#FF0000' : '#1E1E1E'; // Red
      }

      const light = document.createElement("div");
      light.className = "rpm-light";
      light.style.backgroundColor = color;
      rpmBar.appendChild(light);
    }
  }



function starterlights(count) {
  const panel = document.getElementById("starterlightsPanel");

  // Toggle panel visibility
  if (count > 0) {
    panel.classList.remove("starterlights_panel-off");
    panel.classList.add("starterlights_panel-on");
  } else {
    panel.classList.remove("starterlights_panel-on");
    panel.classList.add("starterlights_panel-off");
  }

  // Illuminate individual lights
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

    renderAlertBar(eventCodes);
  } catch (err) {
    console.error("Failed to fetch telemetry:", err);
  }
}

    setInterval(fetchTelemetry, 100); // Poll every 100ms