import struct
from abc import ABCMeta, abstractmethod
from typing import BinaryIO

from openparticle.api.Vec3 import Vec3

STATIC = 0
SIMPLE = 1
FREE = 2


class DataVec3:
    __metaclass__ = ABCMeta

    @abstractmethod
    def write_to_file(self, fp: BinaryIO) -> None:
        pass


# 位置不变
class DataVec3Static(DataVec3):

    def __init__(self, vec3: Vec3):
        self.vec3 = vec3

    def write_to_file(self, fp: BinaryIO) -> None:
        fp.write(struct.pack('>B', STATIC))
        self.vec3.write_to_file(fp)


# 初始位置，初速度，摩擦力，重力
class DataVec3Simple(DataVec3):

    def __init__(self, vec3: Vec3, speed: Vec3, g: float, f: float):
        self.vec3 = vec3
        self.speed = speed
        self.g = g
        self.f = f

    def write_to_file(self, fp: BinaryIO) -> None:
        fp.write(struct.pack('>B', SIMPLE))
        self.vec3.write_to_file(fp)
        fp.write(struct.pack('>f', self.g))
        fp.write(struct.pack('>f', self.f))


# 为每一个tick设置位置
class DataVec3Free(DataVec3):

    def __init__(self, vec3List: list[Vec3]):
        self.vec3List = vec3List

    def write_to_file(self, fp: BinaryIO) -> None:
        fp.write(struct.pack('>B', FREE))
        fp.write(struct.pack('>I', len(self.vec3List)))
        for vec3 in self.vec3List:
            vec3.write_to_file(fp)
