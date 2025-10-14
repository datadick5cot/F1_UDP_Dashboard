import socket
from ctypes import sizeof, LittleEndianStructure
from ctypes import c_uint8, c_uint16, c_uint32, c_uint64, c_float, c_int16, c_int8, Union, c_char, c_double

# Globals to store latest lap info
from collections import deque
import threading

current_lap_number = None
latest_player_lap = None
latest_rival_lap = None



class PacketHeader(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_packetFormat', c_uint16), # 2024
        ('m_gameYear', c_uint8), # Game year - last two digits e.g. 24
        ('m_gameMajorVersion', c_uint8), # Game major version - "X.00"
        ('m_gameMinorVersion', c_uint8), # Game minor version - "1.XX"
        ('m_packetVersion', c_uint8), # Version of this packet type, all start from 1
        ('m_packetId', c_uint8), # Identifier for the packet type, see below
        ('m_sessionUID', c_uint64), # Unique identifier for the session
        ('m_sessionTime', c_float), # Session timestamp
        ('m_frameIdentifier', c_uint32), # Identifier for the frame the data was retrieved on
        ('m_overallFrameIdentifier', c_uint32), # Overall identifier for the frame the data was retrieved
        ('m_playerCarIndex', c_uint8), # Index of player's car in the array
        ('m_secondaryPlayerCarIndex', c_uint8), # Index of secondary player's car in the array (splitscreen)
    ]



class CarMotionData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_worldPositionX', c_float), # World space X position - metres
        ('m_worldPositionY', c_float), # World space Y position
        ('m_worldPositionZ', c_float), # World space Z position
        ('m_worldVelocityX', c_float), # Velocity in world space X – metres/s
        ('m_worldVelocityY', c_float), # Velocity in world space Y
        ('m_worldVelocityZ', c_float), # Velocity in world space Z
        ('m_worldForwardDirX', c_int16), # World space forward X direction (normalised)
        ('m_worldForwardDirY', c_int16), # World space forward Y direction (normalised)
        ('m_worldForwardDirZ', c_int16), # World space forward Z direction (normalised)
        ('m_worldRightDirX', c_int16), # World space right X direction (normalised)
        ('m_worldRightDirY', c_int16), # World space right Y direction (normalised)
        ('m_worldRightDirZ', c_int16), # World space right Z direction (normalised)
        ('m_gForceLateral', c_float), # Lateral G-Force component
        ('m_gForceLongitudinal', c_float),   # Longitudinal G-Force component
        ('m_gForceVertical', c_float), # Vertical G-Force component
        ('m_yaw', c_float), # Yaw angle in radians
        ('m_pitch', c_float),# Pitch angle in radians
        ('m_roll', c_float), # Roll angle in radians
        ('m_wheelSpeed', c_float * 4),       # [RL, RR, FL, FR]
        ('m_wheelSlip', c_float * 4),
        ('m_localVelocityX', c_float),
        ('m_localVelocityY', c_float),
        ('m_localVelocityZ', c_float),
        ('m_angularVelocityX', c_float),
        ('m_angularVelocityY', c_float),
        ('m_angularVelocityZ', c_float),
        ('m_angularAccelerationX', c_float),
        ('m_angularAccelerationY', c_float),
        ('m_angularAccelerationZ', c_float),
        ('m_frontWheelsAngle', c_float)
    ]
        
        

        
class PacketMotionData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader), # Header
        ('m_carMotionData', CarMotionData * 22), # Data for all cars on track
    ]
        

