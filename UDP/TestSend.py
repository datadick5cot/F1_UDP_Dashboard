import time
import socket


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
    pkt.m_totalLaps = 5
    return bytes(pkt)

@staticmethod
def lap_build_test_packet():
    pkt = PacketLapData()
    pkt.m_header.m_packetId = 2
    for i in range(22):
        pkt.m_lapData[i].m_lastLapTimeInMS = 90000 + i * 100
        pkt.m_lapData[i].m_currentLapNum = 3
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
    pkt.m_numActiveCars = 22
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
    pkt.m_nextFrontWingValue = 7.0
    return bytes(pkt)

@staticmethod
def telemetry_build_test_packet():
    pkt = PacketCarTelemetryData()
    pkt.m_header.m_packetId = 6
    for i in range(22):
        pkt.m_carTelemetryData[i].m_speed = 320
        pkt.m_carTelemetryData[i].m_throttle = 0.8
        pkt.m_carTelemetryData[i].m_gear = 7
        pkt.m_carTelemetryData[i].m_brake = 0.5
        pkt.m_carTelemetryData[i].m_revLightsPercent = 90
        pkt.m_carTelemetryData[i].m_revLightsBitValue = 3000
        pkt.m_carTelemetryData[i].m_drs = 0
        
    pkt.m_suggestedGear = 6
    return bytes(pkt)

@staticmethod
def status_build_test_packet():
    pkt = PacketCarStatusData()
    pkt.m_header.m_packetId = 7
    for i in range(22):
        pkt.m_carStatusData[i].m_fuelRemainingLaps = 7
        pkt.m_carStatusData[i].m_ersStoreEnergy = 4000000
        pkt.m_carStatusData[i].m_ersDeployMode = 3
        pkt.m_carStatusData[i].m_drsAllowed = 1
        
        
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
    pkt.m_playerSessionBestDataSet.m_bestLapTime = 85.3
    pkt.m_rivalDataSet.m_bestLapTime = 86.1
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
    while i < 100:
        for packet_name, build_func in PACKETS_TO_SEND:
            pkt = build_func()
            sock.sendto(pkt, (UDP_IP, UDP_PORT))
            print(f"Sent {packet_name} ({len(pkt)} bytes)")
            time.sleep(DELAY_BETWEEN_PACKETS)
            i += 1

if __name__ == "__main__":
    main()






