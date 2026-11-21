// const TELEMETRY_URL = "http://localhost:8000/telemetry";
// const STALE_MS = 2000;            // go blank after this long with no new telemetry
// const FORECAST_MINUTES = 10;      // how far ahead the "future" weather looks

// let telemetryState = {};
// let lastLive = null;
// let lastLiveChange = Date.now();
// let fetchOk = false;
// let lastEventSeq = null;

// const $ = id => document.getElementById(id);

// const gearEl = $('gear'), brakeBiasEl = $('brake-bias'), drsLedEl = $('drs-led');
// const lapInfoEl = $('lap-info'), positionEl = $('position'), ersModeEl = $('ers-mode');
// const fuelLapsEl = $('fuel-laps'), rejoinPosEl = $('rejoin-pos'), speedEl = $('speed');
// const revStrip = $('rev-strip'), dashFrame = $('dash-frame');
// const flagAlertEl = $('flag-alert'), pitOverlayEl = $('pit-limiter-overlay');
// const ersDeployedCircleEl = $('ers-deployed-circle'), ersStoreCircleEl = $('ers-store-circle');
// const ersBatteryTextEl = $('ers-battery-text');
// const scLabelEl = $('sc-label'), scDeltaEl = $('sc-delta'), toastEl = $('event-toast');
// const sessionEl = $('session-name'), wxNowEl = $('wx-now'), wxNextEl = $('wx-next'), wxTimeEl = $('wx-time');
// const gapAheadEl = $('gap-ahead'), gapBehindEl = $('gap-behind');
// const wxRainEl = $('wx-rain') || $('.wx-rain');   // '.wx-rain' = id typo in older HTML copies

// const flWearBarEl = $('fl-wear-bar'), frWearBarEl = $('fr-wear-bar');
// const rlWearBarEl = $('rl-wear-bar'), rrWearBarEl = $('rr-wear-bar');
// const flWearValueEl = $('fl-wear-value'), frWearValueEl = $('fr-wear-value');
// const rlWearValueEl = $('rl-wear-value'), rrWearValueEl = $('rr-wear-value');


// const DESIGN_W = 1734, DESIGN_H = 800;
// function fitToScreen() {
//     const w = document.documentElement.clientWidth;
//     const h = document.documentElement.clientHeight;
//     const s = Math.min(w / DESIGN_W, h / DESIGN_H);
//     $('stage').style.setProperty('--fit', s);
// }
// window.addEventListener('resize', fitToScreen);
// window.addEventListener('load', fitToScreen);
// setInterval(fitToScreen, 1000);   // catches rotation or fullscreen changes that don't fire resize
// fitToScreen();

// for (let i = 0; i < 15; i++) {
//     const led = document.createElement('div');
//     led.className = 'led';
//     revStrip.appendChild(led);
// }
// const leds = Array.from(revStrip.children);

// const gearMap = { '-1': 'R', '0': 'N' };   // 1-8 fall through as numbers

// const flagMap = {
//     1: { text: 'GREEN FLAG', color: 'green' },
//     2: { text: 'BLUE FLAG', color: 'blue' },
//     3: { text: 'YELLOW FLAG', color: 'yellow' },
//     4: { text: 'RED FLAG', color: 'red' }
// };

// const ersModeMap = {
//     0: { text: 'None', color: '#FFFFFF' },
//     1: { text: 'Medium', color: '#FFD580' },
//     2: { text: 'Hotlap', color: '#FFA500' },
//     3: { text: 'Overtake', color: '#ff3300' }
// };

// const SESSION_NAMES = {
//     1: 'P1', 2: 'P2', 3: 'P3', 4: 'SHORT P',
//     5: 'Q1', 6: 'Q2', 7: 'Q3', 8: 'SHORT Q', 9: 'OSQ',
//     10: 'SPRINT SQ1', 11: 'SPRINT SQ2', 12: 'SPRINT SQ3', 13: 'SHORT SQ', 14: 'OS SPRINT SQ',
//     15: 'RACE', 16: 'RACE 2', 17: 'RACE 3', 18: 'TT'
// };

// // 0 clear, 1 light cloud, 2 overcast, 3 light rain, 4 heavy rain, 5 storm
// const WEATHER_ICONS = { 0: '☀️', 1: '🌤️', 2: '☁️', 3: '🌦️', 4: '🌧️', 5: '⛈️' };

// // // [temperature °C, hue] stops. 220 = blue, 120 = green, 30 = orange, 0 = red.
// // const TEMP_STOPS = {
// //     surface: [[70, 220], [85, 120], [105, 120], [115, 30], [125, 0]],
// //     inner:   [[75, 220], [90, 120], [105, 120], [115, 30], [125, 0]]
// // };

// const TEMP_STOPS = {
//     surface: makeStops(85, 105),   // border of each tyre bar
//     inner:   makeStops(85, 100)    // fill of each tyre bar
// };

// function tempColour(t, stops) {
//     if (t <= stops[0][0]) return 'hsl(' + stops[0][1] + ' 90% 50%)';
//     for (let i = 1; i < stops.length; i++) {
//         if (t <= stops[i][0]) {
//             const [t0, h0] = stops[i - 1];
//             const [t1, h1] = stops[i];
//             const h = h0 + (h1 - h0) * ((t - t0) / (t1 - t0));
//             return 'hsl(' + h.toFixed(0) + ' 90% 50%)';
//         }
//     }
//     return 'hsl(' + stops[stops.length - 1][1] + ' 90% 50%)';
// }

