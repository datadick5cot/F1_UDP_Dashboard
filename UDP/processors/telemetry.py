from ctypes import LittleEndianStructure, Union, c_uint8, c_int8, c_uint16, c_int16, c_uint32, c_uint64, c_float, c_double, c_char

import time
from ctypes import Array

class PacketHeader(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_packetFormat', c_uint16),
        ('m_gameYear', c_uint8),
        ('m_gameMajorVersion', c_uint8),
        ('m_gameMinorVersion', c_uint8),
        ('m_packetVersion', c_uint8),
        ('m_packetId', c_uint8),
        ('m_sessionUID', c_uint64),
        ('m_sessionTime', c_float),
        ('m_frameIdentifier', c_uint32),
        ('m_overallFrameIdentifier', c_uint32),
        ('m_playerCarIndex', c_uint8),
        ('m_secondaryPlayerCarIndex', c_uint8),
    ]

class CarTelemetryData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_speed', c_uint16),
        ('m_throttle', c_float),
        ('m_steer', c_float),
        ('m_brake', c_float),
        ('m_clutch', c_uint8),
        ('m_gear', c_int8),
        ('m_engineRPM', c_uint16),
        ('m_drs', c_uint8),
        ('m_revLightsPercent', c_uint8),
        ('m_revLightsBitValue', c_uint16),
        ('m_brakesTemperature', c_uint16 * 4),
        ('m_tyresSurfaceTemperature', c_uint8 * 4),
        ('m_tyresInnerTemperature', c_uint8 * 4),
        ('m_engineTemperature', c_uint16),
        ('m_tyresPressure', c_float * 4),
        ('m_surfaceType', c_uint8 * 4),
    ]

class PacketCarTelemetryData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_carTelemetryData', CarTelemetryData * 22),
        ('m_mfdPanelIndex', c_uint8),
        ('m_mfdPanelIndexSecondaryPlayer', c_uint8),
        ('m_suggestedGear', c_int8),
    ]


def process_telemetry(queue, stop_event):
    while not stop_event.is_set():
        try:
            raw = queue.get(timeout=1)
            packet = PacketCarTelemetryData.from_buffer_copy(raw)
            car = packet.m_carTelemetryData[packet.m_header.m_playerCarIndex]
            print(f"[Telemetry] Speed: {car.m_speed}, Gear: {car.m_gear}")
        except Exception as e:
            print(f"Telemetry error: {e}")
