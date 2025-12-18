import asyncio

UDP_IP = "0.0.0.0"
UDP_PORT = 20777
from ctypes import LittleEndianStructure, Union, c_uint8, c_int8
from ctypes import c_uint16, c_int16, c_uint32, c_uint64, c_float, c_double, c_char

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




EventCodes = {'SSTA': 'Session Started',
                'SEND': 'Session Ended',
                'FTLP': 'Fastest Lap',
                'RTMT': 'Retirement',
                'DRSE': 'DRS enabled',
                'DRSD': 'DRS disabled',
                'TMPT': 'Team mate in pits',
                'CHQF': 'Chequered flag',
                'RCWN': 'Race Winner',
                'PENA': 'Penalty Issued',
                'SPTP': 'Speed Trap Triggered',
                'STLG': 'Start lights',
                'LGOT': 'Lights out',
                'DTSV': 'Drive through served',
                'SGSV': 'Stop go served',
                'FLBK': 'Flashback',
                'BUTN': 'Button status',
                'RDFL': 'Red Flag',
                'OVTK': 'Overtake',
                'SCAR': 'Safety Car',
                'COLL': 'Collision'}



import asyncio
import threading
from ctypes import Structure, c_uint8  # example import; your F1 packet parser uses similar
# from your_f1_parser import PacketHeader, PACKET_PARSERS

UDP_IP = "0.0.0.0"
UDP_PORT = 20777
data_queue = asyncio.Queue(maxsize=100)
latest_data = {}



PACKET_HANDLERS = {
        0: lambda pkt, hdr: {
        # Motion
        
    },
    
    
    1: lambda pkt, hdr: {  #Session Data
        'm_weather': pkt.m_weather,
        'm_trackTemperature': pkt.m_trackTemperature,
        'm_airTemperature': pkt.m_airTemperature,
        "m_sessionTimeLeft" : pkt.m_sessionTimeLeft,
        "m_sessionDuration" : pkt.m_sessionDuration,
        "m_pitStopRejoinPosition" : pkt.m_pitStopRejoinPosition,
        
    },

    2: lambda pkt, hdr: { #Lap Data
        'm_currentLapTime': pkt.m_lapData[hdr.m_playerCarIndex].m_currentLapTimeInMS,
        'm_carPosition': pkt.m_lapData[hdr.m_playerCarIndex].m_carPosition,
        'm_lastLapTimeInMS' : pkt.m_lapData[hdr.m_playerCarIndex].m_lastLapTimeInMS,
        "m_lapDistance" : pkt.m_lapData[hdr.m_playerCarIndex].m_lapDistance,
        "m_totalDistance" : pkt.m_lapData[hdr.m_playerCarIndex].m_totalDistance,
        "m_pitStatus" : pkt.m_lapData[hdr.m_playerCarIndex].m_pitStatus,
        "m_driverStatus" : pkt.m_lapData[hdr.m_playerCarIndex].m_driverStatus,
        "m_currentLapNum" : pkt.m_lapData[hdr.m_playerCarIndex].m_currentLapNum,
        
        
    },

    3: lambda pkt, hdr: {
        # Event packet — often needs decoding from event string
        'm_eventStringCode': bytes(pkt.m_eventStringCode).decode('utf-8').strip('\x00'), 
        'm_eventDetails' : pkt.m_eventDetails
        
        
    },

    4: lambda pkt, hdr: {
        # Participants
        
    },

    5: lambda pkt, hdr: {
        # Setup data
        'm_brakeBias' : pkt.m_carSetups[hdr.m_playerCarIndex].m_brakeBias,
    },

    6: lambda pkt, hdr: (
        lambda car: {
            'm_speed': car.m_speed,
            'm_throttle': car.m_throttle,
            'm_brake': car.m_brake,
            'm_gear': car.m_gear,
            'm_drs': car.m_drs,
            'm_revLightsPercent': car.m_revLightsPercent,
            'm_revLightsBitValue' : car.m_revLightsBitValue,
            'm_brakesTemperature': list(car.m_brakesTemperature),
            'm_tyresSurfaceTemperature': list(car.m_tyresSurfaceTemperature),
            'm_tyresInnerTemperature': list(car.m_tyresInnerTemperature),
            # 'm_surfaceType': list(car.m_surfaceType),
        }
    )(pkt.m_carTelemetryData[hdr.m_playerCarIndex]),

    7: lambda pkt, hdr: {
        # Car status data
    },

    8: lambda pkt, hdr: {
        # Final classification
    },

    9: lambda pkt, hdr: {
        # Lobby info
    },

    10: lambda pkt, hdr: (
        # Damage data
        lambda car_damage : {'m_tyresWear' : list(car_damage.m_tyresWear)}
        )(pkt.m_carDamageData[hdr.m_playerCarIndex]),
        


    11: lambda pkt, hdr: {
        # Session history
    },

    12: lambda pkt, hdr: {
        # Tyre sets
    },

    13: lambda pkt, hdr: {
        # Extended motion
    },

    14: lambda pkt, hdr: {
        # Time trial
    },
}

