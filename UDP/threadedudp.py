from ctypes import LittleEndianStructure, Union, c_uint8, c_int8, c_uint16, c_int16, c_uint32, c_uint64, c_float, c_double, c_char

import time
from ctypes import Array
# -------------------- Packet Header --------------------
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

# class PacketHeader(LittleEndianStructure):
#     _pack_ = 1
#     _fields_ = [
#         ("m_packetFormat", c_uint16),
#         ("m_gameYear", c_uint8),
#         ("m_gameMajorVersion", c_uint8),
#         ("m_gameMinorVersion", c_uint8),
#         ("m_packetVersion", c_uint8),
#         ("m_packetId", c_uint8),
#         ("m_sessionUID", c_uint64),
#         ("m_sessionTime", c_float),
#         ("m_frameIdentifier", c_uint32),
#         ("m_overallFrameIdentifier", c_uint32),
#         ("m_playerCarIndex", c_uint8),
#         ("m_secondaryPlayerCarIndex", c_uint8),
#     ]

# -------------------- Packet 0: Motion --------------------
class CarMotionData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_worldPositionX', c_float),
        ('m_worldPositionY', c_float),
        ('m_worldPositionZ', c_float),
        ('m_worldVelocityX', c_float),
        ('m_worldVelocityY', c_float),
        ('m_worldVelocityZ', c_float),
        ('m_worldForwardDirX', c_int16),
        ('m_worldForwardDirY', c_int16),
        ('m_worldForwardDirZ', c_int16),
        ('m_worldRightDirX', c_int16),
        ('m_worldRightDirY', c_int16),
        ('m_worldRightDirZ', c_int16),
        ('m_gForceLateral', c_float),
        ('m_gForceLongitudinal', c_float),
        ('m_gForceVertical', c_float),
        ('m_yaw', c_float),
        ('m_pitch', c_float),
        ('m_roll', c_float),
    ]

class PacketMotionData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_carMotionData', CarMotionData * 22),
    ]

# -------------------- Packet 1: Session --------------------
class MarshalZone(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_zoneStart', c_float),
        ('m_zoneFlag', c_int8),
    ]

class WeatherForecastSample(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_sessionType', c_uint8),
        ('m_timeOffset', c_uint8),
        ('m_weather', c_uint8),
        ('m_trackTemperature', c_int8),
        ('m_trackTemperatureChange', c_int8),
        ('m_airTemperature', c_int8),
        ('m_airTemperatureChange', c_int8),
        ('m_rainPercentage', c_uint8),
    ]