// function fmtGap(ms) {
//     if (ms === undefined || ms === null || ms <= 0) return '--';
//     return '+' + (ms / 1000).toFixed(3);
// }

// async function fetchTelemetry() {
//     try {
//         const res = await fetch(TELEMETRY_URL);
//         telemetryState = await res.json();
//         fetchOk = true;
//     } catch (err) {
//         fetchOk = false;
//         console.error('Failed to fetch telemetry:', err);
//     }
// }

// function checkStale() {
//     const live = telemetryState.last_live;
//     if (live !== lastLive) { lastLive = live; lastLiveChange = Date.now(); }

//     const paused = telemetryState.global_data?.m_gamePaused === 1;
//     const stale = !fetchOk
//                || live === undefined
//                || (Date.now() - lastLiveChange) > STALE_MS
//                || paused;

//     document.body.classList.toggle('stale', stale);
//     return stale;
// }

// setInterval(async () => {
//     await fetchTelemetry();
//     if (!checkStale()) updateDashboard();
// }, 100);

// // Race events: show the code briefly. Swap in nicer wording per event code if you like.
// let toastTimer = null;
// function showEvent(code) {
//     if (!code) return;
//     toastEl.innerText = code;
//     toastEl.style.display = 'block';
//     clearTimeout(toastTimer);
//     toastTimer = setTimeout(() => { toastEl.style.display = 'none'; }, 3000);
// }

// function updateExtras(p, g) {
//     // Session type
//     const st = g.m_sessionType ?? telemetryState.m_sessionType;
//     if (st !== undefined) sessionEl.innerText = SESSION_NAMES[st] || (st ? 'S' + st : '--');

//     // Weather now + forecast
//     const now = g.m_weather ?? telemetryState.m_weather;
//     if (now !== undefined) wxNowEl.innerText = WEATHER_ICONS[now] ?? '-';

//     // Forecast: only samples for the current session, soonest first
//     const all = g.m_weatherForecastSamples ?? telemetryState.m_weatherForecastSamples ?? [];
//     const samples = all
//         .filter(s => st === undefined || s.m_sessionType === st)
//         .sort((a, b) => a.m_timeOffset - b.m_timeOffset);

//     if (samples.length) {
//         const next = samples.find(s => s.m_timeOffset >= FORECAST_MINUTES) || samples[samples.length - 1];
//         wxNextEl.innerText = WEATHER_ICONS[next.m_weather] ?? '-';
//         wxTimeEl.innerText = '+' + next.m_timeOffset + 'm';

//         // Rain chance for that forecast point (0-100)
//         const rain = next.m_rainPercentage;
//         if (wxRainEl) {
//             if (rain !== undefined) {
//                 wxRainEl.innerText = rain + '%';
//                 wxRainEl.style.color = rain >= 70 ? '#29b6f6' : rain >= 30 ? '#FFBF00' : '#fff';
//             } else {
//                 wxRainEl.innerText = '--';
//             }
//         }
//     }

//     // Gaps in ms (backend sends both, derived from the lap data packet).
//     const ahead  = p.m_deltaToCarInFrontInMS ?? p.m_deltaToCarInFront ?? p.m_gapAhead;
//     const behind = p.m_deltaToCarBehindInMS  ?? p.m_deltaToCarBehind  ?? p.m_gapBehind;
//     gapAheadEl.innerText  = fmtGap(ahead);
//     gapBehindEl.innerText = fmtGap(behind);
// }

// function updateDashboard() {
//     if (!telemetryState || Object.keys(telemetryState).length === 0) return;

//     const playerCarData = telemetryState.player_car_data || {};
//     const globalData = telemetryState.global_data || {};
//     const flagInfo = flagMap[playerCarData.m_vehicleFiaFlags];
//     const rpmPercent = playerCarData.m_revLightsPercent;

//     // Flag banner
//     if (flagInfo) {
//         flagAlertEl.innerText = flagInfo.text;
//         flagAlertEl.style.backgroundColor = flagInfo.color;
//         flagAlertEl.style.display = 'block';
//     } else {
//         flagAlertEl.style.display = 'none';
//     }

//     // Race events: show each new one once
//     const evSeq = telemetryState.m_eventSeq;
//     if (evSeq !== undefined && evSeq !== lastEventSeq) {
//         if (lastEventSeq !== null) showEvent(telemetryState.m_eventName || telemetryState.m_eventStringCode);
//         lastEventSeq = evSeq;
//     }

//     // Safety car / VSC banner (status 1 = SC, 2 = VSC)
//     const scStatus = globalData.m_safetyCarStatus ?? playerCarData.m_safetyCarStatus ?? telemetryState.m_safetyCarStatus;
//     const scDelta  = playerCarData.m_safetyCarDelta ?? globalData.m_safetyCarDelta ?? telemetryState.m_safetyCarDelta;
//     const scOut = scStatus === 1 || scStatus === 2;
//     document.body.classList.toggle('sc-active', scOut);
//     if (scOut) {
//         scLabelEl.innerText = scStatus === 2 ? 'VSC' : 'Safety Car';
//         if (scDelta !== undefined) {
//             scDeltaEl.innerText = (scDelta >= 0 ? '+' : '') + scDelta.toFixed(3);
//             scDeltaEl.style.color = scDelta >= 0 ? '#24fe07' : '#ff3b30';
//         }
//     }

//     // Pit limiter blink
//     pitOverlayEl.classList.toggle('active', playerCarData.m_pitLimiterStatus === 1);