class MarshalZone(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_zoneStart', c_float), # Fraction (0..1) of way through the lap the marshal zone starts
        ('m_zoneFlag', c_int8), # -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow
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
        # 0 = unknown, see appendix
        # Time in minutes the forecast is for
        # Weather - 0 = clear, 1 = light cloud, 2 = overcast
        # Track temp. in degrees Celsius
        # Track temp. change – 0 = up, 1 = down, 2 = no change
        # Air temp. in degrees celsius
        # Air temp. change – 0 = up, 1 = down, 2 = no change
        # Rain percentage (0-100)

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
        # Header
        # Weather - 0 = clear, 1 = light cloud, 2 = overcast
        # Track temp. in degrees celsius
        # Air temp. in degrees celsius
        # Total number of laps in this race
        # Track length in metres
        # 0 = unknown, see appendix
        # -1 for unknown, see appendix
        # Formula, 0 = F1 Modern, 1 = F1 Classic, 2 = F2,
        # Time left in session in seconds
        # Session duration in seconds
        # Pit speed limit in kilometres per hour
        # Whether the game is paused – network game only
        # Whether the player is spectating
        # Index of the car being spectated
        # SLI Pro support, 0 = inactive, 1 = active
        # Number of marshal zones to follow
        # List of marshal zones – max 21
        # 0 = no safety car, 1 = full
        # 0 = offline, 1 = online
        # Number of weather samples to follow
        # Array of weather forecast samples
        # 0 = Perfect, 1 = Approximate
        # AI Difficulty rating – 0-110
        # Identifier for season - persists across saves
        # Identifier for weekend - persists across saves
        # Identifier for session - persists across saves
        # Ideal lap to pit on for current strategy (player)
        # Latest lap to pit on for current strategy (player)
        # Predicted position to rejoin at (player)
        # 0 = off, 1 = on
        # 0 = off, 1 = low, 2 = medium, 3 = high
        # 1 = manual, 2 = manual & suggested gear, 3 = auto
        # 0 = off, 1 = on
        # 0 = off, 1 = on
        # 0 = off, 1 = on
        # 0 = off, 1 = on
        # 0 = off, 1 = corners only, 2 = full
        # 0 = 2D, 1 = 3D
        # Game mode id - see appendix
        # Ruleset - see appendix
        # Local time of day - minutes since midnight
        # 0 = None, 2 = Very Short, 3 = Short, 4 = Medium
        # 0 = MPH, 1 = KPH
        # 0 = Celsius, 1 = Fahrenheit
        # 0 = MPH, 1 = KPH
        # 0 = Celsius, 1 = Fahrenheit
        # Number of safety cars called during session
        # Number of virtual safety cars called
        # Number of red flags called during session
        # 0 = Off, 1 = On
        # 0 = None, 1 = Flashbacks, 2 = Auto-recovery
        # 0 = Low, 1 = Medium, 2 = High, 3 = Unlimited
        # 0 = Simplified, 1 = Realistic
        # 0 = Easy, 1 = Hard
        # 0 = Manual, 1 = Assisted
        # 0 = Surface only, 1 = Surface & Carcass
        # 0 = On, 1 = Off
        # 0 = Off, 1 = Reduced, 2 = Standard, 3 = Simulation
        # 0 = Reduced, 1 = Standard, 2 = Simulation
        # 0 = Off, 1 = Player-to-Player Off, 2 = On
        # 0 = Disabled, 1 = Enabled
        # 0 = On, 1 = Off (Multiplayer)
        # 0 = Disabled, 1 = Enabled (Multiplayer)
        # 0 = Regular, 1 = Strict
        # 0 = Off, 1 = On
        # 0 = Automatic, 1 = Broadcast, 2 = Immersive
        # 0 = Off, 1 = Reduced, 2 = Standard, 3 = Increased
        # 0 = Broadcast, 1 = Immersive
        # 0 = Off, 1 = On
        # 0 = Broadcast, 1 = Immersive
        # 0 = Off, 1 = Reduced, 2 = Standard, 3 = Increased
        # 0 = Off, 1 = On
        # 0 = Off, 1 = On
        # Number of session in following array
        # List of session types to show weekend
        # Distance in m around track where sector 2 starts
        # Distance in m around track where sector 3 starts

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
        # Last lap time in milliseconds
        # Current time around the lap in milliseconds
        # Sector 1 time milliseconds part
        # Sector 1 whole minute part
        # Sector 2 time milliseconds part
        # Sector 2 whole minute part
        # Time delta to car in front milliseconds part
        # Time delta to car in front whole minute part
        # Time delta to race leader milliseconds part
        # Time delta to race leader whole minute part
        # Distance vehicle is around current lap in metres – could
        # Total distance travelled in session in metres – could
        # Delta in seconds for safety car
        # Car race position
        # Current lap number
        # 0 = none, 1 = pitting, 2 = in pit area
        # Number of pit stops taken in this race
        # 0 = sector1, 1 = sector2, 2 = sector3
        # Current lap invalid - 0 = valid, 1 = invalid
        # Accumulated time penalties in seconds to be added
        # Accumulated number of warnings issued
        # Accumulated number of corner cutting warnings issued
        # Num drive through pens left to serve
        # Num stop go pens left to serve
        # Grid position the vehicle started the race in
        # Status of driver - 0 = in garage, 1 = flying lap
        # Result status - 0 = invalid, 1 = inactive, 2 = active
        # Pit lane timing, 0 = inactive, 1 = active
        # If active, the current time spent in the pit lane in ms
        # Time of the actual pit stop in ms
        # Whether the car should serve a penalty at this stop
        # Fastest speed through speed trap for this car in kmph
        # Lap no the fastest speed was achieved, 255 = not set

class PacketLapData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_lapData', LapData * 22),
        ('m_timeTrialPBCarIdx', c_uint8),
        ('m_timeTrialRivalCarIdx', c_uint8),
    ]
        # Header
        # Lap data for all cars on track
        # Index of Personal Best car in time trial (255 if invalid)
        # Index of Rival car in time trial (255 if invalid)

class EventDataDetails(Union):
    _pack_ = 1
    _fields_ = [
    ]

class PacketEventData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_eventStringCode', c_uint8 * 4),
        ('m_eventDetails', EventDataDetails),
    ]
        # Header
        # Event string code, see below
        # Event details - should be interpreted differently

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
        # Whether the vehicle is AI (1) or Human (0) controlled
        # Driver id - see appendix, 255 if network human
        # Network id – unique identifier for network players
        # Team id - see appendix
        # My team flag – 1 = My Team, 0 = otherwise
        # Race number of the car
        # Nationality of the driver
        # Name of participant in UTF-8 format – null terminated
        # The player's UDP setting, 0 = restricted, 1 = public
        # The player's show online names setting, 0 = off, 1 = on
        # F1 World tech level
        # 1 = Steam, 3 = PlayStation, 4 = Xbox, 6 = Origin, 255 = unknown

