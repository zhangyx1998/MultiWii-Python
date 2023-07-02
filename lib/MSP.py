# ===================================================================
# List of all MSP commands
# ===================================================================
# Author: Yuxuan Zhang, yuxuan@yuxuanzhang.net
# Published under MIT License
# ===================================================================
# List of all MSP commands
# ===================================================================
from collections import OrderedDict
from .ByteCode import *
from .Command import ReadCMD, WriteCMD


class IDENT(ReadCMD):
    code = 100
    struct = OrderedDict(
        VERSION=U8,
        # version of MultiWii
        MULTITYPE=U8,
        # type of multi:
        # TRI/QUADP,QUADX,BI,GIMBAL,Y6,HEX6,FLYING_WING,Y4,HEX6X,OCTOX8,
        # OCTOFLATP,OCTOFLATX,AIRPLANE,HELI_120,HELI_90,VTAIL4,HEX6H,SINGLECOPTER,DUALCOPTER
        MSP_VERSION=U8,
        # not used currently
        capability=U32,
        # A 32 bit variable to indicate capability of FC board.
        # Currently,  BIND button is used on first bit, DYNBAL on second, FLAP on third
    )


class STATUS(ReadCMD):
    code = 101
    struct = OrderedDict(
        cycleTime=U16,
        # unit: microseconds
        i2c_errors_count=U16,
        sensor=U16,
        # BARO<<1|MAG<<2|GPS<<3|SONAR<<4
        flag=U32,
        # a bit variable to indicate which BOX are active, the bit position depends on the BOX which are configured
        global_conf_currentSet=U8,
        # to indicate the current configuration setting
    )


class RAW_IMU(ReadCMD):
    code = 102
    struct = OrderedDict(
        accX=I16,
        accY=I16,
        accZ=I16,
        gyrX=I16,
        gyrY=I16,
        gyrZ=I16,
        magX=I16,
        magY=I16,
        magZ=I16,
    )


class SERVO(ReadCMD):
    """
    The servo order depends on multi type
    """

    code = 103
    struct = OrderedDict(
        **U16.ARRAY(16)
        # Range [1000;2000]
    )


MAX_SUPPORTED_MOTORS = 8


class MOTOR(ReadCMD):
    """
    Driectly set motor speeds
    The motor order depends on multi type
    Range [1000;2000]
    """

    code = 104
    struct = OrderedDict(**U16.ARRAY(MAX_SUPPORTED_MOTORS))


class SET_MOTOR(WriteCMD):
    """
    use to set individual motor value (to be used only with DYNBALANCE config)
    Range [1000;2000]
    """

    code = 214
    struct = OrderedDict(**U16.ARRAY(MAX_SUPPORTED_MOTORS))


class RC(ReadCMD):
    """
    ROLL/PITCH/YAW/THROTTLE/AUX1-AUX12
    Range [1000;2000]
    """

    code = 105
    struct = OrderedDict(
        ROLL=U16,
        PITCH=U16,
        YAW=U16,
        THROTTLE=U16,
        **U16.ARRAY(12, start=1, prefix="AUX"),
    )


class SET_RAW_RC(WriteCMD):
    """
    This request is used to inject RC channel via MSP.
    Each chan overrides legacy RX as long as it is refreshed at least every second. See UART radio projects for more details.
    """

    code = 200
    struct = OrderedDict(
        ROLL=U16,
        PITCH=U16,
        YAW=U16,
        THROTTLE=U16,
        **U16.ARRAY(12, start=1, prefix="AUX"),
    )


class RAW_GPS(ReadCMD):
    code = 106
    struct = OrderedDict(
        GPS_FIX=U8,  # 0 or 1
        GPS_numSat=U8,
        GPS_coord_LAT=U32,  # 1 / 10 000 000 deg
        GPS_coord_LON=U32,  # 1 / 10 000 000 deg
        GPS_altitude=U16,  # meter
        GPS_speed=U16,  # cm/s
        GPS_ground_course=U16,  # unit: degree*10
    )


class SET_RAW_GPS(WriteCMD):
    """
    this request is used to inject GPS data (annex GPS device or simulation purpose)
    """

    code = 201
    struct = OrderedDict(
        GPS_FIX=U8,
        GPS_numSat=U8,
        GPS_coord_LAT=U32,  # 1 / 10 000 000 deg
        GPS_coord_LON=U32,  # 1 / 10 000 000 deg
        GPS_altitude=U16,  # meter
        GPS_speed=U16,  # cm/s
    )


class COMP_GPS(ReadCMD):
    code = 107
    struct = OrderedDict(
        GPS_distanceToHome=U16,  # unit: meter
        GPS_directionToHome=U16,  # unit: degree (range [-180;+180])
        GPS_update=U8,  # a flag to indicate when a new GPS frame is received (the GPS fix is not dependent of this)
    )


