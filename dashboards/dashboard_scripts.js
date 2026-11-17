
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
const wxRainEl = $('wx-rain');

const flWearBarEl = $('fl-wear-bar'), frWearBarEl = $('fr-wear-bar');
const rlWearBarEl = $('rl-wear-bar'), rrWearBarEl = $('rr-wear-bar');
const flWearValueEl = $('fl-wear-value'), frWearValueEl = $('fr-wear-value');
const rlWearValueEl = $('rl-wear-value'), rrWearValueEl = $('rr-wear-value');

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
    10: 'RACE', 11: 'RACE 2', 12: 'RACE 3', 13: 'TT'
};

// 0 clear, 1 light cloud, 2 overcast, 3 light rain, 4 heavy rain, 5 storm
const WEATHER_ICONS = { 0: '☀️', 1: '🌤️', 2: '☁️', 3: '🌦️', 4: '🌧️', 5: '⛈️' };

// [temperature °C, hue] stops. 220 = blue, 120 = green, 30 = orange, 0 = red.
const TEMP_STOPS = {
    surface: [[70, 220], [85, 120], [105, 120], [115, 30], [125, 0]],
    inner:   [[75, 220], [90, 120], [105, 120], [115, 30], [125, 0]]
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
    if (st !== undefined) sessionEl.innerText = SESSION_NAMES[st] || '--';

    // Weather now + forecast
    const now = g.m_weather ?? telemetryState.m_weather;
    if (now !== undefined) wxNowEl.innerText = WEATHER_ICONS[now] || '-';

    const samples = g.m_weatherForecastSamples ?? telemetryState.m_weatherForecastSamples ?? [];
    if (samples.length) {
        const next = samples.find(s => s.m_timeOffset >= FORECAST_MINUTES) || samples[samples.length - 1];
        wxNextEl.innerText = WEATHER_ICONS[next.m_weather] || '-';
        wxTimeEl.innerText = '+' + next.m_timeOffset + 'm';
    }

    // Gaps in ms. Gap behind needs the backend to supply it (see notes).
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
        if (lastEventSeq !== null) showEvent(telemetryState.m_eventStringCode);
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

    if (samples.length) {
        const next = samples.find(s => s.m_timeOffset >= FORECAST_MINUTES) || samples[samples.length - 1];
        wxNextEl.innerText = WEATHER_ICONS[next.m_weather] || '-';
        wxTimeEl.innerText = '+' + next.m_timeOffset + 'm';

        // Rain chance for that forecast point (0-100)
        const rain = next.m_rainPercentage;
        if (rain !== undefined) {
            wxRainEl.innerText = rain + '%';
            wxRainEl.style.color = rain >= 70 ? '#29b6f6' : rain >= 30 ? '#FFBF00' : '#666';
        } else {
            wxRainEl.innerText = '';
        }
    }


    if (rainpercetage)

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
const AMBER_AT = 20;     // damage % that turns a part amber
const RED_AT = 50;       // damage % that turns a part red
const IDX = { RL: 0, RR: 1, FL: 2, FR: 3 };   // game arrays are [RL, RR, FL, FR]
const ZONES = [
    ['fwl', 'Front wing L', p => p.m_frontLeftWingDamage],
    ['fwr', 'Front wing R', p => p.m_frontRightWingDamage],
    ['rw', 'Rear wing', p => p.m_rearWingDamage],
    ['floor', 'Floor', p => p.m_floorDamage],
    ['side', 'Sidepods', p => p.m_sidepodDamage],
    ['diff', 'Diffuser', p => p.m_diffuserDamage],
    ['gear', 'Gearbox', p => p.m_gearBoxDamage],
    ['eng', 'Engine', p => p.m_engineDamage],
];
for (const k in IDX) {
    ZONES.push(['t' + IDX[k], 'Tyre ' + k, p => (p.m_tyresDamage || [])[IDX[k]]]);
    ZONES.push(['b' + IDX[k], 'Brake ' + k, p => (p.m_brakesDamage || [])[IDX[k]]]);
}
const zoneEls = {};
ZONES.forEach(z => { zoneEls[z[0]] = Array.from(document.querySelectorAll('#car [data-z="' + z[0] + '"]')); });
const stageEl = $('stage');
const damageListEl = $('damage-list');
let lastList = '';

function updateDamage(p) {
    const found = [];
    ZONES.forEach(([id, label, get]) => {
        const v = Math.round(Number(get(p)) || 0);
        const cls = v >= RED_AT ? 'red' : (v >= AMBER_AT ? 'amber' : '');
        zoneEls[id].forEach(el => {
            el.classList.remove('amber', 'red');
            if (cls) el.classList.add(cls);
        });
        if (cls) found.push({ v, label, cls });
    });
    if (p.m_drsFault === 1) found.push({ v: 100, label: 'DRS fault', cls: 'red', fault: true });
    if (p.m_ersFault === 1) found.push({ v: 100, label: 'ERS fault', cls: 'red', fault: true });
    found.sort((a, b) => b.v - a.v);

    const rows = found.slice(0, 6).map(f =>
        '<div class="row ' + f.cls + '"><span>' + f.label + '</span>' + (f.fault ? '' : '<b>' + f.v + '%</b>') + '</div>');
    if (found.length > 6) rows.push('<div class="row more">+' + (found.length - 6) + ' more</div>');
    const list = rows.join('');
    if (list !== lastList) { damageListEl.innerHTML = list; lastList = list; }

    // Panel only appears (and the dashboard only shrinks) while there is damage
    stageEl.classList.toggle('has-damage', found.length > 0);
}
