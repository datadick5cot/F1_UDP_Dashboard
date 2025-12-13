// // ---------------------------
// // BAR CREATION + UPDATE LOGIC
// // ---------------------------

// // Utility to build a bar container with N segments
// function buildBar(containerId, segments = 100) {
//   const container = document.getElementById(containerId);
//   container.innerHTML = ""; // clear any existing
//   for (let i = 0; i < segments; i++) {
//     const segment = document.createElement("div");
//     segment.classList.add("bar-segment", "blankfilled"); // default state
//     container.appendChild(segment);
//   }
// }

// // Update bar fill based on percentage value
// function updateBar(containerId, percent, type) {
//   const segments = document.querySelectorAll(`#${containerId} .bar-segment`);
//   const total = segments.length;
//   const filledCount = Math.round((percent / 100) * total);

//   segments.forEach((seg, index) => {
//     if (index >= total - filledCount) {
//       seg.className = `bar-segment filled ${type}`;
//     } else {
//       seg.className = "bar-segment blankfilled";
//     }
//   });
// }

// // Build both bars once at page load
// buildBar("brakeBar", 100);
// buildBar("throttleBar", 100);




// function renderRpmLights(percent) {
//     const rpmBar = document.getElementById("rpmBar");
//     rpmBar.innerHTML = "";

//     const activeLights = Math.min(15, Math.ceil(percent / (100 / 15)));

//     for (let i = 1; i <= 15; i++) {
//       let color;
//       if (i <= 5) {
//         color = i <= activeLights ? '#00BFFF' : '#1E1E1E'; // Blue
//       } else if (i <= 10) {
//         color = i <= activeLights ? '#FFA500' : '#1E1E1E'; // Amber
//       } else {
//         color = i <= activeLights ? '#FF0000' : '#1E1E1E'; // Red
//       }

//       const light = document.createElement("div");
//       light.className = "rpm-light";
//       light.style.backgroundColor = color;
//       rpmBar.appendChild(light);
//     }
//   }




// const gearMap = {
//   "R": 0,
//   "N": 1,
//   "1": 2,
//   "2": 3,
//   "3": 4,
//   "4": 5,
//   "5": 6,
//   "6": 7,
//   "7": 8,
//   "8": 9
// };


// const cylinder = document.getElementById('gearCylinder');
// const items = cylinder.querySelectorAll('.gear-item');
// const itemCount = items.length;
// const angleStep = 360 / itemCount;
// let currentIndex = 3; // start at "4"
// let rotation = 0;

// // Position items around the Y-axis
// items.forEach((item, i) => {
//   const angle = i * angleStep;
//   item.style.transform = `rotateY(${angle}deg) translateZ(100px)`;
// });

// // Update active highlight
// function updateActive() {
//   items.forEach((item, i) => {
//     item.classList.toggle('active', i === currentIndex);
//   });
// }

// // Rotate cylinder so active item is centered
// function rotateWheel() {
//   rotation = -currentIndex * angleStep;
//   cylinder.style.transform = `rotateY(${rotation}deg)`;
//   updateActive();
// }

// rotateWheel();

// // ---------------------------
// // TELEMETRY FETCH + UI UPDATE
// // ---------------------------
// async function fetchTelemetry() {
//   try {
//     const res = await fetch("http://localhost:8000/telemetry");
//     const data = await res.json();

//     // Speed and Gear display
//     // document.getElementById("speed").textContent = data.m_speed ?? 0;
//     // document.getElementById("gear").textContent = data.m_gear ?? 0;


//     const gearValue = data.m_gear ?? "N"; // fallback to Neutral
//         if (gearMap.hasOwnProperty(gearValue)) {
//         currentIndex = gearMap[gearValue];
//         rotateWheel();
//         }


//     // Calculate percentages
//     const throttlePercent = Math.round((data.m_throttle ?? 0) * 100);
//     const brakePercent = Math.round((data.m_brake ?? 0) * 100);

//     // Update visual bars
//     updateBar("throttleBar", throttlePercent, "accel");
//     updateBar("brakeBar", brakePercent, "brake");

//     // Starter lights event handling
//     const eventCode = data.m_eventStringCode;
//     if (eventCode === "STLG" && data.m_eventDetails && typeof data.m_eventDetails.numLights === "number") {
//       starterlights(data.m_eventDetails.numLights);
//     } else {
//       starterlights(0); // fallback or hide lights
//     }

//     // RPM lights
//     const rpmPercent = data.m_revLightsPercent ?? 0;
//     renderRpmLights(rpmPercent);

//     // Alert bar
//     const eventCodes = Array.isArray(data.m_eventStringCode)
//       ? data.m_eventStringCode
//       : [data.m_eventStringCode];

//     renderAlertBar(eventCodes);
//   } catch (err) {
//     console.error("Failed to fetch telemetry:", err);
//   }
// }

// // Poll every 100ms
// setInterval(fetchTelemetry, 100);