class PacketParticipantsData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_numActiveCars', c_uint8),
        ('m_participants', ParticipantData * 22),
    ]
        # Header
        # Number of active cars in the data – should match number of

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
        # Front wing aero
        # Rear wing aero
        # Differential adjustment on throttle (percentage)
        # Differential adjustment off throttle (percentage)
        # Front camber angle (suspension geometry)
        # Rear camber angle (suspension geometry)
        # Front toe angle (suspension geometry)
        # Rear toe angle (suspension geometry)
        # Front suspension
        # Rear suspension
        # Front anti-roll bar
        # Front anti-roll bar
        # Front ride height
        # Rear ride height
        # Brake pressure (percentage)
        # Brake bias (percentage)
        # Engine braking (percentage)
        # Rear left tyre pressure (PSI)
        # Rear right tyre pressure (PSI)
        # Front left tyre pressure (PSI)
        # Front right tyre pressure (PSI)
        # Ballast
        # Fuel load

class PacketCarSetupData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_carSetups', CarSetupData * 22),
        ('m_nextFrontWingValue', c_float),
    ]
        # Header
        # Value of front wing after next pit stop - player only



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
        # Speed of car in kilometres per hour
        # Amount of throttle applied (0.0 to 1.0)
        # Steering (-1.0 (full lock left) to 1.0 (full lock right))
        # Amount of brake applied (0.0 to 1.0)
        # Amount of clutch applied (0 to 100)
        # Gear selected (1-8, N=0, R=-1)
        # Engine RPM
        # 0 = off, 1 = on
        # Rev lights indicator (percentage)
        # Rev lights (bit 0 = leftmost LED, bit 14 = rightmost LED)
        # Brakes temperature (celsius)
        # Tyres surface temperature (celsius)
        # Tyres inner temperature (celsius)
        # Engine temperature (celsius)
        # Tyres pressure (PSI)
        # Driving surface, see appendices

class PacketCarTelemetryData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_carTelemetryData', CarTelemetryData * 22),
        ('m_mfdPanelIndex', c_uint8),
        ('m_mfdPanelIndexSecondaryPlayer', c_uint8),
        ('m_suggestedGear', c_int8),
    ]
        # Header
        # Index of MFD panel open - 255 = MFD closed
        # See above
        # Suggested gear for the player (1-8)

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
        # Traction control - 0 = off, 1 = medium, 2 = full
        # 0 (off) - 1 (on)
        # Fuel mix - 0 = lean, 1 = standard, 2 = rich, 3 = max
        # Front brake bias (percentage)
        # Pit limiter status - 0 = off, 1 = on
        # Current fuel mass
        # Fuel capacity
        # Fuel remaining in terms of laps (value on MFD)
        # Cars max RPM, point of rev limiter
        # Cars idle RPM
        # Maximum number of gears
        # 0 = not allowed, 1 = allowed
        # 0 = DRS not available, non-zero - DRS will be available
        # F1 Modern - 16 = C5, 17 = C4, 18 = C3, 19 = C2, 20 = C1
        # F1 visual (can be different from actual compound)
        # Age in laps of the current set of tyres
        # -1 = invalid/unknown, 0 = none, 1 = green
        # Engine power output of ICE (W)
        # Engine power output of MGU-K (W)
        # ERS energy store in Joules
        # ERS deployment mode, 0 = none, 1 = medium
        # ERS energy harvested this lap by MGU-K
        # ERS energy harvested this lap by MGU-H
        # ERS energy deployed this lap
        # Whether the car is paused in a network game

class PacketCarStatusData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_carStatusData', CarStatusData * 22),
    ]
        # Header

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
        # Finishing position
        # Number of laps completed
        # Grid position of the car
        # Number of points scored
        # Number of pit stops made
        # Result status - 0 = invalid, 1 = inactive, 2 = active
        # Best lap time of the session in milliseconds
        # Total race time in seconds without penalties
        # Total penalties accumulated in seconds
        # Number of penalties applied to this driver
        # Number of tyres stints up to maximum
        # Actual tyres used by this driver
        # Visual tyres used by this driver
        # The lap number stints end on

class PacketFinalClassificationData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_numCars', c_uint8),
        ('m_classificationData', FinalClassificationData * 22),
    ]
        # Header
        # Number of cars in the final classification

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
        # Whether the vehicle is AI (1) or Human (0) controlled
        # Team id - see appendix (255 if no team currently selected)
        # Nationality of the driver
        # 1 = Steam, 3 = PlayStation, 4 = Xbox, 6 = Origin, 255 = unknown
        # Name of participant in UTF-8 format – null terminated
        # Car number of the player
        # The player's UDP setting, 0 = restricted, 1 = public
        # The player's show online names setting, 0 = off, 1 = on
        # F1 World tech level
        # 0 = not ready, 1 = ready, 2 = spectating

