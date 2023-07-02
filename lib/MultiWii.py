# ===================================================================
# Python implementation of MultiWii Serial Protocol (MSP)
# ===================================================================
# Author: Yuxuan Zhang, yuxuan@yuxuanzhang.net
# Published under MIT License
# ===================================================================
# http://www.multiwii.com/wiki/index.php?title=Multiwii_Serial_Protocol
# ===================================================================
# The general format of an MSP message is:
# [ preamble | direction | size | command | <data> | crc ]
# Where:
#   preamble  = the ASCII characters '$M'
#   direction = the ASCII character '<' if to the MWC or '>' if from the MWC
#   size      = number of data bytes, binary. Can be zero as in the case of a data request to the MWC
#   command   = message_id as per the table below
#   data      = as per the table below. UINT16 values are LSB first.
#   crc       = XOR of <size>, <command> and each data byte into a zero'ed sum
# ===================================================================
import serial, glob
from .Command import ReadCMD, WriteCMD
from .ByteCode import U8


class PREAMBLE:
    SEND = b"$M<"
    RECV = b"$M>"


class MultiWii:
    def __init__(self, path: str = None, baud: int = 115200, timeout: float = 0.1):
        if path is None:
            path = glob.glob("/dev/ttyACM*")[0]
            print(f"Using serial device {path}")
        self.serial = serial.Serial(path, baud, timeout=timeout)

    def __get_byte__(self):
        read_result = list(self.serial.read())
        if len(read_result) == 0:
            # Timeout triggerred, no data received
            return None
        return U8(read_result[0])

    def __send__(self, code: int, buffer: bytes = b""):
        CODE = U8(code)
        SIZE = U8(len(buffer))
        checksum = SIZE ^ CODE
        for x in buffer:
            checksum ^= x
        checksum = U8(checksum)
        # Compose and send command
        self.serial.write(
            PREAMBLE.SEND + SIZE.bytes + CODE.bytes + buffer + checksum.bytes
        )

    def __recv__(self) -> tuple[U8, bytes]:
        # Match preamble
        preamble = 0
        while preamble < len(PREAMBLE.RECV):
            byte = self.__get_byte__()
            if byte is None:
                return None, None
            if byte == PREAMBLE.RECV[preamble]:
                preamble += 1
            else:
                preamble = 0
        # Decode header
        SIZE = self.__get_byte__()
        CODE = self.__get_byte__()
        # Buffer packet body
        DATA = self.serial.read(SIZE)
        # Decode checksum
        checksum = self.__get_byte__()
        # Verify checksum
        for x in [SIZE, CODE, *DATA]:
            checksum ^= x
        assert checksum == 0, f"Checksum failed for command {CODE}"
        # Return all fields
        return CODE, DATA

    def invoke(self, command: ReadCMD | WriteCMD) -> dict | None:
        if isinstance(command, ReadCMD):
            self.__send__(command.code)
            while True:
                code, data = self.__recv__()
                if code == command.code:
                    return command.fromBytes(data)
        elif isinstance(command, WriteCMD):
            self.__send__(command.code, command.toBytes())
        else:
            raise TypeError
        return None
