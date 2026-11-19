#!/usr/bin/env python3
"""
F1 25 UDP test sender.

Simulates one player car (index 0) plus 21 AI cars driving round a track and sends
every packet type at a realistic rate, with values that change over time so every
part of the dashboard has something to show.

Damage panel test cycle (default 60 s, 5 stages of 12 s):
    0  clean
    1  front wing L amber
    2  front wing L red, floor amber, brake RL amber  (tests amber -> red reappear)
    3  everything damaged + DRS/ERS faults            (tests the "+N more" row)
    4  repaired / clean                               (tests dismissal reset)

Usage:
    python TestSend.py                       # send to this machine's LAN IP, run until Ctrl+C
    python TestSend.py --ip 127.0.0.1
    python TestSend.py --duration 120
    python TestSend.py --damage-cycle 30
    python TestSend.py --skip final lobby    # leave some packet types out

Any field name that doesn't exist in your F1_2025.py is reported once as [warn]
instead of being silently ignored (ctypes accepts misspelt attributes without error).
"""

import argparse
import math
import socket
import time

try:
    from F1_2025 import (
        PacketMotionData,
        PacketSessionData,
        PacketLapData,
        PacketEventData,
        PacketParticipantsData,
        PacketCarSetupData,
        PacketCarTelemetryData,
        PacketCarStatusData,
        PacketFinalClassificationData,
        PacketLobbyInfoData,
        PacketCarDamageData,
        PacketSessionHistoryData,
        PacketTyreSetsData,
        PacketMotionExData,
        PacketTimeTrialData,
    )
except ImportError:
    from UDP.F1_2025 import (
        PacketMotionData,
        PacketSessionData,
        PacketLapData,
        PacketEventData,
        PacketParticipantsData,
        PacketCarSetupData,
        PacketCarTelemetryData,
        PacketCarStatusData,
        PacketFinalClassificationData,
        PacketLobbyInfoData,
        PacketCarDamageData,
        PacketSessionHistoryData,
        PacketTyreSetsData,
        PacketMotionExData,
        PacketTimeTrialData,
    )

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------
UDP_PORT = 20777
NUM_CARS = 22
PLAYER = 0
RIVAL = 1
TOTAL_LAPS = 20
LAP_TIME = 90.0          # seconds for the player to complete a lap
TRACK_LEN = 5800         # metres
TRACK_RX = 800.0         # oval track used for the motion packet (track map)
TRACK_RZ = 500.0

DRIVER_NAMES = [
    "Player", "Verstappen", "Norris", "Leclerc", "Piastri", "Russell", "Hamilton",
    "Sainz", "Alonso", "Gasly", "Albon", "Tsunoda", "Stroll", "Ocon", "Hulkenberg",
    "Lawson", "Bearman", "Antonelli", "Hadjar", "Bortoleto", "Colapinto", "Bottas",
]

# Tyre arrays in the game are [RL, RR, FL, FR]


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
_warned = set()


def put(obj, **fields):
    """Set fields on a ctypes struct. Warn once about names the struct doesn't have."""
    for name, value in fields.items():
        if hasattr(obj, name):
            if isinstance(value, (list, tuple)):
                getattr(obj, name)[:] = value
            else:
                setattr(obj, name, value)
        else:
            key = (type(obj).__name__, name)
            if key not in _warned:
                _warned.add(key)
                print(f"[warn] {key[0]} has no field '{name}' (skipped)")


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def split_ms(ms):
    """Split milliseconds into (ms part within the minute, whole minutes)."""
    ms = max(0, int(ms))
    return ms % 60000, ms // 60000


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))   # doesn't need to be reachable
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


class Sim:
    """Shared clock/frame counter that every packet builder reads."""

    def __init__(self, damage_cycle):
        self.t0 = time.monotonic()
        self.t = 0.0
        self.frame = 0
        self.damage_cycle = damage_cycle
        self.event_idx = 0
        self.history_toggle = 0

    def tick(self):
        self.t = time.monotonic() - self.t0
        self.frame += 1