class PacketLobbyInfoData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_numPlayers', c_uint8),
        ('m_lobbyPlayers', LobbyInfoData * 22),
    ]
        # Header
        # Number of players in the lobby data

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
        ('m_engineMGUHWear', c_uint8),
        ('m_engineESWear', c_uint8),
        ('m_engineCEWear', c_uint8),
        ('m_engineICEWear', c_uint8),
        ('m_engineMGUKWear', c_uint8),
        ('m_engineTCWear', c_uint8),
        ('m_engineBlown', c_uint8),
        ('m_engineSeized', c_uint8),
    ]
        # Tyre wear (percentage)
        # Tyre damage (percentage)
        # Brakes damage (percentage)
        # Front left wing damage (percentage)
        # Front right wing damage (percentage)
        # Rear wing damage (percentage)
        # Floor damage (percentage)
        # Diffuser damage (percentage)
        # Sidepod damage (percentage)
        # Indicator for DRS fault, 0 = OK, 1 = fault
        # Indicator for ERS fault, 0 = OK, 1 = fault
        # Gear box damage (percentage)
        # Engine damage (percentage)
        # Engine wear MGU-H (percentage)
        # Engine wear ES (percentage)
        # Engine wear CE (percentage)
        # Engine wear ICE (percentage)
        # Engine wear MGU-K (percentage)
        # Engine wear TC (percentage)
        # Engine blown, 0 = OK, 1 = fault
        # Engine seized, 0 = OK, 1 = fault

class PacketCarDamageData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_carDamageData', CarDamageData * 22),
    ]
        # Header

class LapHistoryData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_lapTimeInMS', c_uint32),
        ('m_sector1TimeMSPart', c_uint16),
        ('m_sector1TimeMinutesPart', c_uint8),
        ('m_sector2TimeMSPart', c_uint16),
        ('m_sector2TimeMinutesPart', c_uint8),
        ('m_sector3TimeMSPart', c_uint16),
        ('m_sector3TimeMinutesPart', c_uint8),
        ('m_lapValidBitFlags', c_uint8),
    ]
        # Lap time in milliseconds
        # Sector 1 milliseconds part
        # Sector 1 whole minute part
        # Sector 2 time milliseconds part
        # Sector 2 whole minute part
        # Sector 3 time milliseconds part
        # Sector 3 whole minute part
        # 0x01 bit set-lap valid,      0x02 bit set-sector 1 valid

class TyreStintHistoryData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_endLap', c_uint8), # Lap the tyre usage ends on (255 of current tyre)
        ('m_tyreActualCompound', c_uint8), # Actual tyres used by this driver
        ('m_tyreVisualCompound', c_uint8), # Visual tyres used by this driver
    ]
        
        
        

class PacketSessionHistoryData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader), # Header
        ('m_carIdx', c_uint8), # Index of the car this lap data relates to
        ('m_numLaps', c_uint8), # Num laps in the data (including current partial lap)
        ('m_numTyreStints', c_uint8), # Number of tyre stints in the data
        ('m_bestLapTimeLapNum', c_uint8), # Lap the best lap time was achieved on
        ('m_bestSector1LapNum', c_uint8), # Lap the best Sector 1 time was achieved on
        ('m_bestSector2LapNum', c_uint8), # Lap the best Sector 2 time was achieved on
        ('m_bestSector3LapNum', c_uint8), # Lap the best Sector 3 time was achieved on
        ('m_lapHistoryData', LapHistoryData * 100), # 100 laps of data max
        ('m_tyreStintsHistoryData', TyreStintHistoryData * 8), # m_tyreStintsHistoryData[8]
    ]
        

class TyreSetData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_actualTyreCompound', c_uint8), # Actual tyre compound used
        ('m_visualTyreCompound', c_uint8), # Visual tyre compound used
        ('m_wear', c_uint8), # Tyre wear (percentage)
        ('m_available', c_uint8), # Whether this set is currently available
        ('m_recommendedSession', c_uint8), # Recommended session for tyre set, see appendix
        ('m_lifeSpan', c_uint8),  # Laps left in this tyre set
        ('m_usableLife', c_uint8), # Max number of laps recommended for this compound
        ('m_lapDeltaTime', c_int16), # Lap delta time in milliseconds compared to fitted set
        ('m_fitted', c_uint8), # Whether the set is fitted or not
    ]
        


class PacketTyreSetsData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader), # Header
        ('m_carIdx', c_uint8), # Index of the car this data relates to
        ('m_tyreSetData', TyreSetData * 20), # 13 (dry) + 7 (wet)
        ('m_fittedIdx', c_uint8), # Index into array of fitted tyre
    ]
        