//     // Gear
//     if (playerCarData.m_gear !== undefined) {
//         const gv = playerCarData.m_gear;
//         gearEl.innerText = gearMap[gv] ?? gv;
//     }

//     // Speed
//     if (playerCarData.m_speed !== undefined) {
//         speedEl.innerText = `${Math.round(playerCarData.m_speed)} MPH`;
//     }

    
//     // Brake bias
//     if (playerCarData.m_brakeBias !== undefined) {
//         brakeBiasEl.innerText = `${playerCarData.m_brakeBias}%`;
//     }

//     // ERS mode
//     if (playerCarData.m_ersDeployMode !== undefined) {
//         const ersInfo = ersModeMap[playerCarData.m_ersDeployMode];
//         if (ersInfo) {
//             ersModeEl.innerText = ersInfo.text;
//             ersModeEl.style.color = ersInfo.color;
//         }
//     }

//     // ERS store (yellow ring)
//     if (playerCarData.m_ersStoreEnergy !== undefined) {
//         const MAX_ERS_STORE = 4000000;
//         const pct = (playerCarData.m_ersStoreEnergy / MAX_ERS_STORE) * 100;
//         ersBatteryTextEl.innerText = `${Math.round(pct)}%`;
//         ersStoreCircleEl.style.setProperty('--ers-store-percent', `${pct}%`);
//         const glow = pct / 100;
//         ersStoreCircleEl.style.boxShadow = `0 0 ${15 * glow}px rgba(255, 235, 59, ${glow * 0.8})`;
//     }

//     // ERS deploy available (green ring)
//     if (playerCarData.m_ersDeployedThisLap !== undefined) {
//         const MAX_ERS_DEPLOY_LAP = 4000000;
//         const deployedPct = (playerCarData.m_ersDeployedThisLap / MAX_ERS_DEPLOY_LAP) * 100;
//         ersDeployedCircleEl.style.setProperty('--ers-deployed-percent', `${100 - deployedPct}%`);
//     }

//     // Fuel laps
//     if (playerCarData.m_fuelRemainingLaps !== undefined) {
//         const fuelLaps = playerCarData.m_fuelRemainingLaps;
//         fuelLapsEl.innerText = fuelLaps.toFixed(2);
//         fuelLapsEl.style.color = fuelLaps < 0 ? 'red' : '#24fe07';
//     }

//     // Rejoin position
//     if (playerCarData.m_pitStopRejoinPosition !== undefined) {
//         rejoinPosEl.innerText = playerCarData.m_pitStopRejoinPosition;
//     }

//     // DRS
//     if (playerCarData.m_drs !== undefined && playerCarData.m_drsAllowed !== undefined) {
//         drsLedEl.classList.remove('on', 'green', 'blue');
//         if (playerCarData.m_drs === 1) drsLedEl.classList.add('on', 'green');
//         else if (playerCarData.m_drsAllowed === 1) drsLedEl.classList.add('on', 'blue');
//     }

//     // Laps remaining (or lap number if total unknown)
//     if (playerCarData.m_currentLapNum !== undefined && playerCarData.m_totalLaps > 0) {
//         lapInfoEl.innerText = `${playerCarData.m_totalLaps - playerCarData.m_currentLapNum}`;
//     } else if (playerCarData.m_currentLapNum !== undefined) {
//         lapInfoEl.innerText = `${playerCarData.m_currentLapNum}`;
//     }

//     // Tyres: bar width = remaining life, bar colour = inner temp, border = surface temp
//     if (playerCarData.m_tyresWear) {
//         const wears = playerCarData.m_tyresWear;                     // [RL, RR, FL, FR]
//         const surf  = playerCarData.m_tyresSurfaceTemperature || [];
//         const inner = playerCarData.m_tyresInnerTemperature || [];
//         const tyres = [
//             { bar: rlWearBarEl, value: rlWearValueEl, wear: wears[0], surf: surf[0], inner: inner[0] },
//             { bar: rrWearBarEl, value: rrWearValueEl, wear: wears[1], surf: surf[1], inner: inner[1] },
//             { bar: flWearBarEl, value: flWearValueEl, wear: wears[2], surf: surf[2], inner: inner[2] },
//             { bar: frWearBarEl, value: frWearValueEl, wear: wears[3], surf: surf[3], inner: inner[3] }
//         ];
//         tyres.forEach(t => {
//             const remaining = Math.max(0, Math.min(100, 100 - t.wear));
//             t.bar.style.width = `${remaining}%`;
//             t.value.innerText = `${Math.round(remaining)}%`;
//             if (t.inner !== undefined) t.bar.style.backgroundColor = tempColour(t.inner, TEMP_STOPS.inner);
//             if (t.surf !== undefined) t.bar.parentElement.style.borderColor = tempColour(t.surf, TEMP_STOPS.surface);
//         });
//     }

//     try { updateDamage(playerCarData); } catch (e) { console.error('damage view:', e); }
//     try { updateExtras(playerCarData, globalData); } catch (e) { console.error('extras:', e); }

//     // Position
//     if (playerCarData.m_carPosition !== undefined && globalData.m_numActiveCars > 0) {
//         positionEl.innerText = `${playerCarData.m_carPosition}/${globalData.m_numActiveCars}`;
//     } else if (playerCarData.m_carPosition !== undefined) {
//         positionEl.innerText = `${playerCarData.m_carPosition}`;
//     }

