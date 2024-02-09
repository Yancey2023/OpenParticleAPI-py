import struct
from typing import BinaryIO


class Vec3:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def write_to_file(self, fp: BinaryIO) -> None:
        fp.write(struct.pack('>f', self.x))
        fp.write(struct.pack('>f', self.y))
        fp.write(struct.pack('>f', self.z))