class ATTITUDE(ReadCMD):
    code = 108
    struct = OrderedDict(
        angx=I16,  # Range [-1800;1800] (unit: 1/10 degree)
        angy=I16,  # Range [-900;900] (unit: 1/10 degree)
        heading=I16,  # Range [-180;180]
    )


class ALTITUDE(ReadCMD):
    code = 109
    struct = OrderedDict(
        EstAlt=I32,  # cm
        vario=I16,  # cm/s
    )


class ANALOG(ReadCMD):
    code = 110
    struct = OrderedDict(
        vbat=U8,  # unit: 1/10 volt
        intPowerMeterSum=U16,
        rssi=U16,  # range: [0;1023]
        amperage=U16,
    )


class RC_TUNING(ReadCMD):
    code = 111
    struct = OrderedDict(
        byteRC_RATE=U8,  # range [0;100]
        byteRC_EXPO=U8,  # range [0;100]
        byteRollPitchRate=U8,  # range [0;100]
        byteYawRate=U8,  # range [0;100]
        byteDynThrPID=U8,  # range [0;100]
        byteThrottle_MID=U8,  # range [0;100]
        byteThrottle_EXPO=U8,  # range [0;100]
    )


class SET_RC_TUNING(WriteCMD):
    code = 204
    struct = OrderedDict(
        byteRC_RATE=U8,
        byteRC_EXPO=U8,
        byteRollPitchRate=U8,
        byteYawRate=U8,
        byteDynThrPID=U8,
        byteThrottle_MID=U8,
        byteThrottle_EXPO=U8,
    )


# Currently, PIDITEMS is constant = 10
PIDITEMS = 10
# Order : ROLL / PITCH / YAW / ALT / POS / POSR / NAVR / LEVEL / MAG / VEL
PID_ENTRIES = [
    "ROLL",
    "PITCH",
    "YAW",
    "ALT",
    "POS",
    "POSR",
    "NAVR",
    "LEVEL",
    "MAG",
    "VEL",
]
PID_CONFIG = lambda name: {f"{name}_{entry}": U8 for entry in PID_ENTRIES}


class PID(ReadCMD):
    code = 112
    struct = OrderedDict(
        # PIDITEMS x conf.pid[]
        # 3 * PIDITEMS x UINT 8
        # VEL is not used
        **PID_CONFIG("A"),
        **PID_CONFIG("B"),
        **PID_CONFIG("C"),
    )


class SET_PID(WriteCMD):
    code = 202
    struct = OrderedDict(
        # PIDITEMS x conf.pid[]
        # 3 * PIDITEMS x UINT 8
        **PID_CONFIG("A"),
        **PID_CONFIG("B"),
        **PID_CONFIG("C"),
    )


class BOX(ReadCMD):
    code = 113
    struct = OrderedDict(
        # BOXITEMS x conf.activate[]
        # BOXITEMS x UINT 16
        # BOXITEMS number is dependant of multiwii configuration
        # The size of the message is enough to know the number of BOX
        # For each BOX, there is a 16 bit variable which indicates the AUX1->AUX4 activation switch.
        # Bit 1: AUX1 LOW state / bit 2: AUX1 MID state / bit 3: AUX1 HIGH state / bit 4: AUX2 LOW state ….. bit 13: AUX 4 HIGH state
    )


class SET_BOX(WriteCMD):
    code = 203
    struct = OrderedDict(
        # BOXITEMS x conf.activate[]
        # BOXITEMS x UINT 16
    )


class MISC(ReadCMD):
    code = 114
    struct = OrderedDict(
        intPowerTrigger1=U16,
        conf_minthrottle=U16,
        #  minimum throttle to run motor in idle state ( range [1000;2000] )
        MAXTHROTTLE=U16,
        #  maximum throttle ( range [1000;2000] )
        MINCOMMAND=U16,
        #  throttle at the lowest position ( range [1000;2000] , could be occasionally a little bit less than 1000 depending on ESCs)
        conf_failsafe_throttle=U16,
        #  should be set less than hover state ( range [1000;2000] )
        plog_arm=U16,
        # counter
        plog_lifetime=U32,
        conf_mag_declination=U16,
        # magnetic declination   ( unit:1/10 degree )
        conf_vbatscale=U8,
        conf_vbatlevel_warn1=U8,
        # unit: 1/10 volt
        conf_vbatlevel_warn2=U8,
        # unit: 1/10 volt
        conf_vbatlevel_crit=U8,
        # unit: 1/10 volt
    )


