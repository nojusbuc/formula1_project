import ctypes
import enum


class PacketStructure(ctypes.LittleEndianStructure):

    _pack_ = 1

    def __repr__(self):

        fstr_list = []


        for field in self._fields_:
            fname = field[0]
            # getattr returns the value of the attribute object, if not found, returns default value provided
            value = getattr(self, fname)

            if isinstance(value, (PacketStructure, int, float, bytes)):
                vstr = repr(value)

            elif isinstance(value, ctypes.Array):
                vstr = f"[{', '.join(repr(e) for e in value)}]"

            else:
                raise RuntimeError("bad value")

            fstr = f"{fname}={vstr}"
            fstr_list.append(fstr)

        return f"[{self.__class__.__name__, ', '.join(fstr_list)}]"


class PacketHeader(PacketStructure):

    _fields_ = [
        # 2022
        ("packetFormat", ctypes.c_uint16),

        # Game major version - "X.00"
        ("gameMajorVersion", ctypes.c_uint8),

        # Game minor version -"1.XX"
        ("gameMinorVersion", ctypes.c_uint8),

        # Version of this packet type, all start from 1
        ("packetVersion", ctypes.c_uint8),

        # Identifier for the packet type, see below
        ("packetId", ctypes.c_uint8),

        # Unique identifier for the session
        ("sessionUID", ctypes.c_uint64),

        # Session timestamp
        ("sessionTime", ctypes.c_float),

        # Identifier for the frame the data was retrieved on
        ("frameIdentifier", ctypes.c_uint32),

        # Index of player"s car in the array
        ("playerCarIndex", ctypes.c_uint8),

        # Index of secondary player"s car in the array (splitscreen)
        # 255 if no second player
        ("secondaryPlayerCarIndex", ctypes.c_uint8),


    ]


@enum.unique
class PacketID(enum.IntEnum):

    MOTION = 0
    SESSION = 1
    LAP_DATA = 2
    EVENT = 3
    PARTICIPANT = 4
    CAR_SETUPS = 5
    CAR_TELEMETRY = 6
    CAR_STATUS = 7
    FINAL_CLASSIFICATION = 8
    LOBBY_INFO = 9
    CAR_DAMAGE = 10
    SESSION_HISTORY = 11


class CarMotionData(PacketStructure):

    _fields_ = [

        # World space X position
        ("worldPositionX", ctypes.c_float),

        # World space Y position
        ("worldPositionY", ctypes.c_float),

        # World space Z position
        ("worldPositionZ", ctypes.c_float),

        # Velocity in world space X
        ("worldVelocityX", ctypes.c_float),

        # Velocity in world space Y
        ("worldVelocityY", ctypes.c_float),

        # Velocity in world space Z
        ("worldVelocityZ", ctypes.c_float),

        # World space forward X direction (normalised)
        ("worldForwardDirX", ctypes.c_int16),

        # World space forward Y direction (normalised)
        ("worldForwardDirY", ctypes.c_int16),

        # World space forward Z direction (normalised)
        ("worldForwardDirZ", ctypes.c_int16),

        # World space right X direction (normalised)
        ("worldRightDirX", ctypes.c_int16),

        # World space right Y direction (normalised)
        ("worldRightDirY", ctypes.c_int16),

        # World space right Z direction (normalised)
        ("worldRightDirZ", ctypes.c_int16),

        # Lateral G-Force component
        ("gForceLateral", ctypes.c_float),

        # Longitudinal G-Force component
        ("gForceLongitudinal", ctypes.c_float),

        # Vertical G-Force component
        ("gForceVertical", ctypes.c_float),

        # Yaw angle in radians
        ("yaw", ctypes.c_float),

        # Pitch angle in radians
        ("pitch", ctypes.c_float),

        # Roll angle in radians
        ("roll", ctypes.c_float),
    ]


class PacketMotionData(PacketStructure):

    _fields_ = [

        # Header
        ("header", PacketHeader),
        # Data for all cars on track
        ("carMotionData", CarMotionData * 22),


        # // Extra player car ONLY data

        # Note: All wheel arrays have the following order:
        ("suspensionPosition", ctypes.c_float * 4),

        # RL, RR, FL, FR
        ("suspensionVelocity", ctypes.c_float * 4),

        # RL, RR, FL, FR
        ("suspensionAcceleration", ctypes.c_float * 4),

        # Speed of each wheel
        ("wheelSpeed", ctypes.c_float * 4),

        # Slip ratio for each wheel
        ("wheelSlip", ctypes.c_float * 4),

        # Velocity in local space
        ("localVelocityX", ctypes.c_float),

        # Velocity in local space
        ("localVelocityY", ctypes.c_float),

        # Velocity in local space
        ("localVelocityZ", ctypes.c_float),

        # Angular velocity x-component
        ("angularVelocityX", ctypes.c_float),

        # Angular velocity y-component
        ("angularVelocityY", ctypes.c_float),

        # Angular velocity z-component
        ("angularVelocityZ", ctypes.c_float),

        # Angular velocity x-component
        ("angularAccelerationX", ctypes.c_float),

        # Angular velocity y-component
        ("angularAccelerationY", ctypes.c_float),

        # Angular velocity z-component
        ("angularAccelerationZ", ctypes.c_float),

        # Current front wheels angle in radians
        ("frontWheelsAngle", ctypes.c_float),

    ]