class PacketSessionData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_weather', c_uint8),
        ('m_trackTemperature', c_int8),
        ('m_airTemperature', c_int8),
        ('m_totalLaps', c_uint8),
        ('m_trackLength', c_uint16),
        ('m_sessionType', c_uint8),
        ('m_trackId', c_int8),
        ('m_formula', c_uint8),
        ('m_sessionTimeLeft', c_uint16),
        ('m_sessionDuration', c_uint16),
        ('m_pitSpeedLimit', c_uint8),
        ('m_gamePaused', c_uint8),
        ('m_isSpectating', c_uint8),
        ('m_spectatorCarIndex', c_uint8),
        ('m_sliProNativeSupport', c_uint8),
        ('m_numMarshalZones', c_uint8),
        ('m_marshalZones', MarshalZone * 21),
        ('m_safetyCarStatus', c_uint8),
        ('m_networkGame', c_uint8),
        ('m_numWeatherForecastSamples', c_uint8),
        ('m_weatherForecastSamples', WeatherForecastSample * 64),
        ('m_forecastAccuracy', c_uint8),
        ('m_aiDifficulty', c_uint8),
        ('m_seasonLinkIdentifier', c_uint32),
        ('m_weekendLinkIdentifier', c_uint32),
        ('m_sessionLinkIdentifier', c_uint32),
        ('m_pitStopWindowIdealLap', c_uint8),
        ('m_pitStopWindowLatestLap', c_uint8),
        ('m_pitStopRejoinPosition', c_uint8),
        ('m_steeringAssist', c_uint8),
        ('m_brakingAssist', c_uint8),
        ('m_gearboxAssist', c_uint8),
        ('m_pitAssist', c_uint8),
        ('m_pitReleaseAssist', c_uint8),
        ('m_ERSAssist', c_uint8),
        ('m_DRSAssist', c_uint8),
        ('m_dynamicRacingLine', c_uint8),
        ('m_dynamicRacingLineType', c_uint8),
        ('m_gameMode', c_uint8),
        ('m_ruleSet', c_uint8),
        ('m_timeOfDay', c_uint32),
        ('m_sessionLength', c_uint8),
        ('m_speedUnitsLeadPlayer', c_uint8),
        ('m_temperatureUnitsLeadPlayer', c_uint8),
        ('m_speedUnitsSecondaryPlayer', c_uint8),
        ('m_temperatureUnitsSecondaryPlayer', c_uint8),
        ('m_numSafetyCarPeriods', c_uint8),
        ('m_numVirtualSafetyCarPeriods', c_uint8),
        ('m_numRedFlagPeriods', c_uint8),
        ('m_equalCarPerformance', c_uint8),
        ('m_recoveryMode', c_uint8),
        ('m_flashbackLimit', c_uint8),
        ('m_surfaceType', c_uint8),
        ('m_lowFuelMode', c_uint8),
        ('m_raceStarts', c_uint8),
        ('m_tyreTemperature', c_uint8),
        ('m_pitLaneTyreSim', c_uint8),
        ('m_carDamage', c_uint8),
        ('m_carDamageRate', c_uint8),
        ('m_collisions', c_uint8),
        ('m_collisionsOffForFirstLapOnly', c_uint8),
        ('m_mpUnsafePitRelease', c_uint8),
        ('m_mpOffForGriefing', c_uint8),
        ('m_cornerCuttingStringency', c_uint8),
        ('m_parcFermeRules', c_uint8),
        ('m_pitStopExperience', c_uint8),
        ('m_safetyCar', c_uint8),
        ('m_safetyCarExperience', c_uint8),
        ('m_formationLap', c_uint8),
        ('m_formationLapExperience', c_uint8),
        ('m_redFlags', c_uint8),
        ('m_affectsLicenceLevelSolo', c_uint8),
        ('m_affectsLicenceLevelMP', c_uint8),
        ('m_numSessionsInWeekend', c_uint8),
        ('m_weekendStructure', c_uint8 * 12),
        ('m_sector2LapDistanceStart', c_float),
        ('m_sector3LapDistanceStart', c_float),
    ]


# -------------------- Packet 2: Lap Data --------------------
class LapData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_lastLapTimeInMS', c_uint32),
        ('m_currentLapTimeInMS', c_uint32),
        ('m_sector1TimeMSPart', c_uint16),
        ('m_sector1TimeMinutesPart', c_uint8),
        ('m_sector2TimeMSPart', c_uint16),
        ('m_sector2TimeMinutesPart', c_uint8),
        ('m_deltaToCarInFrontMSPart', c_uint16),
        ('m_deltaToCarInFrontMinutesPart', c_uint8),
        ('m_deltaToRaceLeaderMSPart', c_uint16),
        ('m_deltaToRaceLeaderMinutesPart', c_uint8),
        ('m_lapDistance', c_float),
        ('m_totalDistance', c_float),
        ('m_safetyCarDelta', c_float),
        ('m_carPosition', c_uint8),
        ('m_currentLapNum', c_uint8),
        ('m_pitStatus', c_uint8),
        ('m_numPitStops', c_uint8),
        ('m_sector', c_uint8),
        ('m_currentLapInvalid', c_uint8),
        ('m_penalties', c_uint8),
        ('m_totalWarnings', c_uint8),
        ('m_cornerCuttingWarnings', c_uint8),
        ('m_numUnservedDriveThroughPens', c_uint8),
        ('m_numUnservedStopGoPens', c_uint8),
        ('m_gridPosition', c_uint8),
        ('m_driverStatus', c_uint8),
        ('m_resultStatus', c_uint8),
        ('m_pitLaneTimerActive', c_uint8),
        ('m_pitLaneTimeInLaneInMS', c_uint16),
        ('m_pitStopTimerInMS', c_uint16),
        ('m_pitStopShouldServePen', c_uint8),
        ('m_speedTrapFastestSpeed', c_float),
        ('m_speedTrapFastestLap', c_uint8),
    ]

class PacketLapData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_lapData', LapData * 22),
        ('m_timeTrialPBCarIdx', c_uint8),
        ('m_timeTrialRivalCarIdx', c_uint8),
    ]

