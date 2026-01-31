import time
import socket
import random


from F1_2024 import (
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




def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't need to be reachable
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip



@staticmethod
def Motion_build_test_packet():
    pkt = PacketMotionData()
    pkt.m_header.m_packetId = 0
    for i in range(22):
        pkt.m_carMotionData[i].m_worldPositionX = float(i)
        pkt.m_carMotionData[i].m_worldVelocityX = float(i * 2)
    return bytes(pkt)


@staticmethod
def Session_build_test_packet():
    pkt = PacketSessionData()
    pkt.m_header.m_packetId = 1
    pkt.m_weather = 1
    pkt.m_trackTemperature = 30
    pkt.m_airTemperature = 22
    pkt.m_totalLaps = random.randint(10, 20) # Dynamic total laps
    pkt.m_pitStopRejoinPosition = random.randint(1, 22) # Dynamic rejoin position
    return bytes(pkt)

@staticmethod
def lap_build_test_packet():
    pkt = PacketLapData()
    pkt.m_header.m_packetId = 2
    pkt.m_header.m_playerCarIndex = 0 # Assume player is car 0 for test data
    pkt.m_timeTrialRivalCarIdx = 1 # Dummy rival for testing
    for i in range(22):
        pkt.m_lapData[i].m_lastLapTimeInMS = 90000 + i * 100
        pkt.m_lapData[i].m_currentLapNum = random.randint(1, 10)
        pkt.m_lapData[i].m_carPosition = i + 1
        pkt.m_lapData[i].m_deltaToRaceLeaderMinutesPart = random.randint(0, 1) # Random minutes
        pkt.m_lapData[i].m_deltaToRaceLeaderMSPart = random.randint(0, 59999) # Random milliseconds
    return bytes(pkt)

@staticmethod
def event_build_test_packet():
    pkt = PacketEventData()
    pkt.m_header.m_packetId = 3
    pkt.m_eventStringCode[:] = b"FTLP"
    pkt.m_eventDetails.FastestLap.vehicleIdx = 0
    pkt.m_eventDetails.FastestLap.lapTime = 85.3
    pkt.m_eventDetails.StartLights.numLights = 4
    return bytes(pkt)

@staticmethod
def participants_build_test_packet():
    pkt = PacketParticipantsData()
    pkt.m_header.m_packetId = 4
    pkt.m_numActiveCars = random.randint(10, 22) # Dynamic number of active cars
    for i in range(22):
        pkt.m_participants[i].m_name = b"Driver%d" % i
        pkt.m_participants[i].m_driverId = i
    return bytes(pkt)


@staticmethod
def setup_build_test_packet():
    pkt = PacketCarSetupData()
    pkt.m_header.m_packetId = 5
    for i in range(22):
        pkt.m_carSetups[i].m_frontWing = 5
        pkt.m_carSetups[i].m_rearWing = 6
        pkt.m_carSetups[i].m_brakeBias = random.randint(50, 70) # Add random brake bias
    pkt.m_nextFrontWingValue = 7.0
    return bytes(pkt)

@staticmethod
def telemetry_build_test_packet():
    pkt = PacketCarTelemetryData()
    pkt.m_header.m_packetId = 6
    pkt.m_header.m_playerCarIndex = 0 # Assume player is car 0 for test data
    for i in range(22):
        pkt.m_carTelemetryData[i].m_speed = 320
        pkt.m_carTelemetryData[i].m_throttle = random.uniform(0.0, 1.0)
        pkt.m_carTelemetryData[i].m_gear = random.randint(1, 8)
        pkt.m_carTelemetryData[i].m_brake = random.uniform(0.0, 1.0)
        pkt.m_carTelemetryData[i].m_revLightsPercent = random.randint(0, 100)
        pkt.m_carTelemetryData[i].m_revLightsBitValue = random.randint(0, 4095)
        pkt.m_carTelemetryData[i].m_drs = random.randint(0, 1) # DRS on/off
        
    pkt.m_suggestedGear = random.randint(1, 8)
    return bytes(pkt)

@staticmethod
def status_build_test_packet():
    pkt = PacketCarStatusData()
    pkt.m_header.m_packetId = 7
    pkt.m_header.m_playerCarIndex = 0 # Assume player is car 0 for test data
    for i in range(22):
        pkt.m_carStatusData[i].m_fuelRemainingLaps = round(random.uniform(1.0, 20.0), 1)
        pkt.m_carStatusData[i].m_ersDeployMode = random.randint(0, 3) # ERS modes
        pkt.m_carStatusData[i].m_ersStoreEnergy = random.randint(0, 4000000) # Add random ERS energy
        pkt.m_carStatusData[i].m_ersDeployedThisLap = random.randint(0, 4000000)
        pkt.m_carStatusData[i].m_drsAllowed = random.randint(0, 1)
        pkt.m_carStatusData[i].m_vehicleFiaFlags = random.randint(0, 4) # Random flags (0=None, 1=Green, 2=Blue, 3=Yellow, 4=Red)
        
    return bytes(pkt)

@staticmethod
def final_build_test_packet():
    pkt = PacketFinalClassificationData()
    pkt.m_header.m_packetId = 8
    pkt.m_numCars = 22
    for i in range(22):
        pkt.m_classificationData[i].m_position = i + 1
        pkt.m_classificationData[i].m_points = 25 - i
    return bytes(pkt)

@staticmethod
def lobby_build_test_packet():
    pkt = PacketLobbyInfoData()
    pkt.m_header.m_packetId = 9
    pkt.m_numPlayers = 22
    for i in range(22):
        pkt.m_lobbyPlayers[i].m_name = b"Player%d" % i
        pkt.m_lobbyPlayers[i].m_readyStatus = 1
    return bytes(pkt)

@staticmethod
def damage_build_test_packet():
    pkt = PacketCarDamageData()
    pkt.m_header.m_packetId = 10
    for i in range(22):
        pkt.m_carDamageData[i].m_frontLeftWingDamage = 10
        pkt.m_carDamageData[i].m_engineDamage = 5
    return bytes(pkt)

@staticmethod
def session_build_test_packet():
    pkt = PacketSessionHistoryData()
    pkt.m_header.m_packetId = 11
    pkt.m_carIdx = 0
    pkt.m_numLaps = 5
    for i in range(5):
        pkt.m_lapHistoryData[i].m_lapTimeInMS = 90000 + i * 100
    return bytes(pkt)

@staticmethod
def tyres_build_test_packet():
    pkt = PacketTyreSetsData()
    pkt.m_header.m_packetId = 12
    pkt.m_carIdx = 0
    for i in range(20):
        pkt.m_tyreSetData[i].m_actualCompound = 16
        pkt.m_tyreSetData[i].m_wear = 10
    pkt.m_fittedIdx = 0
    return bytes(pkt)

@staticmethod
def motionex_build_test_packet():
    pkt = PacketMotionExData()
    pkt.m_header.m_packetId = 13
    pkt.m_wheelSlipAngle[:] = [0.1, 0.2, 0.3, 0.4]
    return bytes(pkt)

@staticmethod
def tt_build_test_packet():
    pkt = PacketTimeTrialData()
    pkt.m_header.m_packetId = 14
    
    # Player Session Best Data
    pkt.m_playerSessionBestDataSet.m_carIdx = 0
    pkt.m_playerSessionBestDataSet.m_teamId = 6 # Mercedes
    pkt.m_playerSessionBestDataSet.m_lapTimeInMS = random.randint(70000, 90000)
    pkt.m_playerSessionBestDataSet.m_sector1TimeInMS = random.randint(20000, 30000)
    pkt.m_playerSessionBestDataSet.m_sector2TimeInMS = random.randint(20000, 30000)
    pkt.m_playerSessionBestDataSet.m_sector3TimeInMS = random.randint(20000, 30000)
    pkt.m_playerSessionBestDataSet.m_tractionControl = random.randint(0,2)
    pkt.m_playerSessionBestDataSet.m_gearboxAssist = random.randint(1,3)
    pkt.m_playerSessionBestDataSet.m_antiLockBrakes = random.randint(0,1)
    pkt.m_playerSessionBestDataSet.m_equalCarPerformance = 0
    pkt.m_playerSessionBestDataSet.m_customSetup = 1
    pkt.m_playerSessionBestDataSet.m_valid = 1

    # Rival Data
    pkt.m_rivalDataSet.m_carIdx = 1
    pkt.m_rivalDataSet.m_teamId = 0 # Red Bull
    pkt.m_rivalDataSet.m_lapTimeInMS = random.randint(70000, 90000)
    pkt.m_rivalDataSet.m_sector1TimeInMS = random.randint(20000, 30000)
    pkt.m_rivalDataSet.m_sector2TimeInMS = random.randint(20000, 30000)
    pkt.m_rivalDataSet.m_sector3TimeInMS = random.randint(20000, 30000)
    pkt.m_rivalDataSet.m_tractionControl = random.randint(0,2)
    pkt.m_rivalDataSet.m_gearboxAssist = random.randint(1,3)
    pkt.m_rivalDataSet.m_antiLockBrakes = random.randint(0,1)
    pkt.m_rivalDataSet.m_equalCarPerformance = 0
    pkt.m_rivalDataSet.m_customSetup = 1
    pkt.m_rivalDataSet.m_valid = 1
    
    # Personal Best Data (can be similar to player session best for testing)
    pkt.m_personalBestDataSet.m_carIdx = 0
    pkt.m_personalBestDataSet.m_teamId = 6
    pkt.m_personalBestDataSet.m_lapTimeInMS = random.randint(70000, 90000)
    pkt.m_personalBestDataSet.m_sector1TimeInMS = random.randint(20000, 30000)
    pkt.m_personalBestDataSet.m_sector2TimeInMS = random.randint(20000, 30000)
    pkt.m_personalBestDataSet.m_sector3TimeInMS = random.randint(20000, 30000)
    pkt.m_personalBestDataSet.m_tractionControl = random.randint(0,2)
    pkt.m_personalBestDataSet.m_gearboxAssist = random.randint(1,3)
    pkt.m_personalBestDataSet.m_antiLockBrakes = random.randint(0,1)
    pkt.m_personalBestDataSet.m_equalCarPerformance = 0
    pkt.m_personalBestDataSet.m_customSetup = 1
    pkt.m_personalBestDataSet.m_valid = 1

    return bytes(pkt)




UDP_IP = get_local_ip()
UDP_PORT = 20777
DELAY_BETWEEN_PACKETS = 0.01  # seconds

# List of (name, build_function) for all packet types
PACKETS_TO_SEND = [
    ("PacketMotionData", motionex_build_test_packet),
    ("PacketSessionData", session_build_test_packet),
    ("PacketLapData", lap_build_test_packet),
    ("PacketEventData", event_build_test_packet),
    ("PacketParticipantsData", participants_build_test_packet),
    ("PacketCarSetupData", setup_build_test_packet),
    ("PacketCarTelemetryData", telemetry_build_test_packet),
    ("PacketCarStatusData", status_build_test_packet),
    ("PacketFinalClassificationData", final_build_test_packet),
    ("PacketLobbyInfoData", lobby_build_test_packet),
    ("PacketCarDamageData", damage_build_test_packet),
    ("PacketSessionHistoryData", session_build_test_packet),
    ("PacketTyreSetsData", tyres_build_test_packet),
    ("PacketMotionExData", motionex_build_test_packet),
    ("PacketTimeTrialData", tt_build_test_packet),
]

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"Sending test packets to {UDP_IP}:{UDP_PORT}...")

    i = 0
    while i < 1000: # Send more packets for better testing
        for packet_name, build_func in PACKETS_TO_SEND:
            pkt = build_func()
            sock.sendto(pkt, (UDP_IP, UDP_PORT))
            # print(f"Sent {packet_name} ({len(pkt)} bytes)")
            time.sleep(DELAY_BETWEEN_PACKETS)
        i += 1
    print("Finished sending test packets.")

if __name__ == "__main__":
    main()