class MarshalZone(PacketStructure):

    _fields_ = [

        # Fraction (0..1) of way through the lap the marshal zone starts
        ("zone_start", ctypes.c_float),

        # -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow, 4 = red
        ("zoneflag", ctypes.c_int8)

    ]


class WeatherForecastSample(PacketStructure):

    _fields_ = [

        # 0 = unknown, 1 = P1, 2 = P2, 3 = P3, 4 = Short P, 5 = Q1
        # 6 = Q2, 7 = Q3, 8 = Short Q, 9 = OSQ, 10 = R, 11 = R2
        # 12 = R3, 13 = Time Trial
        ("sessionType", ctypes.c_uint8),

        # Time in minutes the forecast is for
        ("timeOffset", ctypes.c_uint8),

        # Weather - 0 = clear, 1 = light cloud, 2 = overcast 3 = light rain,
        # 4 = heavy rain, 5 = storm
        ("weather", ctypes.c_uint8),

        # Track temp. in degrees Celsius
        ("trackTemperature", ctypes.c_int8),

        # Track temp. change –0 = up, 1 = down, 2 = no change
        ("trackTemperatureChange", ctypes.c_int8),

        # Air temp. in degrees celsius
        ("airTemperature", ctypes.c_int8),

        # Air temp. change –0 = up, 1 = down, 2 = no change
        ("airTemperatureChange", ctypes.c_int8),

        # Rain percentage (0-100)
        ("rainPercentage", ctypes.c_uint8)

    ]


class PacketSessionData(PacketStructure):

    _fields_ = [

        # Header
        ("header", PacketHeader),

        # Weather - 0 = clear, 1 = light cloud, 2 = overcast // 3 = light rain,
        # 4 = heavy rain, 5 = storm
        ("weather", ctypes.c_uint8),

        # Track temp. in degrees celsius
        ("trackTemperature", ctypes.c_int8),

        # Air temp. in degrees celsius
        ("airTemperature", ctypes.c_int8),

        # Total number of laps in this race
        ("totalLaps", ctypes.c_uint8),

        # Track length in metres
        ("trackLength", ctypes.c_uint16),

        # 0 = unknown, 1 = P1, 2 = P2, 3 = P3, 4 = Short P// 5 = Q1, 6 = Q2, 7 = Q3,
        # 8 =Short Q, 9 = OSQ// 10 = R, 11 = R2, 12 = R3, 13= Time Trial
        ("sessionType", ctypes.c_uint8),

        # -1 for unknown, see appendix
        ("trackId", ctypes.c_int8),

        # 3 = F1 Generic, 4 = Beta, 5 = Supercars//6 = Esports, 7 = F2 2021
        ("formula", ctypes.c_uint8),

        # Time left in session in seconds
        ("sessionTimeLeft", ctypes.c_uint16),

        # Session duration in seconds
        ("sessionDuration", ctypes.c_uint16),

        # Pit speed limit in kilometres per hour
        ("pitSpeedLimit", ctypes.c_uint8),

        # Whether the game is paused–network game only
        ("gamePaused", ctypes.c_uint8),

        # Whether the player is spectating
        ("isSpectating", ctypes.c_uint8),

        # Index of the car being spectated
        ("spectatorCarIndex", ctypes.c_uint8),

        # SLI Pro support, 0 = inactive, 1 = active
        ("sliProNativeSupport", ctypes.c_uint8),

        # Number of marshal zones to follow
        ("numMarshalZones", ctypes.c_uint8),

        # List of marshal zones – max 21 uint8
        ("marshalZones", MarshalZone * 21),

        # 0 = no safety car, 1 = full // 2 = virtual, 3 = formation lap
        ("safetyCarStatus", ctypes.c_uint8),

        # 0 = offline, 1 = online
        ("networkGame", ctypes.c_uint8),

        # Number of weather samples to follow
        ("numWeatherForecastSamples", ctypes.c_uint8),

        # Array of weather forecast samples
        ("weatherForecastSamples", WeatherForecastSample * 56),

        # 0 = Perfect, 1 = Approximate
        ("forecastAccuracy", ctypes.c_uint8),

        # AI Difficultyrating – 0-110
        ("aiDifficulty", ctypes.c_uint8),

        # Identifier for season -persists across saves
        ("seasonLinkIdentifier", ctypes.c_uint32),

        # Identifier for weekend -persists across saves
        ("weekendLinkIdentifier", ctypes.c_uint32),

        # Identifier for session - persists across saves
        ("sessionLinkIdentifier", ctypes.c_uint32),

        # Ideal lap to pit on for current strategy (player)
        ("pitStopWindowIdealLap", ctypes.c_uint8),

        # Latest lap to pit on for current strategy (player)
        ("pitStopWindowLatestLap", ctypes.c_uint8),

        # Predicted position to rejoin at (player)
        ("pitStopRejoinPosition", ctypes.c_uint8),

        # 0 = off, 1 = on
        ("steeringAssist", ctypes.c_uint8),

        # 0 = off, 1 = on
        ("brakingAssist", ctypes.c_uint8),

        # 0 = off, 1 = on
        ("gearboxAssist", ctypes.c_uint8),

        # 0 = off, 1 = on
        ("pitAssist", ctypes.c_uint8),

        # 0 = off, 1 = on
        ("pitReleaseAssist", ctypes.c_uint8),

        # 0 = off, 1 = on
        ("ERSAssist", ctypes.c_uint8),

        # 0 = off, 1 = on
        ("DRSAssist", ctypes.c_uint8),

        # 0 = off, 1 = corners only, 2 = full
        ("dynamicRacingLine", ctypes.c_uint8),

        # 0 = 2D, 1 = 3D
        ("dynamicRacingLineType", ctypes.c_uint8),

        # Game mode id -see appendix
        ("gameMode", ctypes.c_uint8),

        # Ruleset -see appendix
        ("ruleSet", ctypes.c_uint8),

        # Local time of day -minutes since midnight
        ("timeOfDay", ctypes.c_uint32),

        # 0 = None, 2 = Very Short, 3 = Short, 4 = Medium//5 = Medium Long, 6 = Long, 7 = Full
        ("sessionLength", ctypes.c_uint8),

    ]