# -------------------- Packet 3: Event Data --------------------
class FastestLap(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [('vehicleIdx', c_uint8), ('lapTime', c_float)]

class Retirement(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [('vehicleIdx', c_uint8)]

class TeamMateInPits(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [('vehicleIdx', c_uint8)]

class RaceWinner(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [('vehicleIdx', c_uint8)]

class Penalty(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('penaltyType', c_uint8),
        ('infringementType', c_uint8),
        ('vehicleIdx', c_uint8),
        ('otherVehicleIdx', c_uint8),
        ('time', c_uint8),
        ('lapNum', c_uint8),
        ('placesGained', c_uint8),
    ]

class SpeedTrap(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('vehicleIdx', c_uint8),
        ('speed', c_float),
        ('isOverallFastestInSession', c_uint8),
        ('isDriverFastestInSession', c_uint8),
        ('fastestVehicleIdxInSession', c_uint8),
        ('fastestSpeedInSession', c_float),
    ]

class StartLights(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [('numLights', c_uint8)]

class DriveThroughPenaltyServed(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [('vehicleIdx', c_uint8)]

class StopGoPenaltyServed(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [('vehicleIdx', c_uint8)]

class Flashback(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [('flashbackFrameIdentifier', c_uint32), ('flashbackSessionTime', c_float)]

class Buttons(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [('buttonStatus', c_uint32)]

class Overtake(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [('overtakingVehicleIdx', c_uint8), ('beingOvertakenVehicleIdx', c_uint8)]

class SafetyCar(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [('safetyCarType', c_uint8), ('eventType', c_uint8)]

class Collision(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [('vehicle1Idx', c_uint8), ('vehicle2Idx', c_uint8)]

class EventDataDetails(Union):
    _pack_ = 1
    _fields_ = [
        ('FastestLap', FastestLap),
        ('Retirement', Retirement),
        ('TeamMateInPits', TeamMateInPits),
        ('RaceWinner', RaceWinner),
        ('Penalty', Penalty),
        ('SpeedTrap', SpeedTrap),
        ('StartLights', StartLights),
        ('DriveThroughPenaltyServed', DriveThroughPenaltyServed),
        ('StopGoPenaltyServed', StopGoPenaltyServed),
        ('Flashback', Flashback),
        ('Buttons', Buttons),
        ('Overtake', Overtake),
        ('SafetyCar', SafetyCar),
        ('Collision', Collision),
    ]

class PacketEventData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_eventStringCode', c_uint8 * 4),
        ('m_eventDetails', EventDataDetails),
    ]

# -------------------- Packet 4: Participants --------------------
class ParticipantData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_aiControlled', c_uint8),
        ('m_driverId', c_uint8),
        ('m_networkId', c_uint8),
        ('m_teamId', c_uint8),
        ('m_myTeam', c_uint8),
        ('m_raceNumber', c_uint8),
        ('m_nationality', c_uint8),
        ('m_name', c_char * 48),
        ('m_yourTelemetry', c_uint8),
        ('m_showOnlineNames', c_uint8),
        ('m_techLevel', c_uint16),
        ('m_platform', c_uint8),
    ]

class PacketParticipantsData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_numActiveCars', c_uint8),
        ('m_participants', ParticipantData * 22),
    ]

# -------------------- Packet 5: Car Setup --------------------
class CarSetupData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_frontWing', c_uint8),
        ('m_rearWing', c_uint8),
        ('m_onThrottle', c_uint8),
        ('m_offThrottle', c_uint8),
        ('m_frontCamber', c_float),
        ('m_rearCamber', c_float),
        ('m_frontToe', c_float),
        ('m_rearToe', c_float),
        ('m_frontSuspension', c_uint8),
        ('m_rearSuspension', c_uint8),
        ('m_frontAntiRollBar', c_uint8),
        ('m_rearAntiRollBar', c_uint8),
        ('m_frontSuspensionHeight', c_uint8),
        ('m_rearSuspensionHeight', c_uint8),
        ('m_brakePressure', c_uint8),
        ('m_brakeBias', c_uint8),
        ('m_engineBraking', c_uint8),
        ('m_rearLeftTyrePressure', c_float),
        ('m_rearRightTyrePressure', c_float),
        ('m_frontLeftTyrePressure', c_float),
        ('m_frontRightTyrePressure', c_float),
        ('m_ballast', c_uint8),
        ('m_fuelLoad', c_float),
    ]

class PacketCarSetupData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_carSetups', CarSetupData * 22),
        ('m_nextFrontWingValue', c_float),
    ]

# -------------------- Packet 6: Car Telemetry --------------------
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

# -------------------- Packet 7: Car Status --------------------
class CarStatusData(LittleEndianStructure):
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
        ('m_enginePowerICE', c_float),
        ('m_enginePowerMGUK', c_float),
        ('m_ersStoreEnergy', c_float),
        ('m_ersDeployMode', c_uint8),
        ('m_ersHarvestedThisLapMGUK', c_float),
        ('m_ersHarvestedThisLapMGUH', c_float),
        ('m_ersDeployedThisLap', c_float),
        ('m_networkPaused', c_uint8),
    ]

class PacketCarStatusData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_carStatusData', CarStatusData * 22),
    ]

# -------------------- Packet 8: Final Classification --------------------
class FinalClassificationData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_position', c_uint8),
        ('m_numLaps', c_uint8),
        ('m_gridPosition', c_uint8),
        ('m_points', c_uint8),
        ('m_numPitStops', c_uint8),
        ('m_resultStatus', c_uint8),
        ('m_bestLapTimeInMS', c_uint32),
        ('m_totalRaceTime', c_double),
        ('m_penaltiesTime', c_uint8),
        ('m_numPenalties', c_uint8),
        ('m_numTyreStints', c_uint8),
        ('m_tyreStintsActual', c_uint8 * 8),
        ('m_tyreStintsVisual', c_uint8 * 8),
        ('m_tyreStintsEndLaps', c_uint8 * 8),
    ]

class PacketFinalClassificationData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_numCars', c_uint8),
        ('m_classificationData', FinalClassificationData * 22),
    ]

# -------------------- Packet 9: Lobby Info --------------------
class LobbyInfoData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_aiControlled', c_uint8),
        ('m_teamId', c_uint8),
        ('m_nationality', c_uint8),
        ('m_platform', c_uint8),
        ('m_name', c_char * 48),
        ('m_carNumber', c_uint8),
        ('m_yourTelemetry', c_uint8),
        ('m_showOnlineNames', c_uint8),
        ('m_techLevel', c_uint16),
        ('m_readyStatus', c_uint8),
    ]

class PacketLobbyInfoData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_numPlayers', c_uint8),
        ('m_lobbyPlayers', LobbyInfoData * 22),
    ]

# -------------------- Packet 10: Car Damage --------------------

class CarDamageData(LittleEndianStructure):
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

class PacketCarDamageData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_carDamageData', CarDamageData * 22),
    ]


