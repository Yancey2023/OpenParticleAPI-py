import struct
from abc import ABCMeta, abstractmethod
from typing import BinaryIO

from openparticle.api.data_color import DataColor
from openparticle.api.data_vec3 import DataVec3
from openparticle.api.Identifier import Identifier, IdentifierCache

identifierCache = IdentifierCache()

SINGLE = 0
COMPOUND = 1
TICK = 2
OFFSET = 3
ROTATE = 4
COLOR = 5


class DataParticle:
    __metaclass__ = ABCMeta
    data_particle_list = list()
    nextId = 0

    def __init__(self):
        self.id = DataParticle.nextId
        DataParticle.nextId += 1
        DataParticle.data_particle_list.append(self)

    @abstractmethod
    def write_to_file(self, fp: BinaryIO) -> None:
        pass


# 单个粒子
class DataParticleSingle(DataParticle):

    def __init__(self, identifier: Identifier, age: int):
        super().__init__()
        self.identifier = identifier
        self.age = age

    def write_to_file(self, fp: BinaryIO) -> None:
        fp.write(struct.pack('>B', SINGLE))
        fp.write(struct.pack('>I', self.id))
        fp.write(struct.pack('>I', identifierCache.getId(self.identifier)))
        fp.write(struct.pack('>I', self.age))


# 单个粒子
class DataParticleCompound(DataParticle):

    def __init__(self, flag: bool, dataParticles: list[DataParticle]):
        super().__init__()
        self.flag = flag
        self.dataParticles = dataParticles

    def write_to_file(self, fp: BinaryIO) -> None:
        fp.write(struct.pack('>B', COMPOUND))
        fp.write(struct.pack('>I', self.id))
        fp.write(struct.pack('?', self.flag))
        fp.write(struct.pack('>I', len(self.dataParticles)))
        for dataParticle in self.dataParticles:
            fp.write(struct.pack('>I', dataParticle.id))


# 改变粒子的出现时间
class DataParticleTick(DataParticle):

    def __init__(self, dataParticle: DataParticle, tick_start: int):
        super().__init__()
        self.dataParticle = dataParticle
        self.tick_start = tick_start

    def write_to_file(self, fp: BinaryIO) -> None:
        fp.write(struct.pack('>B', TICK))
        fp.write(struct.pack('>I', self.id))
        fp.write(struct.pack('>I', self.dataParticle.id))
        fp.write(struct.pack('>I', self.tick_start))


# 改变粒子的位置
class DataParticleOffset(DataParticle):

    def __init__(self, dataParticle: DataParticle, offset: DataVec3):
        super().__init__()
        self.dataParticle = dataParticle
        self.offset = offset

    def write_to_file(self, fp: BinaryIO) -> None:
        fp.write(struct.pack('>B', OFFSET))
        fp.write(struct.pack('>I', self.id))
        fp.write(struct.pack('>I', self.dataParticle.id))
        self.offset.write_to_file(fp)


# 改变粒子的位置
class DataParticleRotate(DataParticle):

    def __init__(self, dataParticle: DataParticle, rotate: DataVec3):
        super().__init__()
        self.dataParticle = dataParticle
        self.rotate = rotate

    def write_to_file(self, fp: BinaryIO) -> None:
        fp.write(struct.pack('>B', ROTATE))
        fp.write(struct.pack('>I', self.id))
        fp.write(struct.pack('>I', self.dataParticle.id))
        self.rotate.write_to_file(fp)


# 改变粒子的颜色
class DataParticleColor(DataParticle):

    def __init__(self, dataParticle: DataParticle, color: DataColor):
        super().__init__()
        self.dataParticle = dataParticle
        self.color = color

    def write_to_file(self, fp: BinaryIO) -> None:
        fp.write(struct.pack('>B', COLOR))
        fp.write(struct.pack('>I', self.id))
        fp.write(struct.pack('>I', self.dataParticle.id))
        self.color.write_to_file(fp)


class DataParticleManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataParticleManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.parents: list[DataParticle] = list()

    def add(self, dataParticle: DataParticle) -> None:
        if dataParticle not in self.parents:
            self.parents.append(dataParticle)

    def write_to_file(self, fp: BinaryIO) -> None:
        fp.write(struct.pack('>I', len(DataParticle.data_particle_list)))
        for dataParticle in DataParticle.data_particle_list:
            dataParticle.write_to_file(fp)
        fp.write(struct.pack('>I', len(self.parents)))
        for parent in self.parents:
            fp.write(struct.pack('>I', parent.id))