class LapData(PacketStructure):

    _fields_ = [

        # Last lap time in milliseconds
        ("lastLapTimeInMS", ctypes.c_uint32),

        # Current time around the lap in milliseconds
        ("currentLapTimeInMS", ctypes.c_uint32),

        # Sector 1 time in milliseconds
        ("sector1TimeInMS", ctypes.c_uint16),

        # Sector 2 time in milliseconds
        ("sector2TimeInMS", ctypes.c_uint16),

        # Distance vehicle is around current lap in metres – could
        # be negative if line hasn’t been crossed yet
        ("lapDistance", ctypes.c_float),

        # Total distance travelled in session in metres – could
        # be negative if line hasn’t been crossed yet
        ("totalDistance", ctypes.c_float),

        # Delta in seconds for safety car
        ("safetyCarDelta", ctypes.c_float),

        # Car race position
        ("carPosition", ctypes.c_uint8),

        # Current lap number
        ("currentLapNum", ctypes.c_uint8),

        # 0 = none, 1 = pitting,2 = in pit area
        ("pitStatus", ctypes.c_uint8),

        # Number of pit stops taken in this race
        ("numPitStops", ctypes.c_uint8),

        # 0 = sector1, 1 = sector2, 2 = sector3
        ("sector", ctypes.c_uint8),

        # Current lap invalid -0 = valid, 1= invalid
        ("currentLapInvalid", ctypes.c_uint8),

        # Accumulated time penalties in seconds to be added
        ("penalties", ctypes.c_uint8),

        # Accumulated number of warnings issued
        ("warnings", ctypes.c_uint8),

        # Num drive through pens left to serve
        ("numUnservedDriveThroughPens", ctypes.c_uint8),

        #  Num stop go pens left to serve
        ("numUnservedStopGoPens", ctypes.c_uint8),

        # Grid position the vehicle started the racein
        ("gridPosition", ctypes.c_uint8),

        # Status of driver - 0 = in garage, 1 = flying lap
        # 2 = in lap, 3 = out lap, 4 = on track
        ("driverStatus", ctypes.c_uint8),

        # Result status - 0 = invalid, 1 = inactive, 2 = active 3 = finished,
        # 4 = didnotfinish, 5 = disqualified 6 = not classified, 7 = retired
        ("resultStatus", ctypes.c_uint8),

        # Pit lane timing, 0 = inactive, 1 = active
        ("pitLaneTimerActive", ctypes.c_uint8),

        # If active, the current time spent in the pit lane in ms
        ("pitLaneTimeInLaneInMS", ctypes.c_uint16),

        # Time of the actual pit stop in ms
        ("pitStopTimerInMS", ctypes.c_uint16),

        # Whether the car should serve a penalty at this stop
        ("pitStopShouldServePen", ctypes.c_uint8),

    ]


class PacketLapData(PacketStructure):

    _fields_ = [

        # Header
        ("header", PacketHeader),

        # Lap data for all cars on track
        ("lapData", LapData*22),

        # Index of Personal Bestcar in time trial (255 if invalid)
        ("timeTrialPBCarIdx", ctypes.c_uint8),

        # Index of Rival car in time trial (255 if invalid
        ("timeTrialRivalCarIdx", ctypes.c_uint8),

    ]