# -------------------- Packet 11:  Session History --------------------
class LapHistoryData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_lapTimeInMS', c_uint32),
        ('m_sector1TimeInMS', c_uint16),
        ('m_sector2TimeInMS', c_uint16),
        ('m_sector3TimeInMS', c_uint16),
        ('m_lapValidBitFlags', c_uint8),
    ]

class TyreStintHistoryData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_endLap', c_uint8),
        ('m_tyreActualCompound', c_uint8),
        ('m_tyreVisualCompound', c_uint8),
    ]

class PacketSessionHistoryData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_carIdx', c_uint8),
        ('m_numLaps', c_uint8),
        ('m_numTyreStints', c_uint8),
        ('m_bestLapTimeLapNum', c_uint8),
        ('m_bestSector1LapNum', c_uint8),
        ('m_bestSector2LapNum', c_uint8),
        ('m_bestSector3LapNum', c_uint8),
        ('m_lapHistoryData', LapHistoryData * 100),
        ('m_tyreStintsHistoryData', TyreStintHistoryData * 8),
    ]


# -------------------- Packet 12: Tyre Sets--------------------


class TyreSetData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_actualTyreCompound', c_uint8),   # 1
        ('m_visualTyreCompound', c_uint8),   # 1
        ('m_wear', c_uint8),                 # 1
        ('m_available', c_uint8),            # 1
        ('m_recommendedSession', c_uint8),   # 1
        ('m_lifeSpan', c_uint8),             # 1
        ('m_usableLife', c_uint8),           # 1
        ('m_lapDeltaTime', c_int16),         # 2 (signed 16-bit)
        ('m_fitted', c_uint8),               # 1
    ]
    # total = 10 bytes per TyreSetData