class PacketMotionExData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_suspensionPosition', c_float * 4),
        ('m_suspensionVelocity', c_float * 4),
        ('m_suspensionAcceleration', c_float * 4),
        ('m_wheelSpeed', c_float * 4),
        ('m_wheelSlipRatio', c_float * 4),
        ('m_wheelSlipAngle', c_float * 4),
        ('m_wheelLatForce', c_float * 4),
        ('m_wheelLongForce', c_float * 4),
        ('m_heightOfCOGAboveGround', c_float),
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
        ('m_wheelVertForce', c_float * 4),
        ('m_frontAeroHeight', c_float),
        ('m_rearAeroHeight', c_float),
        ('m_frontRollAngle', c_float),
        ('m_rearRollAngle', c_float),
        ('m_chassisYaw', c_float),
    ]
        # Header
        # Note: All wheel arrays have the following order:
        # RL, RR, FL, FR
        # RL, RR, FL, FR
        # Speed of each wheel
        # Slip ratio for each wheel
        # Slip angles for each wheel
        # Lateral forces for each wheel
        # Longitudinal forces for each wheel
        # Height of centre of gravity above ground
        # Velocity in local space – metres/s
        # Velocity in local space
        # Velocity in local space
        # Angular velocity x-component – radians/s
        # Angular velocity y-component
        # Angular velocity z-component
        # Angular acceleration x-component – radians/s/s
        # Angular acceleration y-component
        # Angular acceleration z-component
        # Current front wheels angle in radians
        # Vertical forces for each wheel
        # Front plank edge height above road surface
        # Rear plank edge height above road surface
        # Roll angle of the front suspension
        # Roll angle of the rear suspension
        # Yaw angle of the chassis relative to the direction

class TimeTrialDataSet(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_carIdx', c_uint8), # Index of the car this data relates to
        ('m_teamId', c_uint8), # Team id - see appendix
        ('m_lapTimeInMS', c_uint32), # Lap time in milliseconds
        ('m_sector1TimeInMS', c_uint32), # Sector 1 time in milliseconds
        ('m_sector2TimeInMS', c_uint32), # Sector 2 time in milliseconds
        ('m_sector3TimeInMS', c_uint32), # Sector 3 time in milliseconds
        ('m_tractionControl', c_uint8),  # 0 = off, 1 = medium, 2 = full
        ('m_gearboxAssist', c_uint8), # 1 = manual, 2 = manual & suggested gear, 3 = auto
        ('m_antiLockBrakes', c_uint8), # 0 (off) - 1 (on)
        ('m_equalCarPerformance', c_uint8), # 0 = Realistic, 1 = Equal
        ('m_customSetup', c_uint8), # 0 = No, 1 = Yes
        ('m_valid', c_uint8), # 0 = invalid, 1 = valid
    ]
                

class PacketTimeTrialData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader), # Header
        ('m_playerSessionBestDataSet', TimeTrialDataSet), # Player session best data set
        ('m_personalBestDataSet', TimeTrialDataSet), # Personal best data set
        ('m_rivalDataSet', TimeTrialDataSet), # Rival data set
    ]




# --- AllPackets list ---
AllPackets = [
    PacketMotionData, PacketSessionData, PacketLapData, PacketEventData,
    PacketParticipantsData, PacketCarSetupData, PacketCarTelemetryData,
    PacketCarStatusData, PacketFinalClassificationData, PacketLobbyInfoData,
    PacketCarDamageData, PacketSessionHistoryData, PacketTyreSetsData,
    PacketMotionExData, PacketTimeTrialData
]





# Assuming your F1 UDP structs and packet map
# from UDP import AllPackets, PacketHeader, PacketMotionData
import socket
import threading
from collections import deque
from ctypes import sizeof



latest_data = {}  # This will always hold the latest values
listener_running = True