class FastestLapData(PacketStructure):

    _fields_ = [

        # Vehicle index of car achieving fastest lap
        ("vehicleIdx", ctypes.c_uint8),

        # Lap time is in seconds
        ("lapTime", ctypes.c_float),

    ]


class RetirementData(PacketStructure):

    _fields_ = [

        # Vehicle index of car retiring
        ("vehicleIdx", ctypes.c_uint8),

    ]


class TeamMateInPitsData(PacketStructure):

    _fields_ = [

        # Vehicle index of team mate
        ("vehicleIdx", ctypes.c_uint8),

    ]


class RaceWinnerData(PacketStructure):

    _fields_ = [

        # Vehicle index of team mate
        ("vehicleIdx", ctypes.c_uint8),

    ]


class PenaltyData(PacketStructure):

    _fields_ = [

        # Penalty type –see Appendices
        ("penaltyType", ctypes.c_uint8),

        # Infringement type –see Appendices
        ("infringementType", ctypes.c_uint8),

        # Vehicle index of the car the penalty is applied to
        ("vehicleIdx", ctypes.c_uint8),

        # Vehicle index of the other car involved
        ("otherVehicleIdx", ctypes.c_uint8),

        # Time gained, or time spent doing actionin seconds
        ("time", ctypes.c_uint8),

        # Lap the penalty occurred on
        ("lapNum", ctypes.c_uint8),

        # Number of places gained by this
        ("placesGained", ctypes.c_uint8),

    ]


class SpeedTrapData(PacketStructure):

    _fields_ = [

        # Vehicle index of the vehicle triggering speedtrap
        ("vehicleIdx", ctypes.c_uint8),

        # Top speed achieved in kilometres per hour
        ("speed", ctypes.c_float),

        # Overall fastest speed in session = 1, otherwise 0
        ("isOverallFastestInSession", ctypes.c_uint8),

        # Fastest speed for driver in session = 1, otherwise 0
        ("isDriverFastestInSession", ctypes.c_uint8),

        # Vehicle index of the vehicle that is the fastest
        # in this session
        ("fastestVehicleIdxInSession", ctypes.c_uint8),

        # Speed of the vehicle that is the fastest
        # in this session
        ("fastestSpeedInSession", ctypes.c_float),

    ]


class StartLightsData(PacketStructure):

    _fields_ = [

        # Number of lights showing
        ("numLights", ctypes.c_uint8),

    ]


class DriveThroughPenaltyServedData(PacketStructure):

    _fields_ = [

        # ehicle index of the vehicle serving drive through
        ("vehicleIdx", ctypes.c_uint8),

    ]


class StopGoPenaltyServedData(PacketStructure):

    _fields_ = [

        # Vehicle index of the vehicle serving stop go
        ("vehicleIdx", ctypes.c_uint8),

    ]


class FlashbackData(PacketStructure):

    _fields_ = [

        # Frame identifier flashed back to
        ("flashBackFrameIdentifier", ctypes.c_uint32),

        # Session time flashed back to
        ("flashBackSessionTime", ctypes.c_float),

    ]


class ButtonsData(PacketStructure):

    _fields_ = [

        # Bit flags specifying which buttons are being pressed
        # currently - see appendices
        ("buttonStatus", ctypes.c_uint32),

    ]


# The event details packet is different for each type of event.
# Make sure only the correct type is interpreted.

class EventDataDetails(ctypes.Union):

    _fields_ = [

        ("fastestLap", FastestLapData),
        ("retirement", RetirementData),
        ("teamMateInPits", TeamMateInPitsData),
        ("raceWinner", RaceWinnerData),
        ("penalty", PenaltyData),
        ("speedTrap", SpeedTrapData),
        ("startLights", StartLightsData),
        ("driveThroughPenaltyServed", DriveThroughPenaltyServedData),
        ("stopGoPenaltyServed", StopGoPenaltyServedData),
        ("flashback", FlashbackData),
        ("buttons", ButtonsData)

    ]


class PacketEventData(PacketStructure):

    _fields_ = [

        # Header
        ("header", PacketHeader),

        # Event string code, see below
        ("eventStringCode", ctypes.c_char * 4),

        # Event details -should be interpreted differently
        # for each type
        ("eventDetails", EventDataDetails)

    ]

    def __repr__(self):
        event = self.eventStringCode.decode()

        if event in ["CHQF", "DRSD", "DRSE", "SEND", "SSTA", "LGOT"]:
            end = ")"
        else:
            if event == "FTLP":
                event_details = self.eventDetails.fastestLap
            elif event == "PENA":
                event_details = self.eventDetails.penalty
            elif event == "RCWN":
                event_details = self.eventDetails.raceWinner
            elif event == "RTMT":
                event_details = self.eventDetails.retirement
            elif event == "SPTP":
                event_details = self.eventDetails.speedTrap
            elif event == "TMPT":
                event_details = self.eventDetails.teamMateInPits
            elif event == "STLG":
                event_details = self.eventDetails.startLights
            elif event == "DTSV":
                event_details = self.eventDetails.driveThroughPenaltyServed
            elif event == "SGSV":
                event_details = self.eventDetails.stopGoPenaltyServed
            elif event == "FLBK":
                event_details = self.eventDetails.flashback
            elif event == "BUTN":
                event_details = self.eventDetails.buttons

            else:
                raise RuntimeError(f"Bad event code {event}")

            end = f", eventDetails={event_details!r})"

        return f"{self.__class__.__name__}(header={self.header!r}, eventStringCode={self.eventStringCode!r}{end}"


