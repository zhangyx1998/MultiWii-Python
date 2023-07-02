# ===================================================================
# Executable binary type annotations
# ===================================================================
# Author: Yuxuan Zhang, yuxuan@yuxuanzhang.net
# Published under MIT License
# ===================================================================
ENDIAN = "little"


class TypedInteger(int):
    byte_size: int
    signed: bool

    @classmethod
    def toBytes(cls, value: int) -> bytes:
        return value.to_bytes(cls.byte_size, ENDIAN, signed=cls.signed)

    @classmethod
    def fromBytes(cls, value: bytes | list[int]) -> int:
        if isinstance(value, list):
            value = bytes(value)
        return cls.from_bytes(value, ENDIAN, signed=cls.signed)

    @classmethod
    def ARRAY(cls, count:int, start: int = 0, prefix: str = None):
        r = range(start, start + count)
        if prefix is None:
            return dict([(n, cls) for n in r])
        else:
            return dict([(f"{prefix}{n}", cls) for n in r])

    def __new__(cls, value: int | bytes):
        if isinstance(value, int) or isinstance(value, float):
            return super().__new__(cls, value)
        elif isinstance(value, bytes):
            return super().__new__(cls, cls.fromBytes(value))
        else:
            raise TypeError

    def __init__(self, value: int):
        self.value = value
        self.bytes = self.toBytes(value)


class U8(TypedInteger):
    byte_size = 1
    signed = False


class U16(TypedInteger):
    byte_size = 2
    signed = False


class U32(TypedInteger):
    byte_size = 4
    signed = False


class U64(TypedInteger):
    byte_size = 8
    signed = False


class I8(TypedInteger):
    byte_size = 1
    signed = True


class I16(TypedInteger):
    byte_size = 2
    signed = True


class I32(TypedInteger):
    byte_size = 4
    signed = True


class I64(TypedInteger):
    byte_size = 8
    signed = True
