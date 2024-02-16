import string
import struct
from abc import ABCMeta, abstractmethod
from typing import BinaryIO

from openparticle.api.output.data_color import DataColor
from openparticle.api.output.data_vec3 import DataVec3
from openparticle.api.output.Identifier import Identifier

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

    @abstractmethod
    def get_count(self) -> int:
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
        fp.write(struct.pack('>I', self.identifier.id))
        fp.write(struct.pack('>I', self.age))

    def get_count(self) -> int:
        return 1


# 合并多个粒子
class DataParticleCompound(DataParticle):

    def __init__(self, flag: bool, data_particles: list[DataParticle]):
        super().__init__()
        self.flag = flag
        self.data_particles = data_particles

    def write_to_file(self, fp: BinaryIO) -> None:
        fp.write(struct.pack('>B', COMPOUND))
        fp.write(struct.pack('>I', self.id))
        fp.write(struct.pack('?', self.flag))
        fp.write(struct.pack('>I', len(self.data_particles)))
        for dataParticle in self.data_particles:
            fp.write(struct.pack('>I', dataParticle.id))

    def get_count(self) -> int:
        sum = 0
        for data_particle in self.data_particles:
            sum += data_particle.get_count()
        return sum


# 改变粒子的出现时间
class DataParticleTick(DataParticle):

    def __init__(self, data_particle: DataParticle, tick_start: int):
        super().__init__()
        self.data_particle = data_particle
        self.tick_start = tick_start

    def write_to_file(self, fp: BinaryIO) -> None:
        fp.write(struct.pack('>B', TICK))
        fp.write(struct.pack('>I', self.id))
        fp.write(struct.pack('>I', self.data_particle.id))
        fp.write(struct.pack('>I', self.tick_start))

    def get_count(self) -> int:
        return self.data_particle.get_count()


# 改变粒子的位置
class DataParticleOffset(DataParticle):

    def __init__(self, data_particle: DataParticle, offset: DataVec3):
        super().__init__()
        self.data_particle = data_particle
        self.offset = offset

    def write_to_file(self, fp: BinaryIO) -> None:
        fp.write(struct.pack('>B', OFFSET))
        fp.write(struct.pack('>I', self.id))
        fp.write(struct.pack('>I', self.data_particle.id))
        self.offset.write_to_file(fp)

    def get_count(self) -> int:
        return self.data_particle.get_count()


# 改变粒子的位置
class DataParticleRotate(DataParticle):

    def __init__(self, data_particle: DataParticle, rotate: DataVec3):
        super().__init__()
        self.data_particle = data_particle
        self.rotate = rotate

    def write_to_file(self, fp: BinaryIO) -> None:
        fp.write(struct.pack('>B', ROTATE))
        fp.write(struct.pack('>I', self.id))
        fp.write(struct.pack('>I', self.data_particle.id))
        self.rotate.write_to_file(fp)

    def get_count(self) -> int:
        return self.data_particle.get_count()


# 改变粒子的颜色
class DataParticleColor(DataParticle):

    def __init__(self, data_particle: DataParticle, color: DataColor):
        super().__init__()
        self.data_particle = data_particle
        self.color = color

    def write_to_file(self, fp: BinaryIO) -> None:
        fp.write(struct.pack('>B', COLOR))
        fp.write(struct.pack('>I', self.id))
        fp.write(struct.pack('>I', self.data_particle.id))
        self.color.write_to_file(fp)

    def get_count(self) -> int:
        return self.data_particle.get_count()


class DataParticleManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataParticleManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.parents: list[DataParticle] = list()

    def add(self, dataParticle: DataParticle):
        self.parents.append(dataParticle)

    def write_to_file(self, fp: BinaryIO) -> None:
        fp.write(struct.pack('>I', len(Identifier.identifier_list)))
        for identifier in Identifier.identifier_list:
            identifier.write_to_file(fp)
        fp.write(struct.pack('>I', len(DataParticle.data_particle_list)))
        for data_particle in DataParticle.data_particle_list:
            data_particle.write_to_file(fp)
        fp.write(struct.pack('>I', len(self.parents)))
        for parent in self.parents:
            fp.write(struct.pack('>I', parent.id))

    def output(self, path: string) -> None:
        with open(path, 'wb') as fp:
            self.write_to_file(fp)