class EventStringCode(enum.Enum):

    SSTA = b"SSTA"
    SEND = b"SEND"
    FTLP = b"FTLP"
    RTMT = b"RTMT"
    DRSE = b"DRSE"
    DRSD = b"DRSD"
    TMPT = b"TMPT"
    CHQF = b"CHQF"
    RCWN = b"RCWN"
    PENA = b"PENA"
    SPTP = b"SPTP"
    STLG = b"STLG"
    LGOT = b"LGOT"
    DTSV = b"DTSV"
    SGSV = b"SGSV"
    FLBK = b"FLBK"
    BUTN = b"BUTN"


class ParticipantData(PacketStructure):

    _fields_ = [

        # Whether the vehicle is AI (1) or Human (0) controlled
        ("aiControlled", ctypes.c_uint8),

        # Driver id - see appendix, 255 if network human
        ("driverId", ctypes.c_uint8),

        # Network id – unique identifier for network players
        ("networkId", ctypes.c_uint8),

        # Team id - see appendix
        ("teamId", ctypes.c_uint8),

        # My team flag – 1 = My Team, 0 = otherwise
        ("myTeam", ctypes.c_uint8),

        # Race number of the car
        ("raceNumber", ctypes.c_uint8),

        # Nationality of the driver
        ("nationality", ctypes.c_uint8),

        # Name of participantin UTF-8 format – null terminated
        # Will be truncated with ... (U+2026) if too long
        ("name", ctypes.c_char*48),

        # The player"s UDP setting, 0 = restricted, 1 = public
        ("yourTelemetry", ctypes.c_uint8),

    ]


class PacketParticipantsData(PacketStructure):

    _fields_ = [

        # Header
        ("header", PacketHeader),

        # Number of active cars in the data–should match number of
        # cars on HUD
        ("numActiveCars", ctypes.c_uint8),

        # List of participants
        ("participants", ParticipantData * 22),

    ]


class CarSetupData(PacketStructure):

    _fields_ = [

        # Front wing aerouint8
        ("frontWing", ctypes.c_uint8),

        # Rear wing aero
        ("rearWing", ctypes.c_uint8),

        # Differential adjustment on throttle (percentage)
        ("onThrottle", ctypes.c_uint8),

        # Differential adjustment off throttle (percentage)
        ("offThrottle", ctypes.c_uint8),

        # Front camber angle (suspension geometry)
        ("frontCamber", ctypes.c_float),

        # Rear camber angle (suspension geometry)
        ("rearCamber", ctypes.c_float),

        # Front toe angle (suspension geometry)
        ("frontToe", ctypes.c_float),

        # Rear toe angle (suspension geometry)
        ("rearToe", ctypes.c_float),

        # Front suspension
        ("frontSuspension", ctypes.c_uint8),

        # Rear suspension
        ("rearSuspension", ctypes.c_uint8),

        # Front anti-roll bar
        ("frontAntiRollBar", ctypes.c_uint8),

        # Front anti-roll bar
        ("rearAntiRollBar", ctypes.c_uint8),

        # Front ride height
        ("frontSuspensionHeight", ctypes.c_uint8),

        # Rear ride height
        ("rearSuspensionHeight", ctypes.c_uint8),

        # Brake pressure (percentage)
        ("brakePressure", ctypes.c_uint8),

        # Brake bias (percentage)
        ("brakeBias", ctypes.c_uint8),

        # Rear left tyre pressure(PSI)
        ("rearLeftTyrePressure", ctypes.c_float),

        # Rear right tyre pressure (PSI)
        ("rearRightTyrePressure", ctypes.c_float),

        # Front left tyre pressure (PSI)
        ("frontLeftTyrePressure", ctypes.c_float),

        # Front right tyre pressure (PSI)
        ("frontRightTyrePressure", ctypes.c_float),

        # Ballast
        ("ballast", ctypes.c_uint8),

        # Fuel load
        ("fuelLoad", ctypes.c_float),

    ]


class PacketCarSetupData(PacketStructure):

    _fields_ = [

        # Header
        ("header", PacketHeader),

        # List of car setups
        ("carSetups", CarSetupData * 22)

    ]