//     // Rev lights and shift flash
//     if (rpmPercent !== undefined) {
//         leds.forEach((led, index) => {
//             const threshold = (index / leds.length) * 100;
//             if (rpmPercent > threshold) {
//                 const colour = index < 5 ? '#4caf50' : index < 10 ? '#ffeb3b' : '#f44336';
//                 led.style.background = colour;
//                 led.style.boxShadow = '0 0 10px ' + colour;
//             } else {
//                 led.style.background = '#333';
//                 led.style.boxShadow = 'none';
//             }
//         });

//         const isShiftFlash = rpmPercent > 90 && playerCarData.m_gear !== 8;
//         if (isShiftFlash) {
//             dashFrame.classList.add('shift-flash');
//             dashFrame.style.backgroundColor = '';
//         } else {
//             dashFrame.classList.remove('shift-flash');
//             dashFrame.style.backgroundColor = flagInfo ? flagInfo.color : '#222';
//         }
//     }
// }
// // ---- Car damage ----
// const AMBER_AT = 30;     // damage % that turns a part amber
// const RED_AT = 50;       // damage % that turns a part red
// const SWIPE_PX = 40;     // drag distance that counts as a swipe
// const TAP_PX = 10;       // movement under this counts as a tap

// const ZONES = [
//     ['fwl', 'Front wing L', p => p.m_frontLeftWingDamage],
//     ['fwr', 'Front wing R', p => p.m_frontRightWingDamage],
//     ['rw', 'Rear wing', p => p.m_rearWingDamage],
//     ['floor', 'Floor', p => p.m_floorDamage],
//     ['side', 'Sidepods', p => p.m_sidepodDamage],
//     ['diff', 'Diffuser', p => p.m_diffuserDamage],
//     ['gear', 'Gearbox', p => p.m_gearBoxDamage],
//     ['eng', 'Engine', p => p.m_engineDamage],
//     // Faults: only do anything if the SVG has data-z="drs" / data-z="ers" elements
//     ['drs', 'DRS fault', p => (p.m_drsFault === 1 ? 100 : 0)],
//     ['ers', 'ERS fault', p => (p.m_ersFault === 1 ? 100 : 0)],
// ];
// // Tyres removed. Brakes kept; indices are [RL, RR, FL, FR]
// const BRAKE_IDX = { RL: 0, RR: 1, FL: 2, FR: 3 };
// for (const k in BRAKE_IDX) {
//     ZONES.push(['b' + BRAKE_IDX[k], 'Brake ' + k, p => (p.m_brakesDamage || [])[BRAKE_IDX[k]]]);
// }

// const zoneEls = {};
// ZONES.forEach(z => { zoneEls[z[0]] = Array.from(document.querySelectorAll('#car [data-z="' + z[0] + '"]')); });
// const stageEl = $('stage');
// const carEl = $('car');

// // Auto-hide state
// const DAMAGE_SHOW_MS = 5000;     // how long the panel stays up after damage is detected
// let panelHidden = true;
// let acknowledged = new Map();    // zone id -> highest severity (1 amber, 2 red) that has already had its turn on screen
// let damageTimer = null;
// const sev = f => (f.cls === 'red' ? 2 : 1);

// function hideDamage() {
//     clearTimeout(damageTimer);
//     damageTimer = null;
//     panelHidden = true;
//     stageEl.classList.remove('has-damage');
// }

// function showDamage() {
//     panelHidden = false;
//     stageEl.classList.add('has-damage');
//     clearTimeout(damageTimer);                        // new damage while visible restarts the 5s
//     damageTimer = setTimeout(hideDamage, DAMAGE_SHOW_MS);
// }

// function updateDamage(p) {
//     const found = [];
//     ZONES.forEach(([id, label, get]) => {
//         const v = Math.round(Number(get(p)) || 0);
//         const cls = v >= RED_AT ? 'red' : (v >= AMBER_AT ? 'amber' : '');
//         zoneEls[id].forEach(el => {
//             el.classList.remove('amber', 'red');
//             if (cls) el.classList.add(cls);
//         });
//         // Only count zones that actually exist on the SVG, so the panel never shows an uncoloured car
//         if (cls && zoneEls[id].length) found.push({ id, cls });
//     });

//     // Damage fully repaired / new session: forget what we've shown and make sure the panel is hidden
//     if (found.length === 0) {
//         acknowledged.clear();
//         if (!panelHidden) hideDamage();
//         return;
//     }

//     // Show for 5s when a zone is damaged for the first time or gets worse (amber -> red).
//     // Damage that has already had its 5s stays hidden until it changes again.
//     const isNew = found.some(f => (acknowledged.get(f.id) || 0) < sev(f));
//     if (isNew) {
//         found.forEach(f => acknowledged.set(f.id, Math.max(acknowledged.get(f.id) || 0, sev(f))));
//         showDamage();
//     }
// }

// function dismissDamage() {   // tap/swipe still closes it early
//     hideDamage();
// }

// // Tap or swipe the car to dismiss the panel
// (function setupDismiss() {
//     const panelEl = carEl;   // change to the panel's container if it has its own id
//     panelEl.style.touchAction = 'none';
//     let sx = 0, sy = 0, tracking = false;

//     panelEl.addEventListener('pointerdown', e => {
//         sx = e.clientX; sy = e.clientY; tracking = true;
//     });
//     panelEl.addEventListener('pointerup', e => {
//         if (!tracking) return;
//         tracking = false;
//         const move = Math.max(Math.abs(e.clientX - sx), Math.abs(e.clientY - sy));
//         if (move >= SWIPE_PX || move < TAP_PX) dismissDamage();
//     });
//     panelEl.addEventListener('pointercancel', () => { tracking = false; });
// })();


