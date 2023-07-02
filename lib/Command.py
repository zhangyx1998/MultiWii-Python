# ===================================================================
# Class prototype for MSP commands
# ===================================================================
# Author: Yuxuan Zhang, yuxuan@yuxuanzhang.net
# Published under MIT License
# ===================================================================
from collections import OrderedDict
from . import ByteCode as BC


class MSP_Command:
    code: int
    struct: OrderedDict


class ReadCMD(MSP_Command):
    def fromBytes(self, buffer: bytes) -> dict:
        result = OrderedDict()
        buffer_size = len(buffer)
        buffer = list(buffer)
        for key, dtype in self.struct.items():
            byte_size = dtype.byte_size
            assert (
                len(buffer) >= byte_size
            ), f"insufficient buffer for {self.__class__.__name__} (got {buffer_size} bytes)"
            chunk = buffer[:byte_size]
            result[key] = dtype.fromBytes(chunk)
            buffer = buffer[byte_size:]
        assert len(buffer) == 0, f"excess buffer for {self.__class__.__name__}"
        return dict(result)


class WriteCMD(MSP_Command):
    payload: OrderedDict[any, BC.TypedInteger]

    def __init__(self, *args, **kwargs):
        self.payload = OrderedDict()
        entries = self.struct.items()
        indexes = range(len(entries))
        for index, (key, dtype) in zip(indexes, entries):
            if key in kwargs:
                # Keyword arguments has priority
                self.payload[key] = dtype(kwargs[key])
            elif index < len(args):
                # Fallback to positional arguments
                self.payload[key] = dtype(args[index])
            else:
                # Fallback to 0
                self.payload[key] = dtype(0)

    def toBytes(self) -> bytes:
        result = bytes()
        for val in self.payload.values():
            result += val.bytes
        return result