class CarTelemetryData(PacketStructure):

    _fields_ = [

        # Speed of car in kilometres per hour
        ("speed", ctypes.c_uint16),

        # Amount of throttle applied (0.0 to 1.0)
        ("throttle", ctypes.c_float),

        # Steering (-1.0 (full lock left) to 1.0 (full lock right))
        ("steer", ctypes.c_float),

        # Amount of brake applied (0.0 to 1.0)
        ("brake", ctypes.c_float),

        # Amount of clutch applied (0 to 100)
        ("clutch", ctypes.c_uint8),

        # Gear selected (1-8, N=0, R=-1)
        ("gear", ctypes.c_int8),

        # Engine RPM
        ("engineRPM", ctypes.c_uint16),

        # 0 = off, 1 = on
        ("drs", ctypes.c_uint8),

        # Rev lights indicator (percentage)
        ("revLightsPercent", ctypes.c_uint8),

        # Rev lights (bit 0 = leftmost LED, bit 14 = rightmost LED)
        ("revLightsValue", ctypes.c_uint16),

        # Brakes temperature (celsius)
        ("brakesTemperature", ctypes.c_uint16 * 4),

        # Tyres surface temperature (celsius)
        ("tyresSurfaceTemperature", ctypes.c_uint8 * 4),

        # Tyres inner temperature (celsius)
        ("tyresInnerTemperature", ctypes.c_uint8 * 4),

        # Engine temperature (celsius)
        ("engineTemperature", ctypes.c_uint16),

        # Tyres pressure (PSI)
        ("tyresPressure", ctypes.c_float * 4),

        # Driving surface, see appendices
        ("surfaceType", ctypes.c_uint8 * 4),

    ]


class PacketCarTelemetryData(PacketStructure):

    _fields_ = [

        # Header
        ("header", PacketHeader),

        # List of cars" telemetry
        ("carTelemetryData", CarTelemetryData * 22),

        # Index of MFD panel open - 255 = MFD closed
        # Single player, race – 0 = Car setup, 1 = Pits
        # 2 = Damage, 3 =  Engine, 4 = Temperatures
        ("mfdPanelIndex", ctypes.c_uint8),

        #
        ("mfdPanelSecondaryPlayer", ctypes.c_uint8),

        # Suggested gear for the player (1-8)
        # 0 if no gear suggested
        ("suggestedGear", ctypes.c_int8)

    ]


class CarStatusData(PacketStructure):

    _fields_ = [

        # Traction control - 0 = off, 1 = medium, 2 full
        ("tractionControl", ctypes.c_uint8),

        # 0 (off) -1 (on)
        ("antiLockBrakes", ctypes.c_uint8),

        # Fuel mix -0 = lean, 1 = standard, 2 = rich, 3 = max
        ("fuelMix", ctypes.c_uint8),

        # Front brake bias (percentage)
        ("frontBrakeBias", ctypes.c_uint8),

        # Pit limiter status -0 = off, 1 = on
        ("pitLimiterStatus", ctypes.c_uint8),

        # Current fuel mass
        ("fuelInTank", ctypes.c_float),

        # Fuel capacity
        ("fuelCapacity", ctypes.c_float),

        # Fuel remaining in terms of laps(value on MFD
        ("fuelRemainingLaps", ctypes.c_float),

        # Cars max RPM, point of rev limiter
        ("maxRPM", ctypes.c_uint16),

        # Cars idle RP
        ("idleRPM", ctypes.c_uint16),

        # Maximum number of gears
        ("maxGears", ctypes.c_uint8),

        # 0 = not allowed, 1 = allowed
        ("drsAllowed", ctypes.c_uint8),

        # 0 = DRS not available, non-zero -DRS will be available
        # in [X] metres
        ("drsActivationDistance", ctypes.c_uint16),

        # F1 Modern - 16 = C5, 17 = C4, 18 = C3, 19 = C2, 20 = C1
        # 7 = inter, 8 = wet
        # F1 Classic - 9 = dry, 10 = wet
        # F2 – 11 = super soft, 12 = soft, 13 = medium, 14 = hard
        # 15 = wet
        ("actualTyreCompound", ctypes.c_uint8),

        # F1 visual (can be different from actual compound)
        # 16 = soft, 17 = medium, 18 = hard, 7 = inter, 8 = wet
        # F1 Classic – same as above
        # F2 ‘19, 15 = wet, 19 – super soft, 20 = soft
        # 21 = medium , 22 = hard
        ("visualTyreCompound", ctypes.c_uint8),

        # Age in laps of the current set of tyres
        ("tyresAgeLap", ctypes.c_uint8),

        # -1 = invalid/unknown, 0 = none, 1 = green
        # 2 = blue, 3 = yellow, 4 = red
        ("VehicleFiaFlags", ctypes.c_int8),

        # ERS energy store in Joules
        ("ersStoreEnergy", ctypes.c_float),

        # ERS deployment mode, 0 = none, 1 = medium
        # 2 = hotlap, 3 = overtake
        ("ersDeployMode", ctypes.c_uint8),

        # ERS energy harvested this lap by MGU-K
        ("ersHarvestedThisLapMGUK", ctypes.c_float),

        # ERS energy harvested this lap by MGU-H
        ("ersHarvestedThisLapMGUH", ctypes.c_float),

        # ERS energy deployed this lap
        ("ersDeployedThisLap", ctypes.c_float),

        # Whether the car is paused in a network game
        ("networkPaused", ctypes.c_uint8),

    ]