def hdr(pkt, packet_id, sim):
    put(
        pkt.m_header,
        m_packetFormat=2025,
        m_gameYear=25,
        m_gameMajorVersion=1,
        m_gameMinorVersion=0,
        m_packetVersion=1,
        m_packetId=packet_id,
        m_sessionUID=0xF125F125,
        m_sessionTime=float(sim.t),
        m_frameIdentifier=sim.frame,
        m_overallFrameIdentifier=sim.frame,
        m_playerCarIndex=PLAYER,
        m_secondaryPlayerCarIndex=255,
    )


# --------------------------------------------------------------------------
# Driving model (one function drives every packet so the data is consistent)
# --------------------------------------------------------------------------
def drive(t, i):
    """State of car i at session time t."""
    lap_time = LAP_TIME + i * 0.05
    tt = max(t - i * 0.6, 0.0)
    lap_frac = (tt / lap_time) % 1.0
    lap_num = int(tt / lap_time) % TOTAL_LAPS + 1

    phase = 2 * math.pi * 6 * lap_frac + i
    s, c = math.sin(phase), math.cos(phase)

    speed = int(200 + 110 * s)                       # 90..310 km/h
    throttle = clamp(0.55 + 1.2 * c, 0.0, 1.0)
    brake = clamp(-1.2 * c - 0.35, 0.0, 1.0)
    steer = 0.8 * math.sin(phase * 0.5)
    gear = int(clamp(1 + speed // 40, 1, 8))
    rpm = int(clamp(4500 + (speed % 40) / 40 * 7500, 4500, 12000))
    drs_allowed = int((tt // 10) % 2 == 0)
    drs = int(drs_allowed and speed > 250 and brake == 0)

    return dict(
        tt=tt, lap_frac=lap_frac, lap_num=lap_num, speed=speed, throttle=throttle,
        brake=brake, steer=steer, gear=gear, rpm=rpm, drs_allowed=drs_allowed, drs=drs,
    )


def grid_positions(t):
    """Race positions. The player swaps between P3 and P6 every 20 s."""
    player_pos = 3 + int(t // 20) % 4
    free = [p for p in range(1, NUM_CARS + 1) if p != player_pos]
    pos = {PLAYER: player_pos}
    for car, p in zip(range(1, NUM_CARS), free):
        pos[car] = p
    return pos


def damage_stage(sim):
    return int((sim.t % sim.damage_cycle) / (sim.damage_cycle / 5))


def damage_profile(stage):
    z = dict(fwl=0, fwr=0, rw=0, floor=0, side=0, diff=0, gear=0, eng=0,
             brakes=[0, 0, 0, 0], drs=0, ers=0)
    if stage == 1:
        z.update(fwl=35)
    elif stage == 2:
        z.update(fwl=55, floor=32, brakes=[40, 0, 0, 0])
    elif stage == 3:
        z.update(fwl=60, fwr=52, rw=38, floor=70, side=33, diff=41, gear=45, eng=55,
                 brakes=[45, 60, 35, 52], drs=1, ers=1)
    return z


def pit_window(t):
    """True for 6 s out of every 60 s (pit limiter / pit status on)."""
    return 20 <= (t % 60) < 26


# --------------------------------------------------------------------------
# Packet builders
# --------------------------------------------------------------------------
def build_motion(sim):
    pkt = PacketMotionData()
    hdr(pkt, 0, sim)
    for i in range(NUM_CARS):
        d = drive(sim.t, i)
        theta = 2 * math.pi * d["lap_frac"]
        v = d["speed"] / 3.6
        yaw = math.atan2(math.sin(theta + math.pi / 2), math.cos(theta + math.pi / 2))
        put(
            pkt.m_carMotionData[i],
            m_worldPositionX=TRACK_RX * math.cos(theta),
            m_worldPositionY=0.0,
            m_worldPositionZ=TRACK_RZ * math.sin(theta),
            m_worldVelocityX=-v * math.sin(theta),
            m_worldVelocityY=0.0,
            m_worldVelocityZ=v * math.cos(theta),
            m_gForceLateral=d["steer"] * 3.0,
            m_gForceLongitudinal=(d["throttle"] - d["brake"] * 2) * 1.5,
            m_gForceVertical=1.0,
            m_yaw=yaw,
            m_pitch=0.0,
            m_roll=d["steer"] * 0.05,
        )
    return pkt


def build_session(sim):
    pkt = PacketSessionData()
    hdr(pkt, 1, sim)
    weather = int(sim.t // 30) % 6          # 0 clear .. 5 storm, changes every 30 s
    cycle = sim.t % 120
    safety_car = 1 if 40 <= cycle < 48 else (2 if 80 <= cycle < 88 else 0)  # SC / VSC

    put(
        pkt,
        m_weather=weather,
        m_trackTemperature=int(30 + 5 * math.sin(sim.t / 20)),
        m_airTemperature=int(22 + 3 * math.sin(sim.t / 25)),
        m_totalLaps=TOTAL_LAPS,
        m_trackLength=TRACK_LEN,
        m_sessionType=15,                   # race
        m_trackId=0,
        m_formula=0,
        m_sessionTimeLeft=int(max(0, 3600 - sim.t)),
        m_sessionDuration=3600,
        m_pitSpeedLimit=80,
        m_gamePaused=0,
        m_isSpectating=0,
        m_networkGame=0,
        m_safetyCarStatus=safety_car,
        m_pitStopRejoinPosition=1 + int(sim.t // 3) % NUM_CARS,
        m_numWeatherForecastSamples=5,
    )
    for k in range(5):
        w = (weather + k) % 6
        put(
            pkt.m_weatherForecastSamples[k],
            m_sessionType=15,
            m_timeOffset=k * 5,
            m_weather=w,
            m_trackTemperature=28 - w,
            m_airTemperature=21 - w // 2,
            m_rainPercentage=min(100, w * 20),
        )
    return pkt


def gap_to_car_ahead(pos, t):
    """Gap in ms to the car one place ahead (0 for the leader). Varies over time."""
    if pos <= 1:
        return 0
    return int(1300 + 600 * math.sin(t / 6 + pos))


def gap_to_leader(pos, t):
    """Cumulative gap in ms to the leader, consistent with gap_to_car_ahead."""
    return sum(gap_to_car_ahead(k, t) for k in range(2, pos + 1))


def build_lap(sim):
    pkt = PacketLapData()
    hdr(pkt, 2, sim)
    put(pkt, m_timeTrialPBCarIdx=PLAYER, m_timeTrialRivalCarIdx=RIVAL)
    pos = grid_positions(sim.t)
    in_pit = pit_window(sim.t)

    for i in range(NUM_CARS):
        d = drive(sim.t, i)
        p = pos[i]
        lap_ms = int(d["lap_frac"] * (LAP_TIME + i * 0.05) * 1000)
        last_lap = 0 if d["lap_num"] == 1 else 90000 + i * 100 + (d["lap_num"] * 37 + i * 11) % 800
        sector = int(d["lap_frac"] * 3)
        s_ms = int((LAP_TIME + i * 0.05) * 1000 / 3)

        front_ms, front_min = split_ms(gap_to_car_ahead(p, sim.t))
        lead_ms, lead_min = split_ms(gap_to_leader(p, sim.t))
        s1_ms, s1_min = split_ms(s_ms)
        s2_ms, s2_min = split_ms(s_ms)

        player = i == PLAYER
        put(
            pkt.m_lapData[i],
            m_lastLapTimeInMS=last_lap,
            m_currentLapTimeInMS=lap_ms,
            m_sector1TimeMSPart=s1_ms,
            m_sector1TimeMinutesPart=s1_min,
            m_sector2TimeMSPart=s2_ms,
            m_sector2TimeMinutesPart=s2_min,
            m_deltaToCarInFrontMSPart=front_ms,
            m_deltaToCarInFrontMinutesPart=front_min,
            m_deltaToRaceLeaderMSPart=lead_ms,
            m_deltaToRaceLeaderMinutesPart=lead_min,
            m_lapDistance=float(d["lap_frac"] * TRACK_LEN),
            m_totalDistance=float((d["lap_num"] - 1 + d["lap_frac"]) * TRACK_LEN),
            m_safetyCarDelta=0.0,
            m_carPosition=p,
            m_currentLapNum=d["lap_num"],
            m_pitStatus=(1 if (player and in_pit) else 0),
            m_numPitStops=int(sim.t // 60) if player else 0,
            m_sector=sector,
            m_currentLapInvalid=int(player and d["lap_num"] % 5 == 0),
            m_penalties=(5 if (player and d["lap_num"] % 4 == 0) else 0),
            m_totalWarnings=(d["lap_num"] % 3 if player else 0),
            m_cornerCuttingWarnings=(d["lap_num"] % 3 if player else 0),
            m_numUnservedDriveThroughPens=0,
            m_numUnservedStopGoPens=0,
            m_gridPosition=i + 1,
            m_driverStatus=4,               # on track
            m_resultStatus=2,               # active
            m_pitLaneTimerActive=int(player and in_pit),
            m_pitLaneTimeInLaneInMS=(int((sim.t % 60 - 20) * 1000) if (player and in_pit) else 0),
            m_pitStopTimerInMS=(int((sim.t % 60 - 20) * 500) if (player and in_pit) else 0),
            m_pitStopShouldServePen=0,
            m_speedTrapFastestSpeed=int(300 + i % 8),
            m_speedTrapFastestLap=d["lap_num"],
        )
    return pkt


# Event code -> {union member: {field: value}}
EVENTS = [
    (b"STLG", {"StartLights": {"numLights": 5}}),
    (b"LGOT", {}),
    (b"FTLP", {"FastestLap": {"vehicleIdx": 0, "lapTime": 85.3}}),
    (b"SPTP", {"SpeedTrap": {"vehicleIdx": 0, "speed": 328.4, "isOverallFastestInSession": 1,
                             "isDriverFastestInSession": 1, "fastestVehicleIdxInSession": 0,
                             "fastestSpeedInSession": 328.4}}),
    (b"DRSE", {}),
    (b"OVTK", {"Overtake": {"overtakingVehicleIdx": 0, "beingOvertakenVehicleIdx": 4}}),
    (b"PENA", {"Penalty": {"penaltyType": 5, "infringementType": 7, "vehicleIdx": 0,
                           "otherVehicleIdx": 255, "time": 5, "lapNum": 3, "placesGained": 0}}),
    (b"COLL", {"Collision": {"vehicle1Idx": 0, "vehicle2Idx": 5}}),
    (b"SCAR", {"SafetyCar": {"safetyCarType": 1, "eventType": 0}}),
    (b"DRSD", {}),
]


def build_event(sim):
    code, details = EVENTS[sim.event_idx % len(EVENTS)]
    sim.event_idx += 1
    pkt = PacketEventData()
    hdr(pkt, 3, sim)
    pkt.m_eventStringCode[:] = code
    for group, fields in details.items():
        if hasattr(pkt.m_eventDetails, group):
            put(getattr(pkt.m_eventDetails, group), **fields)
        else:
            key = ("m_eventDetails", group)
            if key not in _warned:
                _warned.add(key)
                print(f"[warn] m_eventDetails has no member '{group}' (skipped)")
    return pkt


def build_participants(sim):
    pkt = PacketParticipantsData()
    hdr(pkt, 4, sim)
    put(pkt, m_numActiveCars=NUM_CARS)
    for i in range(NUM_CARS):
        put(
            pkt.m_participants[i],
            m_aiControlled=int(i != PLAYER),
            m_driverId=i,
            m_networkId=i,
            m_teamId=i // 2,
            m_myTeam=0,
            m_raceNumber=i + 1,
            m_nationality=i % 40,
            m_name=DRIVER_NAMES[i].encode(),
            m_yourTelemetry=1,
            m_showOnlineNames=1,
            m_techLevel=1000,
            m_platform=1,
        )
    return pkt


def build_setup(sim):
    pkt = PacketCarSetupData()
    hdr(pkt, 5, sim)
    for i in range(NUM_CARS):
        put(
            pkt.m_carSetups[i],
            m_frontWing=5, m_rearWing=6,
            m_onThrottle=60, m_offThrottle=50,
            m_frontCamber=-3.0, m_rearCamber=-1.5,
            m_frontToe=0.05, m_rearToe=0.20,
            m_frontSuspension=5, m_rearSuspension=5,
            m_frontAntiRollBar=6, m_rearAntiRollBar=6,
            m_frontSuspensionHeight=20, m_rearSuspensionHeight=30,
            m_brakePressure=100,
            m_brakeBias=int(60 + 8 * math.sin(sim.t / 10)),     # 52..68
            m_engineBraking=50,
            m_frontLeftTyrePressure=23.0, m_frontRightTyrePressure=23.0,
            m_rearLeftTyrePressure=21.5, m_rearRightTyrePressure=21.5,
            m_ballast=5,
            m_fuelLoad=100.0,
        )
    put(pkt, m_nextFrontWingValue=7.0)
    return pkt


def build_telemetry(sim):
    pkt = PacketCarTelemetryData()
    hdr(pkt, 6, sim)
    for i in range(NUM_CARS):
        d = drive(sim.t, i)
        pct = int(clamp((d["rpm"] - 9000) / 3000 * 100, 0, 100))
        leds = (1 << int(pct / 100 * 15)) - 1                   # 15 rev lights
        hot = int(80 + 20 * d["throttle"])
        put(
            pkt.m_carTelemetryData[i],
            m_speed=d["speed"],
            m_throttle=float(d["throttle"]),
            m_steer=float(d["steer"]),
            m_brake=float(d["brake"]),
            m_clutch=0,
            m_gear=d["gear"],
            m_engineRPM=d["rpm"],
            m_drs=d["drs"],
            m_revLightsPercent=pct,
            m_revLightsBitValue=leds,
            m_brakesTemperature=[int(300 + d["brake"] * 600)] * 4,
            m_tyresSurfaceTemperature=[hot, hot, hot + 3, hot + 3],
            m_tyresInnerTemperature=[hot + 10, hot + 10, hot + 12, hot + 12],
            m_engineTemperature=int(105 + 8 * d["throttle"]),
            m_tyresPressure=[21.5, 21.6, 23.0, 23.1],
            m_surfaceType=[0, 0, 0, 0],
        )
    d0 = drive(sim.t, PLAYER)
    put(
        pkt,
        m_mfdPanelIndex=255,
        m_mfdPanelIndexSecondaryPlayer=255,
        m_suggestedGear=(min(8, d0["gear"] + 1) if d0["rpm"] > 11500 else 0),
    )
    return pkt


def build_status(sim):
    pkt = PacketCarStatusData()
    hdr(pkt, 7, sim)
    flag = int(sim.t // 8) % 4                  # 0 none, 1 green, 2 blue, 3 yellow
    in_pit = pit_window(sim.t)
    for i in range(NUM_CARS):
        d = drive(sim.t, i)
        tank = max(5.0, 100.0 - sim.t * 0.08)
        harvest = d["lap_frac"]
        player = i == PLAYER
        put(
            pkt.m_carStatusData[i],
            m_tractionControl=2,
            m_antiLockBrakes=1,
            m_fuelMix=1,
            m_frontBrakeBias=int(60 + 8 * math.sin(sim.t / 10)),
            m_pitLimiterStatus=int(player and in_pit),
            m_fuelInTank=float(tank),
            m_fuelCapacity=110.0,
            m_fuelRemainingLaps=float(round(tank / 1.7, 1)),
            m_maxRPM=13000,
            m_idleRPM=4000,
            m_maxGears=8,
            m_drsAllowed=d["drs_allowed"],
            m_drsActivationDistance=0,
            m_actualTyreCompound=16,
            m_visualTyreCompound=16,
            m_tyresAgeLaps=int(sim.t // 90) % 20,
            m_vehicleFiaFlags=(flag if player else 0),
            m_enginePowerICE=float(400000 + 80000 * d["throttle"]),
            m_enginePowerMGUK=float(120000 * d["throttle"]),
            m_ersStoreEnergy=float(2000000 + 1900000 * math.sin(sim.t / 7)),
            m_ersDeployMode=int(sim.t // 10) % 4,    # 0 none, 1 medium, 2 hotlap, 3 overtake
            m_ersHarvestedThisLapMGUK=float(harvest * 1500000),
            m_ersHarvestedThisLapMGUH=float(harvest * 700000),
            m_ersDeployedThisLap=float(harvest * 3500000),
            m_networkPaused=0,
        )
    return pkt


def build_final(sim):
    pkt = PacketFinalClassificationData()
    hdr(pkt, 8, sim)
    put(pkt, m_numCars=NUM_CARS)
    points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
    for i in range(NUM_CARS):
        put(
            pkt.m_classificationData[i],
            m_position=i + 1,
            m_numLaps=TOTAL_LAPS,
            m_gridPosition=i + 1,
            m_points=points[i] if i < len(points) else 0,
            m_numPitStops=1,
            m_resultStatus=3,
            m_bestLapTimeInMS=88000 + i * 150,
            m_totalRaceTime=1800.0 + i * 3.5,
            m_penaltiesTime=0,
            m_numPenalties=0,
            m_numTyreStints=2,
            m_tyreStintsActual=[16, 18, 0, 0, 0, 0, 0, 0],
            m_tyreStintsVisual=[16, 18, 0, 0, 0, 0, 0, 0],
            m_tyreStintsEndLaps=[10, 20, 0, 0, 0, 0, 0, 0],
        )
    return pkt


def build_lobby(sim):
    pkt = PacketLobbyInfoData()
    hdr(pkt, 9, sim)
    put(pkt, m_numPlayers=NUM_CARS)
    for i in range(NUM_CARS):
        put(
            pkt.m_lobbyPlayers[i],
            m_aiControlled=int(i != PLAYER),
            m_teamId=i // 2,
            m_nationality=i % 40,
            m_platform=1,
            m_name=DRIVER_NAMES[i].encode(),
            m_carNumber=i + 1,
            m_yourTelemetry=1,
            m_showOnlineNames=1,
            m_techLevel=1000,
            m_readyStatus=1,
        )
    return pkt


def build_damage(sim):
    pkt = PacketCarDamageData()
    hdr(pkt, 10, sim)
    stage = damage_stage(sim)
    z = damage_profile(stage)
    stint_wear = (sim.t % 180) * 0.45                       # 0..81 %, resets each "stint"

    for i in range(NUM_CARS):
        wear = [clamp(stint_wear * f, 0, 100) for f in (1.0, 1.05, 1.10, 1.15)]
        if i == PLAYER:
            put(
                pkt.m_carDamageData[i],
                m_tyresWear=[float(w) for w in wear],
                m_tyresDamage=[int(w * 0.5) for w in wear],
                m_brakesDamage=z["brakes"],
                m_tyreBlisters=[int(w * 0.2) for w in wear],
                m_frontLeftWingDamage=z["fwl"],
                m_frontRightWingDamage=z["fwr"],
                m_rearWingDamage=z["rw"],
                m_floorDamage=z["floor"],
                m_diffuserDamage=z["diff"],
                m_sidepodDamage=z["side"],
                m_drsFault=z["drs"],
                m_ersFault=z["ers"],
                m_gearBoxDamage=z["gear"],
                m_engineDamage=z["eng"],
                m_engineMGUHWear=int(sim.t // 10) % 100,
                m_engineESWear=int(sim.t // 12) % 100,
                m_engineCEWear=int(sim.t // 14) % 100,
                m_engineICEWear=int(sim.t // 16) % 100,
                m_engineMGUKWear=int(sim.t // 18) % 100,
                m_engineTCWear=int(sim.t // 20) % 100,
                m_engineBlown=0,
                m_engineSeized=0,
            )
        else:
            put(
                pkt.m_carDamageData[i],
                m_tyresWear=[float(w) for w in wear],
                m_frontLeftWingDamage=i % 10,
                m_engineDamage=i % 6,
            )
    return pkt


def build_history(sim):
    pkt = PacketSessionHistoryData()
    hdr(pkt, 11, sim)
    car = (PLAYER, RIVAL)[sim.history_toggle % 2]            # alternate player / rival
    sim.history_toggle += 1
    laps_done = min(100, int(sim.t / LAP_TIME))
    put(
        pkt,
        m_carIdx=car,
        m_numLaps=laps_done,
        m_numTyreStints=1,
        m_bestLapTimeLapNum=1 if laps_done else 0,
        m_bestSector1LapNum=1 if laps_done else 0,
        m_bestSector2LapNum=1 if laps_done else 0,
        m_bestSector3LapNum=1 if laps_done else 0,
    )
    for n in range(laps_done):
        base = 90000 + car * 100 + (n * 53) % 700
        put(
            pkt.m_lapHistoryData[n],
            m_lapTimeInMS=base,
            m_sector1TimeInMS=base // 3,
            m_sector1TimeMinutesPart=0,
            m_sector2TimeInMS=base // 3,
            m_sector2TimeMinutesPart=0,
            m_sector3TimeInMS=base - 2 * (base // 3),
            m_sector3TimeMinutesPart=0,
            m_lapValidBitFlags=15,
        )
    put(
        pkt.m_tyreStintsHistoryData[0],
        m_endLap=255, m_tyreActualCompound=16, m_tyreVisualCompound=16,
    )
    return pkt


def build_tyres(sim):
    pkt = PacketTyreSetsData()
    hdr(pkt, 12, sim)
    stint_wear = int((sim.t % 180) * 0.45)
    compounds = [16, 17, 18]                                 # soft, medium, hard (visual)
    actual = [16, 17, 18]
    put(pkt, m_carIdx=PLAYER, m_fittedIdx=0)
    for k in range(20):
        c = k % 3
        fitted = int(k == 0)
        put(
            pkt.m_tyreSetData[k],
            m_actualTyreCompound=actual[c],
            m_visualTyreCompound=compounds[c],
            m_wear=stint_wear if fitted else (k * 3) % 40,
            m_available=1,
            m_recommendedSession=15,
            m_lifeSpan=max(0, 25 - stint_wear // 4),
            m_usableLife=25,
            m_lapDeltaTime=c * 400,
            m_fitted=fitted,
        )
    return pkt


def build_motionex(sim):
    pkt = PacketMotionExData()
    hdr(pkt, 13, sim)
    d = drive(sim.t, PLAYER)
    v = d["speed"] / 3.6
    put(
        pkt,
        m_suspensionPosition=[5.0, 5.0, 4.0, 4.0],
        m_suspensionVelocity=[0.0, 0.0, 0.0, 0.0],
        m_suspensionAcceleration=[0.0, 0.0, 0.0, 0.0],
        m_wheelSpeed=[v, v, v, v],
        m_wheelSlipRatio=[0.02 * d["throttle"]] * 4,
        m_wheelSlipAngle=[abs(d["steer"]) * 0.1, abs(d["steer"]) * 0.1,
                          abs(d["steer"]) * 0.15, abs(d["steer"]) * 0.15],
        m_wheelLatForce=[d["steer"] * 3000.0] * 4,
        m_wheelLongForce=[(d["throttle"] - d["brake"]) * 2500.0] * 4,
        m_heightOfCOGAboveGround=0.03,
        m_localVelocityX=0.0,
        m_localVelocityY=0.0,
        m_localVelocityZ=v,
        m_frontWheelsAngle=d["steer"] * 0.3,
        m_wheelVertForce=[3000.0, 3000.0, 2800.0, 2800.0],
    )
    return pkt


def _tt_set(ds, car, team, sim):
    lap = 80000 + int(5000 * math.sin(sim.t / 9 + car))
    put(
        ds,
        m_carIdx=car,
        m_teamId=team,
        m_lapTimeInMS=lap,
        m_sector1TimeInMS=lap // 3,
        m_sector2TimeInMS=lap // 3,
        m_sector3TimeInMS=lap - 2 * (lap // 3),
        m_tractionControl=int(sim.t // 5) % 3,
        m_gearboxAssist=1 + int(sim.t // 7) % 3,
        m_antiLockBrakes=int(sim.t // 11) % 2,
        m_equalCarPerformance=0,
        m_customSetup=1,
        m_valid=1,
    )


def build_timetrial(sim):
    pkt = PacketTimeTrialData()
    hdr(pkt, 14, sim)
    _tt_set(pkt.m_playerSessionBestDataSet, PLAYER, 6, sim)
    _tt_set(pkt.m_rivalDataSet, RIVAL, 0, sim)
    _tt_set(pkt.m_personalBestDataSet, PLAYER, 6, sim)
    return pkt


# --------------------------------------------------------------------------
# Scheduler
# --------------------------------------------------------------------------
# key, builder, rate in Hz
PACKETS = [
    ("motion", build_motion, 30),
    ("session", build_session, 2),
    ("lap", build_lap, 20),
    ("event", build_event, 0.25),
    ("participants", build_participants, 0.5),
    ("setup", build_setup, 2),
    ("telemetry", build_telemetry, 30),
    ("status", build_status, 10),
    ("final", build_final, 0.05),
    ("lobby", build_lobby, 0.05),
    ("damage", build_damage, 10),
    ("history", build_history, 5),
    ("tyres", build_tyres, 5),
    ("motionex", build_motionex, 30),
    ("timetrial", build_timetrial, 1),
]


def main():
    keys = [k for k, _, _ in PACKETS]
    ap = argparse.ArgumentParser(description="F1 25 UDP dashboard test sender")
    ap.add_argument("--ip", default=None, help="destination IP (default: this machine's LAN IP)")
    ap.add_argument("--port", type=int, default=UDP_PORT)
    ap.add_argument("--duration", type=float, default=0, help="seconds to run (0 = until Ctrl+C)")
    ap.add_argument("--damage-cycle", type=float, default=60, help="seconds per damage test cycle")
    ap.add_argument("--skip", nargs="*", default=[], choices=keys, help="packet types to leave out")
    args = ap.parse_args()

    ip = args.ip or get_local_ip()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sim = Sim(args.damage_cycle)
    schedule = [[k, fn, 1.0 / hz, 0.0] for k, fn, hz in PACKETS if k not in args.skip]

    print(f"Sending test packets to {ip}:{args.port} (Ctrl+C to stop)")
    print(f"Damage test cycle: {args.damage_cycle:.0f}s")
    last_stage = -1
    try:
        while True:
            sim.tick()
            if args.duration and sim.t >= args.duration:
                break

            stage = damage_stage(sim)
            if stage != last_stage:
                print(f"[{sim.t:6.1f}s] damage stage {stage}")
                last_stage = stage

            now = time.monotonic()
            for item in schedule:
                key, builder, interval, due = item
                if now >= due:
                    sock.sendto(bytes(builder(sim)), (ip, args.port))
                    item[3] = max(due + interval, now) if due else now + interval
            time.sleep(0.004)
    except KeyboardInterrupt:
        pass
    finally:
        sock.close()
        print("Stopped.")


if __name__ == "__main__":
    main()