class PacketTyreSetsData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),          # 29 bytes
        ('m_carIdx', c_uint8),               # 1
        ('m_tyreSetData', TyreSetData * 20), # 20 * 10 = 200
        ('m_fittedIdx', c_uint8),            # 1
    ]

# -------------------- Packet 13: Motion Ex --------------------

class PacketMotionExData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_localVelocityX', c_float),
        ('m_localVelocityY', c_float),
        ('m_localVelocityZ', c_float),
        ('m_angularVelocityX', c_float),
        ('m_angularVelocityY', c_float),
        ('m_angularVelocityZ', c_float),
        ('m_angularAccelerationX', c_float),
        ('m_angularAccelerationY', c_float),
        ('m_angularAccelerationZ', c_float),
        ('m_frontWheelsAngle', c_float),
        ('m_wheelSpeed', c_float * 4),
        ('m_wheelSlipRatio', c_float * 4),
        ('m_wheelSlipAngle', c_float * 4)
    ]


# -------------------- Packet 14:  Time Trial --------------------

class TimeTrialDataSet(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_carIdx', c_uint8),
        ('m_bestLapTime', c_float),
        ('m_sector1Time', c_float),
        ('m_sector2Time', c_float),
        ('m_sector3Time', c_float),
    ]

class PacketTimeTrialData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_pb', TimeTrialDataSet),
        ('m_rival', TimeTrialDataSet),
    ]



# -------------------- Packet Registry --------------------


from ctypes import sizeof

PACKET_REGISTRY = {
    0: ("Motion", PacketMotionData),
    1: ("Session", PacketSessionData),
    2: ("Lap", PacketLapData),
    3: ("Event", PacketEventData),
    4: ("Participants", PacketParticipantsData),
    5: ("Car Setups", PacketCarSetupData),
    6: ("Telemetry", PacketCarTelemetryData),
    7: ("Car Status", PacketCarStatusData),
    8: ("Final Classification", PacketFinalClassificationData),
    9: ("Lobby Info", PacketLobbyInfoData),
    10: ("Damage", PacketCarDamageData),
    11: ("Session History", PacketSessionHistoryData),
    12: ("Tyres", PacketTyreSetsData),
    13: ("MotionEx", PacketMotionExData),
    14: ("TimeTrial", PacketTimeTrialData),
}


PACKET_PARSERS = {  0:  PacketMotionData,
    1: PacketSessionData,
    2: PacketLapData,
    3: PacketEventData,
    4: PacketParticipantsData,
    5: PacketCarSetupData,
    6: PacketCarTelemetryData,
    7: PacketCarStatusData,
    8: PacketFinalClassificationData,
    9: PacketLobbyInfoData,
    10: PacketCarDamageData,
    11: PacketSessionHistoryData,
    12: PacketTyreSetsData,
    13: PacketMotionExData,
    14: PacketTimeTrialData}


import socket, threading, queue
from router import PacketRouter
from packet_definitions import PacketHeader

UDP_IP = "0.0.0.0"
UDP_PORT = 20777
STOP_EVENT = threading.Event()

# One queue per packet type
PACKET_QUEUES = {i: queue.Queue(maxsize=100) for i in range(14)}

def udp_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print(f"Listening on {UDP_IP}:{UDP_PORT}")
    while not STOP_EVENT.is_set():
        try:
            data, _ = sock.recvfrom(2048)
            header = PacketHeader.from_buffer_copy(data)
            packet_id = header.m_packetId
            if packet_id in PACKET_QUEUES:
                try:
                    PACKET_QUEUES[packet_id].put_nowait(data)
                except queue.Full:
                    PACKET_QUEUES[packet_id].get_nowait()
                    PACKET_QUEUES[packet_id].put_nowait(data)
        except Exception as e:
            print(f"UDP error: {e}")

# Start router and threads
router = PacketRouter(PACKET_QUEUES, STOP_EVENT)
threads = [threading.Thread(target=udp_listener, daemon=True)] + router.get_processor_threads()

for t in threads:
    t.start()

try:
    STOP_EVENT.wait()
except KeyboardInterrupt:
    STOP_EVENT.set()