class PacketCarStatusData(PacketStructure):

    _fields_ = [

        # Header
        ("header", PacketHeader),

        # List of cars" status
        ("carStatusData", CarStatusData * 22),

    ]


class FinalClassificationData(PacketStructure):
    _fields_ = [

        # Finishing position
        ("position", ctypes.c_uint8),

        # Number of laps completed
        ("numLaps", ctypes.c_uint8),

        # Grid position of the car
        ("gridPosition", ctypes.c_uint8),

        # Number of points scored
        ("points", ctypes.c_uint8),

        # Number of pit stops made
        ("numPitStops", ctypes.c_uint8),

        # Result status - 0 = invalid, 1 = inactive, 2 = active
        # 3 = finished, 4 = didnotfinish, 5 = disqualified
        # 6 = not classified, 7 = retired
        ("resultStatus", ctypes.c_uint8),

        # Best lap time of the session in milliseconds
        ("bestLapTimeInMS", ctypes.c_uint32),

        # Total race time in seconds without penaltie
        ("totalRaceTime", ctypes.c_double),

        # Total penalties accumulated in seconds
        ("penaltiesTime", ctypes.c_uint8),

        # Number of penalties applied to this driver
        ("numPenalties", ctypes.c_uint8),

        # Number of tyres stints up to maximum
        ("numTyreStints", ctypes.c_uint8),

        # Actual tyres used by this driver
        ("tyreStintsActual", ctypes.c_uint8 * 8),

        # Visual tyres used by this driver
        ("tyreStintsVisual", ctypes.c_uint8 * 8),

        # The lap number stintsend on
        ("tyreStintsEndLaps", ctypes.c_uint8 * 8),

    ]


class PacketFinalClassificationData(PacketStructure):

    _fields_ = [

        # Header
        ("header", PacketHeader),

        # Number of cars in the final classification
        ("numCars", ctypes.c_uint8),

        # Final classification data for all cars
        ("classificationData", FinalClassificationData * 22),

    ]


class LobbyInfoData(PacketStructure):

    _fields_ = [

        # Whether the vehicle is AI (1) or Human (0) controlled
        ("aiControlled", ctypes.c_uint8),

        # Team id -see appendix (255 if no team currently selected)
        ("teamId", ctypes.c_uint8),

        # Nationality of the driver
        ("nationality", ctypes.c_uint8),

        # Name of participant in UTF-8 format –null terminated
        # Will be truncated with ... (U+2026) if too long
        ("name", ctypes.c_char * 48),

        # Car number of the player
        ("carNumber", ctypes.c_uint8),

        # 0 = not ready, 1 = ready, 2 = spectating
        ("readyStatus", ctypes.c_uint8),

    ]


class PacketLobbyInfoData(PacketStructure):

    _fields_ = [

        # Header
        ("header", PacketHeader),

        # Number of players in the lobby data
        ("numPlayers", ctypes.c_uint8),

        # Lobby info for all players
        ("lobbyPlayers", LobbyInfoData * 22),

    ]


class CarDamageData(PacketStructure):

    _fields_ = [

        # Tyre wear (percentage)
        ("tyresWear", ctypes.c_float * 4),

        # Tyre damage (percentage)
        ("tyresDamage", ctypes.c_uint8 * 4),

        # Brakes damage (percentage)
        ("brakesDamage", ctypes.c_uint8 * 4),

        # Front left wing damage(percentage)
        ("frontLeftWingDamage", ctypes.c_char),

        # Front right wing damage (percentage)
        ("frontRightWingDamage", ctypes.c_uint8),

        # Rear wing damage (percentage)
        ("rearWingDamage", ctypes.c_uint8),

        # Floor damage (percentage)
        ("floorDamage", ctypes.c_uint8),

        # Diffuser damage (percentage)
        ("diffuserDamage", ctypes.c_uint8),

        # Sidepod damage (percentage)
        ("sidepodDamage", ctypes.c_uint8),

        # Indicator for DRS fault, 0 = OK, 1 = fault
        ("drsFault", ctypes.c_uint8),

        # Indicator for ERS fault, 0 = OK, 1 = fault
        ("ersFault", ctypes.c_uint8),

        # Gear box damage (percentage)
        ("gearBoxDamage", ctypes.c_uint8),

        # Engine damage (percentage)
        ("engineDamage", ctypes.c_uint8),

        # Engine wear MGU-H (percentage)
        ("engineMGUHWear", ctypes.c_uint8),

        # Engine wear ES (percentage)
        ("engineESWear", ctypes.c_uint8),

        # Engine wear CE (percentage)
        ("engineCEWear", ctypes.c_uint8),

        # Engine wear ICE (percentage)
        ("engineICEWear", ctypes.c_uint8),

        # Engine wear MGU-K (percentage)
        ("engineMGUKWear", ctypes.c_uint8),

        # Engine wear TC (percentage)
        ("engineTCWearWear", ctypes.c_uint8),

        # Engine blown, 0 = OK, 1 = fault
        ("engineBlown", ctypes.c_uint8),

        # Engine seized, 0 = OK, 1 = fault
        ("engineSeized", ctypes.c_uint8),

    ]