# PACKET_HANDLERS = {
#         0: lambda pkt, hdr: {
#         # Motion

#     },
        
#     1: lambda pkt, hdr: {  #Session Data
#         'm_weather': pkt.m_weather,
#         'm_trackTemperature': pkt.m_trackTemperature,
#         'm_airTemperature': pkt.m_airTemperature,
#         "m_sessionTimeLeft" : pkt.m_sessionTimeLeft,
#         "m_sessionDuration" : pkt.m_sessionDuration,
#         "m_pitStopRejoinPosition" : pkt.m_pitStopRejoinPosition,
      
#     },

#     2: lambda pkt, hdr: { #Lap Data
#         'm_currentLapTime': pkt.m_lapData[hdr.m_playerCarIndex].m_currentLapTimeInMS,
#         'm_carPosition': pkt.m_lapData[hdr.m_playerCarIndex].m_carPosition,
#         'm_lastLapTimeInMS' : pkt.m_lapData[hdr.m_playerCarIndex].m_lastLapTimeInMS,
#         "m_lapDistance" : pkt.m_lapData[hdr.m_playerCarIndex].m_lapDistance,
#         "m_totalDistance" : pkt.m_lapData[hdr.m_playerCarIndex].m_totalDistance,
#         "m_pitStatus" : pkt.m_lapData[hdr.m_playerCarIndex].m_pitStatus,
#         "m_driverStatus" : pkt.m_lapData[hdr.m_playerCarIndex].m_driverStatus,
#         "m_currentLapNum" : pkt.m_lapData[hdr.m_playerCarIndex].m_currentLapNum,
#     },

#     3: lambda pkt, hdr: {
#         # Event packet — often needs decoding from event string
#         # 'eventStringCode': pkt.m_eventStringCode.decode('utf-8'),
#         'm_eventStringCode': bytes(pkt.m_eventStringCode).decode('utf-8').strip('\x00'), 
#         'm_eventDetails' : pkt.m_eventDetails


#     },

#     4: lambda pkt, hdr: {
#         # Participants

#     },

#     5: lambda pkt, hdr: {
#         # Setup data
        
#         'm_brakeBias' : pkt.m_carSetups[hdr.m_playerCarIndex].m_brakeBias,
#     },

#     6: lambda pkt, hdr: (
#         lambda car: {
#             'm_speed': car.m_speed,
#             'm_throttle': car.m_throttle,
#             'm_brake': car.m_brake,
#             'm_gear': car.m_gear,
#             'm_drs': car.m_drs,
#             'm_revLightsPercent': car.m_revLightsPercent,
#             'm_revLightsBitValue' : car.m_revLightsBitValue,
#             'm_brakesTemperature': list(car.m_brakesTemperature),
#             'm_tyresSurfaceTemperature': list(car.m_tyresSurfaceTemperature),
#             'm_tyresInnerTemperature': list(car.m_tyresInnerTemperature),
#             'm_surfaceType': list(car.m_surfaceType),
#             # 'm_surfaceType': list(car.m_surfaceType),
#         }
#     )(pkt.m_carTelemetryData[hdr.m_playerCarIndex]),

#     7: lambda pkt, hdr: {
    
#             "m_carStatusData": [
#             {
#             "m_tractionControl": cs.m_tractionControl,
#             "m_antiLockBrakes": cs.m_antiLockBrakes,
#             "m_fuelMix": cs.m_fuelMix,
#             "m_frontBrakeBias": cs.m_frontBrakeBias,
#             "m_pitLimiterStatus": cs.m_pitLimiterStatus,
#             "m_fuelInTank": cs.m_fuelInTank,
#             "m_fuelCapacity": cs.m_fuelCapacity,
#             "m_fuelRemainingLaps": cs.m_fuelRemainingLaps,
#             "m_maxRPM": cs.m_maxRPM,
#             "m_idleRPM": cs.m_idleRPM,
#             "m_maxGears": cs.m_maxGears,
#             "m_drsAllowed": cs.m_drsAllowed,
#             "m_drsActivationDistance": cs.m_drsActivationDistance,
#             "m_actualTyreCompound": cs.m_actualTyreCompound,
#             "m_visualTyreCompound": cs.m_visualTyreCompound,
#             "m_tyresAgeLaps": cs.m_tyresAgeLaps,
#             "m_vehicleFiaFlags": cs.m_vehicleFiaFlags,
#             "m_ersStoreEnergy": cs.m_ersStoreEnergy,
#             "m_ersDeployMode": cs.m_ersDeployMode,
#             "m_ersHarvestedThisLapMGUK": cs.m_ersHarvestedThisLapMGUK,
#             "m_ersHarvestedThisLapMGUH": cs.m_ersHarvestedThisLapMGUH,
#             "m_ersDeployedThisLap": cs.m_ersDeployedThisLap,
#             "m_networkPaused": cs.m_networkPaused,
#         }
#         for cs in pkt.m_carStatusData
#     ]
#     },