def udp_listener(UDP_IP="0.0.0.0", UDP_PORT=20777):
    """
    Continuously listen for F1 telemetry packets and update latest_data dict.
    Returns the most recent values from all packet types.
    """
    global latest_data

    print(f"[UDP] Listening on {UDP_IP}:{UDP_PORT}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    while listener_running:
        try:
            data, addr = sock.recvfrom(2048)
            header = PacketHeader.from_buffer_copy(data)
            packet_id = header.m_packetId

            if packet_id < 0 or packet_id >= len(AllPackets):
                continue

            PacketClass = AllPackets[packet_id]
            if len(data) < sizeof(PacketClass):
                continue

            packet = PacketClass.from_buffer_copy(data)
            player_index = header.m_playerCarIndex

            # --- Assign latest values by packet type ---
            if packet_id == 0:  # Motion
                car = packet.m_carMotionData[player_index]
                latest_data["Motion"] = {
                    "wheelSpeed": list(car.m_wheelSpeed),
                    "wheelSlipRatio": list(car.m_wheelSlipRatio),
                    "wheelSlipAngle": list(car.m_wheelSlipAngle),
                }

            elif packet_id == 1:  # Session
                latest_data["Session"] = {
                    "weather": packet.m_weather,
                    "trackLength": packet.m_trackLength,
                    "sessionType": packet.m_sessionType,
                    "trackId": packet.m_trackId,
                }

            elif packet_id == 2:  # Lap Data
                lap = packet.m_lapData[player_index]
                latest_data["Lap"] = {
                    "currentLap": lap.m_currentLapNum,
                    "lapDistance": lap.m_lapDistance,
                    "totalDistance": getattr(lap, "m_totalDistance", None),
                }

            elif packet_id == 6:  # Car Telemetry
                car = packet.m_carTelemetryData[player_index]
                latest_data["Telemetry"] = {
                    "speed": car.m_speed,
                    "throttle": car.m_throttle,
                    "brake": car.m_brake,
                    "steer": car.m_steer,
                    "gear": car.m_gear,
                }

            elif packet_id == 10:  # Car Damage
                dmg = packet.m_carDamageData[player_index]
                latest_data["Damage"] = {
                    "tyreWear": list(dmg.m_tyresWear),
                    "frontWingDamage": dmg.m_frontLeftWingDamage,
                    "rearWingDamage": dmg.m_rearWingDamage,
                    "engineDamage": dmg.m_engineDamage,
                }

        except Exception as e:
            print(f"[UDP ERROR] {e}")


def get_latest_data():
    """Return the most recent telemetry dictionary."""
    return latest_data


# --- Example standalone test ---
if __name__ == "__main__":
    t = threading.Thread(target=udp_listener, daemon=True)
    t.start()

    import time
    while True:
        # time.sleep(1)
        if latest_data:
            try:
                print(f'frontWingDamage = {latest_data['Damage']['frontWingDamage']}')
            except:
                pass
        else:
            print("[UDP] Waiting for data...")






# # --- Global Lap Tracking ---
# current_lap_number = None
# latest_player_lap = None
# latest_rival_lap = None
# rival_car_index = None

# # --- Data Stores ---
# motion_history        = deque(maxlen=500)
# motion_ex_history     = deque(maxlen=500)
# session_data          = deque(maxlen=10)
# lap_data_history      = deque(maxlen=100)
# event_data_history    = deque(maxlen=100)
# participants_data     = deque(maxlen=1)
# car_setups_data       = deque(maxlen=100)
# car_telemetry_history = deque(maxlen=1000)
# car_status_history    = deque(maxlen=1000)
# classification_data   = deque(maxlen=1)
# lobby_info_data       = deque(maxlen=1)
# car_damage_history    = deque(maxlen=1000)
# session_history_data  = deque(maxlen=10)
# tyre_sets_data        = deque(maxlen=10)
# time_trial_data       = deque(maxlen=10)
# history_lock = threading.Lock()


# # def udp_listener(UDP_IP="192.168.1.227", UDP_PORT=20777):
# def udp_listener(UDP_IP="0.0.0.0", UDP_PORT=20777):
#     """
#     Receive all F1 24 UDP packets and route them to proper histories.
#     """
#     global current_lap_number, latest_player_lap, latest_rival_lap, rival_car_index
    

#     print(f"[UDP] Listening on {UDP_IP}:{UDP_PORT}")
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.bind((UDP_IP, UDP_PORT))

#     while True:
#         data, _ = sock.recvfrom(2048)
#         header = PacketHeader.from_buffer_copy(data)
#         packet_id = header.m_packetId

#         if packet_id < 0 or packet_id >= len(AllPackets):
#             continue

#         PacketClass = AllPackets[packet_id]
#         if len(data) < sizeof(PacketClass):
#             continue

#         packet = PacketClass.from_buffer_copy(data)
#         player_car_index = header.m_playerCarIndex

#         with history_lock:

#             # --- 0: Motion ---
#             if packet_id == 0:
#                 car_motion = packet.PacketMotionExData[player_car_index]
#                 motion_history.append({
#                     "m_wheelSpeed": list(car_motion.m_wheelSpeed),
#                     # "m_wheelSlipRatio": list(car_motion.m_wheelSlipRatio),
#                     # "m_wheelSlipAngle": list(car_motion.m_wheelSlipAngle),
#                     # "m_wheelLatForce": list(car_motion.m_wheelLatForce),
#                     # "m_wheelLongForce": list(car_motion.m_wheelLongForce),
#                 })

#             # --- 1: Session ---
#             elif packet_id == 1:
#                 session_data.clear()
#                 session_data.append({
#                     "weather": packet.m_weather,
#                     "trackLength": packet.m_trackLength,
#                     "sessionType": packet.m_sessionType,
#                     "trackId": packet.m_trackId,
#                     "aiDifficulty": packet.m_aiDifficulty,
#                 })

#             # --- 2: Lap Data ---
#             elif packet_id == 2:
#                 latest_player_lap = packet.m_lapData[player_car_index]
#                 rival_car_index = packet.m_timeTrialRivalCarIdx
#                 latest_rival_lap = packet.m_lapData[rival_car_index]

#                 lap_data_history.append({
#                     "playerLap": latest_player_lap.m_currentLapNum,
#                     "playerDistance": latest_player_lap.m_lapDistance,
#                     "rivalDistance": latest_rival_lap.m_lapDistance,
#                 })

#                 # if current_lap_number is None:
#                 #     current_lap_number = latest_player_lap.m_currentLapNum

#                 # if latest_player_lap.m_currentLapNum != current_lap_number:
#                 #     print(f"[LAP] New lap {latest_player_lap.m_currentLapNum}")
#                 #     motion_history.clear()
#                 #     car_telemetry_history.clear()
#                 #     current_lap_number = latest_player_lap.m_currentLapNum

#             # --- 3: Event ---
#             elif packet_id == 3:
#                 event_data_history.append({
#                     "eventCode": bytes(packet.m_eventStringCode).decode("utf-8", errors="ignore").strip("\x00")
#                 })

#             # --- 4: Participants ---
#             elif packet_id == 4:
#                 participants_data.clear()
#                 participants_data.append({"numCars": packet.m_numActiveCars})

#             # --- 5: Car Setups ---
#             elif packet_id == 5:
#                 setup = packet.m_carSetups[player_car_index]
#                 car_setups_data.append({
#                     "frontWing": setup.m_frontWing,
#                     "rearWing": setup.m_rearWing,
#                     "onThrottle": setup.m_onThrottle,
#                     "offThrottle": setup.m_offThrottle,
#                 })


#             # --- 6: Car Telemetry ---
#             elif packet_id == 6:
#                 car = packet.m_carTelemetryData[player_car_index]

#                 # Always record player data
#                 telemetry_entry = {
#                     "speed": car.m_speed,
#                     "throttle": car.m_throttle,
#                     "brake": car.m_brake,
#                     "steer": car.m_steer,
#                     "gear": car.m_gear,
#                 }

#                 # Record rival data if available
#                 if rival_car_index is not None and rival_car_index < len(packet.m_carTelemetryData):
#                     rcar = packet.m_carTelemetryData[rival_car_index]
#                     telemetry_entry.update({
#                         "rspeed": rcar.m_speed,
#                         "rthrottle": rcar.m_throttle,
#                         "rbrake": rcar.m_brake,
#                         "rsteer": rcar.m_steer,
#                         "rgear": rcar.m_gear,
#                     })
#                 else:
#                     telemetry_entry.update({
#                         "rspeed": None,
#                         "rthrottle": None,
#                         "rbrake": None,
#                         "rsteer": None,
#                         "rgear": None,
#                     })

#                 car_telemetry_history.append(telemetry_entry)


#             # --- 7: Car Status ---
#             elif packet_id == 7:
#                 status = packet.m_carStatusData[player_car_index]
#                 car_status_history.append({
#                     "ersStore": status.m_ersStoreEnergy,
#                     "fuelRemaining": status.m_fuelRemainingLaps,
#                 })

#             # --- 8: Final Classification ---
#             elif packet_id == 8:
#                 classification_data.clear()
#                 classification_data.append({
#                     "positions": [c.m_position for c in packet.m_classificationData],
#                     "bestLap": [c.m_bestLapTimeInMS for c in packet.m_classificationData],
#                 })

#             # --- 9: Lobby Info ---
#             elif packet_id == 9:
#                 lobby_info_data.clear()
#                 lobby_info_data.append({"numPlayers": packet.m_numPlayers})

#             # --- 10: Car Damage (fixed) ---
#             elif packet_id == 10:
#                 dmg = packet.m_carDamageData[player_car_index]
#                 car_damage_history.append({
#                     "tyresWear": list(dmg.m_tyresWear),
#                     "tyresDamage": list(dmg.m_tyresDamage),
#                     "brakesDamage": list(dmg.m_brakesDamage),
#                     "frontLeftWingDamage": dmg.m_frontLeftWingDamage,
#                     "frontRightWingDamage": dmg.m_frontRightWingDamage,
#                     "rearWingDamage": dmg.m_rearWingDamage,
#                     "floorDamage": dmg.m_floorDamage,
#                     "diffuserDamage": dmg.m_diffuserDamage,
#                     "sidepodDamage": dmg.m_sidepodDamage,
#                     "gearBoxDamage": dmg.m_gearBoxDamage,
#                     "engineDamage": dmg.m_engineDamage,
#                 })

#             # --- 11: Session History ---
#             elif packet_id == 11:
#                 session_history_data.clear()
#                 session_history_data.append({
#                     "numLaps": packet.m_numLaps,
#                     "bestLapNum": packet.m_bestLapTimeLapNum,
#                 })

#             # --- 12: Tyre Sets ---

#             elif packet_id == 12:
#                 # PacketTyreSetsData has: m_header, m_carIdx, m_tyreSetData (array of TyreSetData), m_fittedIdx
#                 tyre_sets_data.clear()
#                 # build a safe list from the array of TyreSetData
#                 sets_list = []
#                 try:
#                     for t in packet.m_tyreSetData:
#                         # TyreSetData fields in your file:
#                         # m_actualTyreCompound, m_visualTyreCompound, m_wear, m_available,
#                         # m_recommendedSession, m_lifeSpan, m_usableLife, m_lapDeltaTime, m_fitted
#                         sets_list.append({
#                             "actualCompound": getattr(t, "m_actualTyreCompound", 0),
#                             "visualCompound": getattr(t, "m_visualTyreCompound", 0),
#                             "wear": getattr(t, "m_wear", 0),
#                             "available": getattr(t, "m_available", 0),
#                             "recommendedSession": getattr(t, "m_recommendedSession", 0),
#                             "lifeSpan": getattr(t, "m_lifeSpan", 0),
#                             "usableLife": getattr(t, "m_usableLife", 0),
#                             "lapDeltaTime": getattr(t, "m_lapDeltaTime", 0),
#                             "fitted": getattr(t, "m_fitted", 0),
#                         })
#                 except Exception:
#                     # defensive: if the array cannot be iterated, keep empty sets_list
#                     sets_list = []

#                 tyre_sets_data.append({
#                     "carIndex": getattr(packet, "m_carIdx", None),
#                     "fittedIdx": getattr(packet, "m_fittedIdx", None),
#                     "sets": sets_list
#                 })


#             # --- 13: Motion Ex ---
#             elif packet_id == 13:
#                 motion_ex_history.append({
#                     "suspensionPos": list(packet.m_suspensionPosition),
#                     "suspensionVel": list(packet.m_suspensionVelocity),
#                 })


#             # --- 14: Time Trial ---
#             elif packet_id == 14:
                
                
#                 player_best = packet.m_playerSessionBestDataSet
#                 personal_best = packet.m_personalBestDataSet
#                 rival_data = packet.m_rivalDataSet
#                 rival_car_index = rival_data.m_carIdx
 
 
#                 with history_lock:
#                     time_trial_data.clear()
#                     time_trial_data.append({
#                         # --- Player Session Best ---
#                         "player_car_index": player_best.m_carIdx,
#                         "player_team_id": player_best.m_teamId,
#                         "player_lap_time_ms": player_best.m_lapTimeInMS,
#                         "player_sector1_ms": player_best.m_sector1TimeInMS,
#                         "player_sector2_ms": player_best.m_sector2TimeInMS,
#                         "player_sector3_ms": player_best.m_sector3TimeInMS,
#                         "player_tc": player_best.m_tractionControl,
#                         "player_abs": player_best.m_antiLockBrakes,
#                         "player_equal_perf": player_best.m_equalCarPerformance,
#                         "player_custom_setup": player_best.m_customSetup,
#                         "player_valid": player_best.m_valid,

#                         # --- Personal Best ---
#                         "personal_lap_time_ms": personal_best.m_lapTimeInMS,
#                         "personal_sector1_ms": personal_best.m_sector1TimeInMS,
#                         "personal_sector2_ms": personal_best.m_sector2TimeInMS,
#                         "personal_sector3_ms": personal_best.m_sector3TimeInMS,
#                         "personal_valid": personal_best.m_valid,

#                         # --- Rival Data ---
#                         "rival_car_index": rival_data.m_carIdx,
#                         "rival_team_id": rival_data.m_teamId,
#                         "rival_lap_time_ms": rival_data.m_lapTimeInMS,
#                         "rival_sector1_ms": rival_data.m_sector1TimeInMS,
#                         "rival_sector2_ms": rival_data.m_sector2TimeInMS,
#                         "rival_sector3_ms": rival_data.m_sector3TimeInMS,
#                         "rival_valid": rival_data.m_valid,
#                     })

#     #

# import time
 
# if __name__ == "__main__":
#     t = threading.Thread(target=udp_listener, daemon=True)
#     t.start()

#     telemetry = {}
    
#     while True:
#         # time.sleep(0.2)
#         with history_lock:
#                 # --- LAP DATA ---
#                 if lap_data_history:
#                     telemetry['PlayerDistance'] = lap_data_history[-1].get("playerDistance", 0)
#                     telemetry['RivalDistance'] = lap_data_history[-1].get("rivalDistance", 0)
                    
#                 if motion_history:
#                     telemetry['m_wheelSlipRatio'] = motion_history[-1].get("m_wheelSlipRatio", 0)
#                     # telemetry['m_wheelSlipRatio'] = motion_history[-1].get("m_wheelSlipRatio", 0)
                    

#                 # --- TELEMETRY ---
#                 if car_telemetry_history:
#                     latest = car_telemetry_history[-1]
#                     telemetry['PlayerSpeed']     = latest.get('speed', 0)
#                     telemetry['RivalSpeed']      = latest.get('rspeed', 0)
#                     telemetry['PlayerThrottle']  = latest.get('throttle', 0)
#                     telemetry['RivalThrottle']   = latest.get('rthrottle', 0)
#                     telemetry['PlayerBrake']     = latest.get('brake', 0)
#                     telemetry['RivalBrake']      = latest.get('rbrake', 0)
#                     telemetry['PlayerGear']      = latest.get('gear', 0)
#                     telemetry['RivalGear']       = latest.get('rgear', 0)

         

#         # Convert deque to dict (serializable for dcc.Store)
#         try:
#             print(f'slip{telemetry['m_wheelSlipRatio']}')
#             print(f'PlayerDistance {telemetry['PlayerDistance']}')
#         except:
#             pass

        
            


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


# import socket
# import threading

# def udp_tester(UDP_IP="0.0.0.0", UDP_PORT=20777):
#     """
#     Basic UDP listener to verify whether F1 24 is sending telemetry packets.
#     Prints True if any signal is received.
#     """
#     print(f"[UDP] Listening on {UDP_IP}:{UDP_PORT}")
    
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.bind((UDP_IP, UDP_PORT))
#     sock.settimeout(5.0)  # Prevent blocking forever if no data

#     packet_count = 0

#     while True:
#         try:
#             data, addr = sock.recvfrom(4096)
#             packet_count += 1
#             print(f"[UDP] Packet #{packet_count} received from {addr}")
#         except socket.timeout:
#             print("[UDP] No signal received in the last 5 seconds...")
#         except Exception as e:
#             print(f"[UDP ERROR] {e}")

# # --- Test run ---
# if __name__ == "__main__":
#     t = threading.Thread(target=udp_tester, daemon=True)
#     t.start()

#     import time
#     while True:
#         time.sleep(1)