const TELEMETRY_URL = "http://localhost:8000/telemetry";
const STALE_MS = 2000;            // go blank after this long with no new telemetry
const FORECAST_MINUTES = 10;      // how far ahead the "future" weather looks

let telemetryState = {};
let lastLive = null;
let lastLiveChange = Date.now();
let fetchOk = false;
let lastEventSeq = null;

const $ = id => document.getElementById(id);

const gearEl = $('gear'), brakeBiasEl = $('brake-bias'), drsLedEl = $('drs-led');
const lapInfoEl = $('lap-info'), positionEl = $('position'), ersModeEl = $('ers-mode');
const fuelLapsEl = $('fuel-laps'), rejoinPosEl = $('rejoin-pos'), speedEl = $('speed');
const revStrip = $('rev-strip'), dashFrame = $('dash-frame');
const flagAlertEl = $('flag-alert'), pitOverlayEl = $('pit-limiter-overlay');
const ersDeployedCircleEl = $('ers-deployed-circle'), ersStoreCircleEl = $('ers-store-circle');
const ersBatteryTextEl = $('ers-battery-text');
const scLabelEl = $('sc-label'), scDeltaEl = $('sc-delta'), toastEl = $('event-toast');
const sessionEl = $('session-name'), wxNowEl = $('wx-now'), wxNextEl = $('wx-next'), wxTimeEl = $('wx-time');
const gapAheadEl = $('gap-ahead'), gapBehindEl = $('gap-behind');
const wxRainEl = $('wx-rain') || $('.wx-rain');   // '.wx-rain' = id typo in older HTML copies

const flWearBarEl = $('fl-wear-bar'), frWearBarEl = $('fr-wear-bar');
const rlWearBarEl = $('rl-wear-bar'), rrWearBarEl = $('rr-wear-bar');
const flWearValueEl = $('fl-wear-value'), frWearValueEl = $('fr-wear-value');
const rlWearValueEl = $('rl-wear-value'), rrWearValueEl = $('rr-wear-value');


const DESIGN_W = 1734, DESIGN_H = 800;
function fitToScreen() {
    const w = document.documentElement.clientWidth;
    const h = document.documentElement.clientHeight;
    const s = Math.min(w / DESIGN_W, h / DESIGN_H);
    $('stage').style.setProperty('--fit', s);
}
window.addEventListener('resize', fitToScreen);
window.addEventListener('load', fitToScreen);
setInterval(fitToScreen, 1000);   // catches rotation or fullscreen changes that don't fire resize
fitToScreen();

for (let i = 0; i < 15; i++) {
    const led = document.createElement('div');
    led.className = 'led';
    revStrip.appendChild(led);
}
const leds = Array.from(revStrip.children);

const gearMap = { '-1': 'R', '0': 'N' };   // 1-8 fall through as numbers

const flagMap = {
    1: { text: 'GREEN FLAG', color: 'green' },
    2: { text: 'BLUE FLAG', color: 'blue' },
    3: { text: 'YELLOW FLAG', color: 'yellow' },
    4: { text: 'RED FLAG', color: 'red' }
};

const ersModeMap = {
    0: { text: 'None', color: '#FFFFFF' },
    1: { text: 'Medium', color: '#FFD580' },
    2: { text: 'Hotlap', color: '#FFA500' },
    3: { text: 'Overtake', color: '#ff3300' }
};

const SESSION_NAMES = {
    1: 'P1', 2: 'P2', 3: 'P3', 4: 'SHORT P',
    5: 'Q1', 6: 'Q2', 7: 'Q3', 8: 'SHORT Q', 9: 'OSQ',
    10: 'SPRINT SQ1', 11: 'SPRINT SQ2', 12: 'SPRINT SQ3', 13: 'SHORT SQ', 14: 'OS SPRINT SQ',
    15: 'RACE', 16: 'RACE 2', 17: 'RACE 3', 18: 'TT'
};

// ---- Session-based layout ----
// Which family each session id belongs to
const SESSION_KIND = {
    1: 'practice', 2: 'practice', 3: 'practice', 4: 'practice',
    5: 'quali', 6: 'quali', 7: 'quali', 8: 'quali', 9: 'quali',
    10: 'quali', 11: 'quali', 12: 'quali', 13: 'quali', 14: 'quali',   // sprint shootouts
    15: 'race', 16: 'race', 17: 'race',
    18: 'tt'
};

// What each family shows/hides lives in style.css (body[data-session="..."] rules).

let currentKind = null;
function applyLayout(st) {
    const kind = SESSION_KIND[st] || 'unknown';      // unknown session: CSS shows everything
    if (kind === currentKind) return;
    currentKind = kind;
    document.body.dataset.session = kind;            // CSS hook: body[data-session="race"] { ... }
}

// 0 clear, 1 light cloud, 2 overcast, 3 light rain, 4 heavy rain, 5 storm
const WEATHER_ICONS = { 0: '☀️', 1: '🌤️', 2: '☁️', 3: '🌦️', 4: '🌧️', 5: '⛈️' };

// Tyre temperature colours. Hue: 220 blue (cold) > 180 cyan > 120 green (ideal) > 60 yellow > 30 orange > 0 red (too hot).
// Tune each tyre type with just two numbers: the green window [lo, hi] in °C.
//   below lo  -> fades green > cyan > blue (blue only ~30 degrees under lo)
//   above hi  -> fades green > yellow > orange > red (red ~26 degrees over hi)
function makeStops(lo, hi) {
    return [[lo - 30, 220], [lo - 12, 180], [lo, 120], [hi, 120], [hi + 8, 60], [hi + 16, 30], [hi + 26, 0]];
}
const TEMP_STOPS = {
    surface: makeStops(55, 105),   // border of each tyre bar
    inner:   makeStops(65, 100)    // fill colour of each tyre bar
};