class SET_MISC(WriteCMD):
    code = 207
    struct = OrderedDict(
        intPowerTrigger1=U16,
        conf_minthrottle=U16,
        MAXTHROTTLE=U16,
        # not used currently as a set variable
        MINCOMMAND=U16,
        # not used currently as a set variable
        conf_failsafe_throttle=U16,
        plog_arm=U16,
        # not used, it's here to have the same struct as get
        plog_lifetime=U32,
        # not used, it's here to have the same struct as get
        conf_mag_declination=U16,
        # magnetic declination   ( unit:1/10 degree )
        conf_vbatscale=U8,
        conf_vbatlevel_warn1=U8,
        # unit: 1/10 volt
        conf_vbatlevel_warn2=U8,
        # unit: 1/10 volt
        conf_vbatlevel_crit=U8,
        # unit: 1/10 volt
    )


class MOTOR_PINS(ReadCMD):
    """
    motor pin indication
    """

    code = 115
    struct = OrderedDict(
        # 8 * PWM_PIN
        # 8 x UNIT 8
        **U8.ARRAY(8)
    )


# class BOXNAMES(ReadCMD):
#     # all the configured CHECKBOX name separated by ";"
#     code = 116
#     struct = OrderedDict(
#         # string of BOX items
#         # string
#     )

# class PIDNAMES(ReadCMD):
#     # all the PID name separated by ";"
#     code = 117
#     struct = OrderedDict(
#         # string of PID items
#         # string
#     )

# class WP(ReadCMD):
#     # not fully implemented yet, works partially for HOME POSITION (wp 0) and HOLD position (wp 15)
#     code = 118
#     struct = OrderedDict(
#         wp_no=U8,
#         lat=U32,
#         lon=U32,
#         AltHold=U32,
#         heading=U16,
#         time to stay=U16,
#         nav flag=U8,
#     )

# class SET_WP(WriteCMD):
#     code = 209
#     struct = OrderedDict(
#         wp_no=U8,
#         lat=U32,
#         lon=U32,
#         AltHold=U32,
#         heading=U16,
#         time to stay=U16,
#         nav flag=U8,
#     )

# class BOXIDS(ReadCMD):
#     code = 119
#     struct = OrderedDict(
#         # ID*CHECKBOXITEMS
#         # CHECKBOXITEMS x UINT 8
#         # each BOX (used or not) have a unique ID.
#         # In order to retrieve the number of BOX and which BOX are in used, this request can be used.
#         # It is more efficient than retrieving BOX names if you know what BOX function is behing the ID.
#         # See enum MultiWii.cpp (0: ARM, 1 ANGLE, 2 HORIZON, …)
#     )

# class SERVO_CONF(ReadCMD):
#     code = 120
#     struct = OrderedDict(
#         # 8 x conf.servoConf[]
#         # 8 x [UINT 16, UINT 16, UINT 16, UINT 8]
#         # struct servo_conf_ is 7 bytes length: min:2 / max:2 / middle:2 / rate:1
#         # [1000;2000], [1000;2000], [1000;2000], [0;100]
#         # Special use:
#         # middle normal range is [1000;2000]
#         # If middle < RC_CHANS => the relevant rc channel is the middle position of the servo (usefull for gimbal where you wnt to control the middle axis via a rc chan)</p><p>Depending on the servo use in multiwii type, rate is used to reverse the direction of servo (first bit) or to set a proportional range
#     )

# class SET_SERVO_CONF(WriteCMD):
#     code = 212
#     struct = OrderedDict(
#         # 8 x conf.servoConf[]
#         # 8 x [UINT 16, UINT 16, UINT 16, UINT 8]
#     )


class ACC_CALIBRATION(WriteCMD):
    """
    trigger calibration of ACC
    """

    code = 205
    struct = OrderedDict(
        # no param
    )


class MAG_CALIBRATION(WriteCMD):
    """
    trigger calibration of MAG
    """

    code = 206
    struct = OrderedDict(
        # no param
    )


class RESET_CONF(WriteCMD):
    """
    reset all params to default
    """

    code = 208
    struct = OrderedDict(
        # no param
    )


# class SELECT_SETTING(WriteCMD):
#     code = 210
#     struct = OrderedDict(
#         # global_conf.currentSet=U8,
#         # select the setting configuration (you can set for instance different pid and rate)
#         # Range: 0, 1 or 2
#     )


class SET_HEAD(WriteCMD):
    code = 211
    struct = OrderedDict(
        magHold=I16,
        # Set a new head lock reference
        # Range [-180;+180]
    )


class BIND(WriteCMD):
    """
    Currently only uses to bind spektrum sttellites
    """

    code = 240
    struct = OrderedDict(
        # no param
    )


class EEPROM_WRITE(WriteCMD):
    """
    write the settings to the eeprom
    """

    code = 250
    struct = OrderedDict(
        # no param
    )