class PacketCarDamageData(PacketStructure):

    _fields_ = [

        # Header
        ("header", PacketHeader),
        # List of car damage of each car
        ("carDamageData", CarDamageData * 22),

    ]


class LapHistoryData(PacketStructure):

    _fields_ = [

        # Lap time in milliseconds
        ("lapTimeInMS", ctypes.c_uint32),

        # Sector 1 time in milliseconds
        ("sector1TimeInMS", ctypes.c_uint16),

        # Sector 2 time in milliseconds
        ("sector2TimeInMS", ctypes.c_uint16),

        # Sector 3 time in milliseconds
        ("sector3TimeInMS", ctypes.c_uint16),

        # 0x01 bit set-lap valid,
        # 0x02 bit set-sector 1 valid
        # 0x04 bit set-sector 2 valid,
        # 0x08 bit set-sector 3 valid
        ("lapValidBitFlags", ctypes.c_uint8),

    ]


class TyreStintHistoryData(PacketStructure):

    _fields_ = [

        # Lap the tyre usage ends on (255 of current tyre)
        ("endLap", ctypes.c_uint8),

        # Actual tyres used by this driver
        ("tyreActualCompound", ctypes.c_uint8),

        # Visual tyres used by this driver
        ("tyreVisualCompound", ctypes.c_uint8),

    ]


class PacketSessionHistoryData(PacketStructure):

    _fields_ = [
        # Header
        ("header", PacketHeader),

        # Index of the car this lap data relates to
        ("carIdx", ctypes.c_uint8),

        # Num laps in the data(including current partial lap)
        ("numLaps", ctypes.c_uint8),

        # Number of tyre stints in the data
        ("numTyreStints", ctypes.c_uint8),

        # Lap the best lap time was achieved on
        ("bestLapTimeNum", ctypes.c_uint8),

        # Lap the best Sector 1 time was achieved on
        ("bestSector1LapNum", ctypes.c_uint8),

        # Lap the best Sector 2 time was achieved on
        ("bestSector2LapNum", ctypes.c_uint8),

        # Lap the best Sector 3 time was achieved on
        ("bestSector3LapNum", ctypes.c_uint8),

        # 100 laps of data max
        ("lapHistoryData", LapHistoryData * 100),

        # List of tyre stints
        ("tyreStintsHistoryData", TyreStintHistoryData * 8),
    ]


HeaderFieldsToPacketType = {

    (2022, 1, 0): PacketMotionData,
    (2022, 1, 1): PacketSessionData,
    (2022, 1, 2): PacketLapData,
    (2022, 1, 3): PacketEventData,
    (2022, 1, 4): PacketParticipantsData,
    (2022, 1, 5): PacketCarSetupData,
    (2022, 1, 6): PacketCarTelemetryData,
    (2022, 1, 7): PacketCarStatusData,
    (2022, 1, 8): PacketFinalClassificationData,
    (2022, 1, 9): PacketLobbyInfoData,
    (2022, 1, 10): PacketCarDamageData,
    (2022, 1, 11): PacketSessionHistoryData,

}


class UnpackError(Exception):
    pass


#function that returns a more structured object from udp stream
def unpack_udp_packet(packet: bytes) -> PacketStructure: 

    # gets the size of the packet and its header
    packet_size = len(packet)
    header_size = ctypes.sizeof(PacketHeader)

    # compares packet and packet header size. In this case, the packets are always larger than
    # their headers. To avoid stopping the program, a custom exception is raised.
    if packet_size < header_size:
        raise UnpackError(
            f"Bad telemetry packet: too short ({packet_size} bytes)")

    # copies a buffer object PacketHeader to a variable
    header = PacketHeader.from_buffer_copy(packet)
    # separates the buffer object into information that will be required later
    key = (header.packetFormat, header.packetVersion, header.packetId)

    # exception handling if the packet information does not have the expected value
    if key not in HeaderFieldsToPacketType:
        raise UnpackError("bad telemetry packet")

    #getting the size of the expected packet based on its id
    packet_type = HeaderFieldsToPacketType[key]
    expected_packet_size = ctypes.sizeof(packet_type)

    # exception handling if packet sizes do not match
    if packet_size != expected_packet_size:

        raise UnpackError(
            "Bad telemetry packet: bad size for {} packet; expected {} bytes but received {} bytes. header size = {}".format(
                packet_type.__name__, expected_packet_size, packet_size, header_size))

    # returning the buffer object of the packet
    return packet_type.from_buffer_copy(packet)




