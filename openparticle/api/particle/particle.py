from __future__ import annotations

import string
from abc import ABCMeta, abstractmethod
from typing import Callable

from openparticle.api.math import matrix_util
from openparticle.api.output.Identifier import Identifier
from openparticle.api.math.vec3 import Vec3
from openparticle.api.output.data_color import DataColor, DataColorStatic, DataColorFree
from openparticle.api.output.data_particle import DataParticle, DataParticleSingle, DataParticleCompound, \
    DataParticleManager, DataParticleTransform
from openparticle.api.output.data_matrix import DataMatrix, DataMatrixStatic, DataMatrixFree


class Particle:
    __metaclass__ = ABCMeta

    def __init__(self, tick_add: int, age: int):
        self.__is_use_cache = False
        self.cache = None
        self.tick_add = tick_add
        self.age = age

    @abstractmethod
    def run(self) -> DataParticle:
        pass

    def run_with_cache(self) -> DataParticle:
        if self.__is_use_cache and self.cache is not None:
            return self.cache
        dataParticle = self.run()
        if self.__is_use_cache:
            self.cache = dataParticle
        return dataParticle

    def use_cache(self, is_use_cache: bool) -> Particle:
        self.__is_use_cache = is_use_cache
        return self

    def output(self, path: string) -> None:
        DataParticleManager(self.run()).write_to_file(path)

    @classmethod
    def create(cls, identifier: Identifier, age: int) -> Particle:
        return ParticleDefault(identifier, age).use_cache(True)

    def repeat(self, times: int) -> Particle:
        children = list()
        for i in range(times):
            children.append(self)
        return ParticleCompound(children).use_cache(self.__is_use_cache)

    @classmethod
    def compound(cls, children: list[Particle]) -> Particle:
        if len(children) == 0:
            raise RuntimeError("No children")
        is_use_cache = True
        for child in children:
            if not child.__is_use_cache:
                is_use_cache = False
                break
        return ParticleCompound(children).use_cache(is_use_cache)

    def shape(self, function: Callable[[Particle], list[Particle]]) -> Particle:
        return Particle.compound(function(self))

    def tick(self, tick: int) -> Particle:
        return ParticleTransform(self, None, None, tick).use_cache(self.__is_use_cache)

    def transform(self, data_matrix: DataMatrix) -> Particle:
        return ParticleTransform(self, data_matrix, None, 0).use_cache(self.__is_use_cache)

    def color(self, data_color: DataColor) -> Particle:
        return ParticleTransform(self, None, data_color, 0).use_cache(self.__is_use_cache)

    def offset_static(self, offset: Vec3) -> Particle:
        return self.transform(DataMatrixStatic(matrix_util.offset(offset)))

    def offset_free(self, offsets: list[Vec3]) -> Particle:
        return self.transform(DataMatrixFree(list(map(lambda offset: matrix_util.offset(offset), offsets))))

    def rotate_static(self, rotate: Vec3) -> Particle:
        return self.transform(DataMatrixStatic(matrix_util.rotateXYZ(rotate)))

    def rotate_free(self, rotates: list[Vec3]) -> Particle:
        return self.transform(DataMatrixFree(list(map(lambda rotate: matrix_util.rotateXYZ(rotate), rotates))))

    def color_static(self, color: int) -> Particle:
        return self.color(DataColorStatic(color))

    def color_free(self, colors: list[int]) -> Particle:
        return self.color(DataColorFree(colors))

    def apply(self, function: Callable[[Particle], Particle]) -> Particle:
        return ParticleFunction(self, function)


class ParticleDefault(Particle):

    def __init__(self, identifier: Identifier, age: int):
        super().__init__(0, age)
        self.__identifier = identifier

    def run(self) -> DataParticle:
        return DataParticleSingle(self.__identifier, self.age)


class ParticleCompound(Particle):

    def __init__(self, children: list[Particle]):
        tick_add = min(map(lambda child: child.tick_add, children))
        age = max(map(lambda child: child.tick_add + child.age, children)) - tick_add
        super().__init__(tick_add, age)
        self.__children = children

    def run(self) -> DataParticle:
        return DataParticleCompound(list(map(lambda particle: particle.run_with_cache(), self.__children)))


class ParticleTransform(Particle):

    def __init__(self, particle: Particle, data_matrix: None | DataMatrix, data_color: None | DataColor, tick_add: int):
        super().__init__(particle.tick_add + tick_add, particle.age)
        self.__particle = particle
        self.__data_matrix = data_matrix
        self.__data_color = data_color
        self.__tick_add = tick_add

    def run(self) -> DataParticle:
        return DataParticleTransform(
            self.__particle.run_with_cache(),
            self.__data_matrix,
            self.__data_color,
            self.__tick_add
        )


class ParticleFunction(Particle):

    def __init__(self, particle: Particle, function: Callable[[Particle], Particle]):
        super().__init__(particle.tick_add, particle.age)
        self.__particle = particle
        self.__function = function

    def run(self) -> DataParticle:
        new_particle = self.__function(self.__particle)
        if new_particle.age != self.__particle.age:
            raise RuntimeError('Particle age mismatch')
        return new_particle.run_with_cache()