function tempColour(t, stops) {
    if (t <= stops[0][0]) return 'hsl(' + stops[0][1] + ' 90% 50%)';
    for (let i = 1; i < stops.length; i++) {
        if (t <= stops[i][0]) {
            const [t0, h0] = stops[i - 1];
            const [t1, h1] = stops[i];
            const h = h0 + (h1 - h0) * ((t - t0) / (t1 - t0));
            return 'hsl(' + h.toFixed(0) + ' 90% 50%)';
        }
    }
    return 'hsl(' + stops[stops.length - 1][1] + ' 90% 50%)';
}

function fmtGap(ms) {
    if (ms === undefined || ms === null || ms <= 0) return '--';
    return '+' + (ms / 1000).toFixed(3);
}

async function fetchTelemetry() {
    try {
        const res = await fetch(TELEMETRY_URL);
        telemetryState = await res.json();
        fetchOk = true;
    } catch (err) {
        fetchOk = false;
        console.error('Failed to fetch telemetry:', err);
    }
}

function checkStale() {
    const live = telemetryState.last_live;
    if (live !== lastLive) { lastLive = live; lastLiveChange = Date.now(); }

    const paused = telemetryState.global_data?.m_gamePaused === 1;
    const stale = !fetchOk
               || live === undefined
               || (Date.now() - lastLiveChange) > STALE_MS
               || paused;

    document.body.classList.toggle('stale', stale);
    return stale;
}

setInterval(async () => {
    await fetchTelemetry();
    if (!checkStale()) updateDashboard();
}, 100);

// Race events: show the code briefly. Swap in nicer wording per event code if you like.
let toastTimer = null;
function showEvent(code) {
    if (!code) return;
    toastEl.innerText = code;
    toastEl.style.display = 'block';
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => { toastEl.style.display = 'none'; }, 3000);
}

function updateExtras(p, g) {
    // Session type
    const st = g.m_sessionType ?? telemetryState.m_sessionType;
    if (st !== undefined) sessionEl.innerText = SESSION_NAMES[st] || (st ? 'S' + st : '--');
    if (st !== undefined) applyLayout(st);

    // Weather now + forecast
    const now = g.m_weather ?? telemetryState.m_weather;
    if (now !== undefined) wxNowEl.innerText = WEATHER_ICONS[now] ?? '-';

    // Forecast: only samples for the current session, soonest first
    const all = g.m_weatherForecastSamples ?? telemetryState.m_weatherForecastSamples ?? [];
    const samples = all
        .filter(s => st === undefined || s.m_sessionType === st)
        .sort((a, b) => a.m_timeOffset - b.m_timeOffset);

    if (samples.length) {
        const next = samples.find(s => s.m_timeOffset >= FORECAST_MINUTES) || samples[samples.length - 1];
        wxNextEl.innerText = WEATHER_ICONS[next.m_weather] ?? '-';
        wxTimeEl.innerText = '+' + next.m_timeOffset + 'm';

        // Rain chance for that forecast point (0-100)
        const rain = next.m_rainPercentage;
        if (wxRainEl) {
            if (rain !== undefined) {
                wxRainEl.innerText = rain + '%';
                wxRainEl.style.color = rain >= 70 ? '#29b6f6' : rain >= 30 ? '#FFBF00' : '#fff';
            } else {
                wxRainEl.innerText = '--';
            }
        }
    }

    // Gaps in ms (backend sends both, derived from the lap data packet).
    const ahead  = p.m_deltaToCarInFrontInMS ?? p.m_deltaToCarInFront ?? p.m_gapAhead;
    const behind = p.m_deltaToCarBehindInMS  ?? p.m_deltaToCarBehind  ?? p.m_gapBehind;
    gapAheadEl.innerText  = fmtGap(ahead);
    gapBehindEl.innerText = fmtGap(behind);
}

