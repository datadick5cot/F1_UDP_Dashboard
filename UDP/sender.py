import socket
import time

from telemetry import (
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

UDP_IP = "127.0.0.1"
UDP_PORT = 20777
DELAY_BETWEEN_PACKETS = 0.5  # seconds

# List of (name, build_function) for all packet types
PACKETS_TO_SEND = [
    ("PacketMotionData", PacketMotionData.build_test_packet),
    ("PacketSessionData", PacketSessionData.build_test_packet),
    ("PacketLapData", PacketLapData.build_test_packet),
    ("PacketEventData", PacketEventData.build_test_packet),
    ("PacketParticipantsData", PacketParticipantsData.build_test_packet),
    ("PacketCarSetupData", PacketCarSetupData.build_test_packet),
    ("PacketCarTelemetryData", PacketCarTelemetryData.build_test_packet),
    ("PacketCarStatusData", PacketCarStatusData.build_test_packet),
    ("PacketFinalClassificationData", PacketFinalClassificationData.build_test_packet),
    ("PacketLobbyInfoData", PacketLobbyInfoData.build_test_packet),
    ("PacketCarDamageData", PacketCarDamageData.build_test_packet),
    ("PacketSessionHistoryData", PacketSessionHistoryData.build_test_packet),
    ("PacketTyreSetsData", PacketTyreSetsData.build_test_packet),
    ("PacketMotionExData", PacketMotionExData.build_test_packet),
    ("PacketTimeTrialData", PacketTimeTrialData.build_test_packet),
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
