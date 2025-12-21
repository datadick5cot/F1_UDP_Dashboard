from ctypes import LittleEndianStructure, Union, c_uint8, c_int8
from ctypes import c_uint16, c_int16, c_uint32, c_uint64, c_float

# =========================================================
# Packet Header (UNCHANGED in F1 25)
# =========================================================

class PacketHeader(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_packetFormat', c_uint16),      # 2025
        ('m_gameYear', c_uint8),            # 25
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


# =========================================================
# Packet 6 – Car Telemetry (UNCHANGED STRUCTURE)
# =========================================================

class CarTelemetryData_2025(LittleEndianStructure):
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


class PacketCarTelemetryData_2025(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_carTelemetryData', CarTelemetryData_2025 * 22),
        ('m_mfdPanelIndex', c_uint8),
        ('m_mfdPanelIndexSecondaryPlayer', c_uint8),
        ('m_suggestedGear', c_int8),
    ]


# =========================================================
# Packet 7 – Car Status (UPDATED FOR F1 25)
# =========================================================

class CarStatusData_2025(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_tractionControl', c_uint8),
        ('m_antiLockBrakes', c_uint8),
        ('m_fuelMix', c_uint8),
        ('m_frontBrakeBias', c_uint8),
        ('m_pitLimiterStatus', c_uint8),

        ('m_fuelInTank', c_float),
        ('m_fuelCapacity', c_float),
        ('m_fuelRemainingLaps', c_float),

        ('m_maxRPM', c_uint16),
        ('m_idleRPM', c_uint16),
        ('m_maxGears', c_uint8),

        ('m_drsAllowed', c_uint8),
        ('m_drsActivationDistance', c_uint16),

        ('m_actualTyreCompound', c_uint8),
        ('m_visualTyreCompound', c_uint8),
        ('m_tyresAgeLaps', c_uint8),

        ('m_vehicleFiaFlags', c_int8),

        # Power unit
        ('m_enginePowerICE', c_float),
        ('m_enginePowerMGUK', c_float),

        # ERS
        ('m_ersStoreEnergy', c_float),
        ('m_ersDeployMode', c_uint8),
        ('m_ersHarvestedThisLapMGUK', c_float),
        ('m_ersHarvestedThisLapMGUH', c_float),
        ('m_ersDeployedThisLap', c_float),

        # NEW IN F1 25 (documented additions)
        ('m_ersAvailableDeployEnergy', c_float),
        ('m_ersMaxDeployEnergy', c_float),

        ('m_networkPaused', c_uint8),
    ]


class PacketCarStatusData_2025(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_carStatusData', CarStatusData_2025 * 22),
    ]


# =========================================================
# Packet 10 – Car Damage (UNCHANGED STRUCTURE)
# =========================================================

class CarDamageData_2025(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_tyresWear', c_float * 4),
        ('m_tyresDamage', c_uint8 * 4),
        ('m_brakesDamage', c_uint8 * 4),
        ('m_frontLeftWingDamage', c_uint8),
        ('m_frontRightWingDamage', c_uint8),
        ('m_rearWingDamage', c_uint8),
        ('m_floorDamage', c_uint8),
        ('m_diffuserDamage', c_uint8),
        ('m_sidepodDamage', c_uint8),
        ('m_drsFault', c_uint8),
        ('m_ersFault', c_uint8),
        ('m_gearBoxDamage', c_uint8),
        ('m_engineDamage', c_uint8),
        ('m_engineMGUKWear', c_uint8),
        ('m_engineESWear', c_uint8),
        ('m_engineCEWear', c_uint8),
        ('m_engineICEWear', c_uint8),
        ('m_engineMGUHWear', c_uint8),
        ('m_engineTCWear', c_uint8),
        ('m_engineBlown', c_uint8),
        ('m_engineSeized', c_uint8),
    ]


class PacketCarDamageData_2025(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_carDamageData', CarDamageData_2025 * 22),
    ]