function updateDashboard() {
    if (!telemetryState || Object.keys(telemetryState).length === 0) return;

    const playerCarData = telemetryState.player_car_data || {};
    const globalData = telemetryState.global_data || {};
    const flagInfo = flagMap[playerCarData.m_vehicleFiaFlags];
    const rpmPercent = playerCarData.m_revLightsPercent;

    // Flag banner
    if (flagInfo) {
        flagAlertEl.innerText = flagInfo.text;
        flagAlertEl.style.backgroundColor = flagInfo.color;
        flagAlertEl.style.display = 'block';
    } else {
        flagAlertEl.style.display = 'none';
    }

    // Race events: show each new one once
    const evSeq = telemetryState.m_eventSeq;
    if (evSeq !== undefined && evSeq !== lastEventSeq) {
        if (lastEventSeq !== null) showEvent(telemetryState.m_eventName || telemetryState.m_eventStringCode);
        lastEventSeq = evSeq;
    }

    // Safety car / VSC banner (status 1 = SC, 2 = VSC)
    const scStatus = globalData.m_safetyCarStatus ?? playerCarData.m_safetyCarStatus ?? telemetryState.m_safetyCarStatus;
    const scDelta  = playerCarData.m_safetyCarDelta ?? globalData.m_safetyCarDelta ?? telemetryState.m_safetyCarDelta;
    const scOut = scStatus === 1 || scStatus === 2;
    document.body.classList.toggle('sc-active', scOut);
    if (scOut) {
        scLabelEl.innerText = scStatus === 2 ? 'VSC' : 'Safety Car';
        if (scDelta !== undefined) {
            scDeltaEl.innerText = (scDelta >= 0 ? '+' : '') + scDelta.toFixed(3);
            scDeltaEl.style.color = scDelta >= 0 ? '#24fe07' : '#ff3b30';
        }
    }

    // Pit limiter blink
    pitOverlayEl.classList.toggle('active', playerCarData.m_pitLimiterStatus === 1);

    // Gear
    if (playerCarData.m_gear !== undefined) {
        const gv = playerCarData.m_gear;
        gearEl.innerText = gearMap[gv] ?? gv;
    }

    // Speed
    if (playerCarData.m_speed !== undefined) {
        speedEl.innerText = `${Math.round(playerCarData.m_speed)} MPH`;
    }

    
    // Brake bias
    if (playerCarData.m_brakeBias !== undefined) {
        brakeBiasEl.innerText = `${playerCarData.m_brakeBias}%`;
    }

    // ERS mode
    if (playerCarData.m_ersDeployMode !== undefined) {
        const ersInfo = ersModeMap[playerCarData.m_ersDeployMode];
        if (ersInfo) {
            ersModeEl.innerText = ersInfo.text;
            ersModeEl.style.color = ersInfo.color;
        }
    }

    // ERS store (yellow ring)
    if (playerCarData.m_ersStoreEnergy !== undefined) {
        const MAX_ERS_STORE = 4000000;
        const pct = (playerCarData.m_ersStoreEnergy / MAX_ERS_STORE) * 100;
        ersBatteryTextEl.innerText = `${Math.round(pct)}%`;
        ersStoreCircleEl.style.setProperty('--ers-store-percent', `${pct}%`);
        const glow = pct / 100;
        ersStoreCircleEl.style.boxShadow = `0 0 ${15 * glow}px rgba(255, 235, 59, ${glow * 0.8})`;
    }

    // ERS deploy available (green ring)
    if (playerCarData.m_ersDeployedThisLap !== undefined) {
        const MAX_ERS_DEPLOY_LAP = 4000000;
        const deployedPct = (playerCarData.m_ersDeployedThisLap / MAX_ERS_DEPLOY_LAP) * 100;
        ersDeployedCircleEl.style.setProperty('--ers-deployed-percent', `${100 - deployedPct}%`);
    }

    // Fuel laps
    if (playerCarData.m_fuelRemainingLaps !== undefined) {
        const fuelLaps = playerCarData.m_fuelRemainingLaps;
        fuelLapsEl.innerText = fuelLaps.toFixed(2);
        fuelLapsEl.style.color = fuelLaps < 0 ? 'red' : '#24fe07';
    }

    // Rejoin position
    if (playerCarData.m_pitStopRejoinPosition !== undefined) {
        rejoinPosEl.innerText = playerCarData.m_pitStopRejoinPosition;
    }

    // DRS
    if (playerCarData.m_drs !== undefined && playerCarData.m_drsAllowed !== undefined) {
        drsLedEl.classList.remove('on', 'green', 'blue');
        if (playerCarData.m_drs === 1) drsLedEl.classList.add('on', 'green');
        else if (playerCarData.m_drsAllowed === 1) drsLedEl.classList.add('on', 'blue');
    }

    // Laps remaining (or lap number if total unknown)
    if (playerCarData.m_currentLapNum !== undefined && playerCarData.m_totalLaps > 0) {
        lapInfoEl.innerText = `${playerCarData.m_totalLaps - playerCarData.m_currentLapNum}`;
    } else if (playerCarData.m_currentLapNum !== undefined) {
        lapInfoEl.innerText = `${playerCarData.m_currentLapNum}`;
    }

    // Tyres: bar width = remaining life, bar colour = inner temp, border = surface temp
    if (playerCarData.m_tyresWear) {
        const wears = playerCarData.m_tyresWear;                     // [RL, RR, FL, FR]
        const surf  = playerCarData.m_tyresSurfaceTemperature || [];
        const inner = playerCarData.m_tyresInnerTemperature || [];
        const tyres = [
            { bar: rlWearBarEl, value: rlWearValueEl, wear: wears[0], surf: surf[0], inner: inner[0] },
            { bar: rrWearBarEl, value: rrWearValueEl, wear: wears[1], surf: surf[1], inner: inner[1] },
            { bar: flWearBarEl, value: flWearValueEl, wear: wears[2], surf: surf[2], inner: inner[2] },
            { bar: frWearBarEl, value: frWearValueEl, wear: wears[3], surf: surf[3], inner: inner[3] }
        ];
        tyres.forEach(t => {
            const remaining = Math.max(0, Math.min(100, 100 - t.wear));
            t.bar.style.width = `${remaining}%`;
            t.value.innerText = `${Math.round(remaining)}%`;
            if (t.inner !== undefined) t.bar.style.backgroundColor = tempColour(t.inner, TEMP_STOPS.inner);
            if (t.surf !== undefined) t.bar.parentElement.style.borderColor = tempColour(t.surf, TEMP_STOPS.surface);
        });
    }

    try { updateDamage(playerCarData); } catch (e) { console.error('damage view:', e); }
    try { updateExtras(playerCarData, globalData); } catch (e) { console.error('extras:', e); }

    // Position
    if (playerCarData.m_carPosition !== undefined && globalData.m_numActiveCars > 0) {
        positionEl.innerText = `${playerCarData.m_carPosition}/${globalData.m_numActiveCars}`;
    } else if (playerCarData.m_carPosition !== undefined) {
        positionEl.innerText = `${playerCarData.m_carPosition}`;
    }

    // Rev lights and shift flash
    if (rpmPercent !== undefined) {
        leds.forEach((led, index) => {
            const threshold = (index / leds.length) * 100;
            if (rpmPercent > threshold) {
                const colour = index < 5 ? '#4caf50' : index < 10 ? '#ffeb3b' : '#f44336';
                led.style.background = colour;
                led.style.boxShadow = '0 0 10px ' + colour;
            } else {
                led.style.background = '#333';
                led.style.boxShadow = 'none';
            }
        });

        const isShiftFlash = rpmPercent > 90 && playerCarData.m_gear !== 8;
        if (isShiftFlash) {
            dashFrame.classList.add('shift-flash');
            dashFrame.style.backgroundColor = '';
        } else {
            dashFrame.classList.remove('shift-flash');
            dashFrame.style.backgroundColor = flagInfo ? flagInfo.color : '#222';
        }
    }
}
// ---- Car damage ----
const AMBER_AT = 30;     // damage % that turns a part amber
const RED_AT = 50;       // damage % that turns a part red
const SWIPE_PX = 40;     // drag distance that counts as a swipe
const TAP_PX = 10;       // movement under this counts as a tap

