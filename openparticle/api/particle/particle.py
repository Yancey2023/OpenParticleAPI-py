from __future__ import annotations

import string
from abc import ABCMeta, abstractmethod
from typing import Callable

from openparticle.api.output.Identifier import Identifier
from openparticle.api.output.Vec3 import Vec3
from openparticle.api.output.data_color import DataColor, DataColorStatic
from openparticle.api.output.data_particle import DataParticle, DataParticleSingle, DataParticleCompound, \
    DataParticleTick, DataParticleOffset, DataParticleRotate, DataParticleColor, DataParticleManager
from openparticle.api.output.data_vec3 import DataVec3, DataVec3Static


class Particle:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.is_use_cache = False
        self.cache = None

    @abstractmethod
    def run(self) -> DataParticle:
        pass

    def run_with_cache(self) -> DataParticle:
        if self.is_use_cache and self.cache is not None:
            return self.cache
        dataParticle = self.run()
        if self.is_use_cache:
            self.cache = dataParticle
        return dataParticle

    def use_cache(self, is_use_cache: bool) -> Particle:
        self.is_use_cache = is_use_cache
        return self

    def output(self, path: string) -> None:
        manager = DataParticleManager()
        manager.add(self.run())
        manager.write_to_file(path)

    @classmethod
    def create(cls, identifier: Identifier, age: int) -> Particle:
        return ParticleDefault(identifier, age).use_cache(True)

    def repeat(self, times: int) -> Particle:
        children = list()
        for i in range(times):
            children.append(self)
        return ParticleCompound(children).use_cache(self.is_use_cache)

    @classmethod
    def compound_all(cls, children: list[Particle]) -> Particle:
        is_use_cache = True
        for particle in children:
            if particle.is_use_cache:
                is_use_cache = False
                break
        return ParticleCompound(children).use_cache(is_use_cache)

    def compound(self, function: Callable[[Particle], list[Particle]]) -> Particle:
        return Particle.compound_all(function(self))

    def tick(self, tick: int) -> Particle:
        return ParticleTick(self, tick)

    def offset(self, offset: DataVec3) -> Particle:
        return ParticleOffset(self, offset)

    def offset_static(self, offset: Vec3) -> Particle:
        return ParticleOffset(self, DataVec3Static(offset))

    def rotate(self, rotate: DataVec3) -> Particle:
        return ParticleRotate(self, rotate)

    def rotate_static(self, rotate: Vec3) -> Particle:
        return ParticleOffset(self, DataVec3Static(rotate))

    def color(self, color: DataColor) -> Particle:
        return ParticleColor(self, color)

    def color_static(self, color: int) -> Particle:
        return ParticleColor(self, DataColorStatic(color))


class ParticleDefault(Particle):

    def __init__(self, identifier: Identifier, age: int):
        super().__init__()
        self.identifier = identifier
        self.age = age

    def run(self) -> DataParticle:
        return DataParticleSingle(self.identifier, self.age)


class ParticleCompound(Particle):

    def __init__(self, children: list[Particle]):
        super().__init__()
        self.children = children

    def run(self) -> DataParticle:
        return DataParticleCompound(False, list(map(lambda particle: particle.run_with_cache(), self.children)))


class ParticleTick(Particle):

    def __init__(self, particle: Particle, tick: int):
        super().__init__()
        self.particle = particle
        self.tick = tick

    def run(self) -> DataParticle:
        return DataParticleTick(self.particle.run_with_cache(), self.tick)


class ParticleOffset(Particle):

    def __init__(self, particle: Particle, offset: DataVec3):
        super().__init__()
        self.particle = particle
        self.offset = offset

    def run(self) -> DataParticle:
        return DataParticleOffset(self.particle.run_with_cache(), self.offset)


class ParticleRotate(Particle):

    def __init__(self, particle: Particle, rotate: DataVec3):
        super().__init__()
        self.particle = particle
        self.offset = rotate

    def run(self) -> DataParticle:
        return DataParticleRotate(self.particle.run_with_cache(), self.offset)


class ParticleColor(Particle):

    def __init__(self, particle: Particle, color: DataColor):
        super().__init__()
        self.particle = particle
        self.color = color

    def run(self) -> DataParticle:
        return DataParticleColor(self.particle.run_with_cache(), self.color)


class ParticleFunction(Particle):

    def __init__(self, particle: Particle, function: Callable[[Particle], Particle]):
        super().__init__()
        self.particle = particle
        self.function = function

    def run(self) -> DataParticle:
        return self.function(self).run_with_cache()