#     8: lambda pkt, hdr: {
#         # Final classification
#     },

#     9: lambda pkt, hdr: {
#         # Lobby info
#     },

#     10: lambda pkt, hdr: (
#         # Damage data
#         lambda car_damage : {'m_tyresWear' : list(car_damage.m_tyresWear)}
#         )(pkt.m_carDamageData[hdr.m_playerCarIndex]),



#     11: lambda pkt, hdr: {
#         # Session history
#     },

#     12: lambda pkt, hdr: {
#         # Tyre sets
#     },

#     13: lambda pkt, hdr: {# Extended motion
#     "m_wheelSlipAngle": list(pkt.m_wheelSlipAngle),
#     "m_wheelSlipRatio": list(pkt.m_wheelSlipRatio),
#     "m_wheelSpeed": list(pkt.m_wheelSpeed),
# },




#     14: lambda packet, hdr: {
#         # Time trial
    
#     # "m_playerSessionBestLapTime": packet.m_playerSessionBestLapTime,
#     # "m_playerSessionBestLapTimeLapNum": packet.m_playerSessionBestLapTimeLapNum,
#     # "m_playerSessionBestSector1Time": packet.m_playerSessionBestSector1Time,
#     # "m_playerSessionBestSector1TimeLapNum": packet.m_playerSessionBestSector1TimeLapNum,
#     # "m_playerSessionBestSector2Time": packet.m_playerSessionBestSector2Time,
#     # "m_playerSessionBestSector2TimeLapNum": packet.m_playerSessionBestSector2TimeLapNum,
#     # "m_playerSessionBestSector3Time": packet.m_playerSessionBestSector3Time,
#     # "m_playerSessionBestSector3TimeLapNum": packet.m_playerSessionBestSector3TimeLapNum,
# }

# }
    




def get_latest_data():
    """Return a copy of the most recent telemetry dictionary."""
    return dict(latest_data)


def handle_packet(packet_id, packet, header):
    handler = PACKET_HANDLERS.get(packet_id)
    return handler(packet, header) if handler else None


def unpack_packet(data: bytes):
    try:
        header = PacketHeader.from_buffer_copy(data)
        packet_id = header.m_packetId
        parser_cls = PACKET_PARSERS.get(packet_id)
        if not parser_cls:
            return None
        packet = parser_cls.from_buffer_copy(data)
        return handle_packet(packet_id, packet, header)
    except Exception as e:
        print(f"Error unpacking packet: {e}")
        return None


class F1TelemetryProtocol(asyncio.DatagramProtocol):
    def datagram_received(self, data, addr):
        asyncio.create_task(self.handle_packet(data))

    async def handle_packet(self, data):
        parsed = unpack_packet(data)
        if parsed:
            if data_queue.full():
                await data_queue.get()
            await data_queue.put(parsed)


async def udp_listener():
    """Asynchronous UDP listener."""
    loop = asyncio.get_running_loop()
    transport, _ = await loop.create_datagram_endpoint(
        lambda: F1TelemetryProtocol(),
        local_addr=(UDP_IP, UDP_PORT)
    )

    print(f"Listening asynchronously for UDP telemetry on {UDP_IP}:{UDP_PORT}")
    try:
        while True:
            await asyncio.sleep(3600)
    finally:
        transport.close()


async def dashboard_update_loop():
    """Continuously pull from queue and update latest_data."""
    global latest_data
    while True:
        try:
            new_data = await asyncio.wait_for(data_queue.get(), timeout=0.05)
            latest_data = new_data
        except asyncio.TimeoutError:
            await asyncio.sleep(0.01)


def start_udp_background():
    """Launch asyncio loop in a background thread."""
    async def main():
        await asyncio.gather(udp_listener(), dashboard_update_loop())

    def runner():
        asyncio.run(main())

    thread = threading.Thread(target=runner, daemon=True)
    thread.start()
    print("UDP telemetry listener started in background.")



# Print Testing
if __name__ == "__main__":
    start_udp_background()

    while True:
        data = get_latest_data()
        
        
        # if data is not None skip
        try:
            print(f'm_wheelSlipAngle : {data['m_wheelSlipAngle']}')
            # print(data)
        except:
            pass
        




# | ID | Packet Name          |
# | -- | -------------------- |
# | 0  | Motion               |
# | 1  | Session              |
# | 2  | Lap Data             |
# | 3  | Event                |
# | 4  | Participants         |
# | 5  | Car Setups           |
# | 6  | Car Telemetry        |
# | 7  | Car Status           |
# | 8  | Final Classification |
# | 9  | Lobby Info           |
# | 10 | Car Damage           |
# | 11 | Session History      |
# | 12 | Tyre Sets            |
# | 13 | Motion Ex            |
# | 14 | Time Trial           |