const ZONES = [
    ['fwl', 'Front wing L', p => p.m_frontLeftWingDamage],
    ['fwr', 'Front wing R', p => p.m_frontRightWingDamage],
    ['rw', 'Rear wing', p => p.m_rearWingDamage],
    ['floor', 'Floor', p => p.m_floorDamage],
    ['side', 'Sidepods', p => p.m_sidepodDamage],
    ['diff', 'Diffuser', p => p.m_diffuserDamage],
    ['gear', 'Gearbox', p => p.m_gearBoxDamage],
    ['eng', 'Engine', p => p.m_engineDamage],
    // Faults: only do anything if the SVG has data-z="drs" / data-z="ers" elements
    ['drs', 'DRS fault', p => (p.m_drsFault === 1 ? 100 : 0)],
    ['ers', 'ERS fault', p => (p.m_ersFault === 1 ? 100 : 0)],
];
// Tyres removed. Brakes kept; indices are [RL, RR, FL, FR]
const BRAKE_IDX = { RL: 0, RR: 1, FL: 2, FR: 3 };
for (const k in BRAKE_IDX) {
    ZONES.push(['b' + BRAKE_IDX[k], 'Brake ' + k, p => (p.m_brakesDamage || [])[BRAKE_IDX[k]]]);
}

const zoneEls = {};
ZONES.forEach(z => { zoneEls[z[0]] = Array.from(document.querySelectorAll('#car [data-z="' + z[0] + '"]')); });
const stageEl = $('stage');
const carEl = $('car');

// Auto-hide state
const DAMAGE_SHOW_MS = 5000;     // how long the panel stays up after damage is detected
let panelHidden = true;
let acknowledged = new Map();    // zone id -> highest severity (1 amber, 2 red) that has already had its turn on screen
let damageTimer = null;
const sev = f => (f.cls === 'red' ? 2 : 1);

function hideDamage() {
    clearTimeout(damageTimer);
    damageTimer = null;
    panelHidden = true;
    stageEl.classList.remove('has-damage');
}

function showDamage() {
    panelHidden = false;
    stageEl.classList.add('has-damage');
    clearTimeout(damageTimer);                        // new damage while visible restarts the 5s
    damageTimer = setTimeout(hideDamage, DAMAGE_SHOW_MS);
}

function updateDamage(p) {
    const found = [];
    ZONES.forEach(([id, label, get]) => {
        const v = Math.round(Number(get(p)) || 0);
        const cls = v >= RED_AT ? 'red' : (v >= AMBER_AT ? 'amber' : '');
        zoneEls[id].forEach(el => {
            el.classList.remove('amber', 'red');
            if (cls) el.classList.add(cls);
        });
        // Only count zones that actually exist on the SVG, so the panel never shows an uncoloured car
        if (cls && zoneEls[id].length) found.push({ id, cls });
    });

    // Damage fully repaired / new session: forget what we've shown and make sure the panel is hidden
    if (found.length === 0) {
        acknowledged.clear();
        if (!panelHidden) hideDamage();
        return;
    }

    // Show for 5s when a zone is damaged for the first time or gets worse (amber -> red).
    // Damage that has already had its 5s stays hidden until it changes again.
    const isNew = found.some(f => (acknowledged.get(f.id) || 0) < sev(f));
    if (isNew) {
        found.forEach(f => acknowledged.set(f.id, Math.max(acknowledged.get(f.id) || 0, sev(f))));
        showDamage();
    }
}

function dismissDamage() {   // tap/swipe still closes it early
    hideDamage();
}

// Tap or swipe the car to dismiss the panel
(function setupDismiss() {
    const panelEl = carEl;   // change to the panel's container if it has its own id
    panelEl.style.touchAction = 'none';
    let sx = 0, sy = 0, tracking = false;

    panelEl.addEventListener('pointerdown', e => {
        sx = e.clientX; sy = e.clientY; tracking = true;
    });
    panelEl.addEventListener('pointerup', e => {
        if (!tracking) return;
        tracking = false;
        const move = Math.max(Math.abs(e.clientX - sx), Math.abs(e.clientY - sy));
        if (move >= SWIPE_PX || move < TAP_PX) dismissDamage();
    });
    panelEl.addEventListener('pointercancel', () => { tracking = false; });
})();