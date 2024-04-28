import math
import random
from typing import Callable

from openparticle.api.math.vec3 import Vec3
from openparticle.api.particle.particle import Particle


def butterfly(age: int) -> Callable[[Particle], list[Particle]]:
    def inner(particle: Particle) -> list[Particle]:
        particle_list: list[Particle] = list()
        for i in range(314):
            theta = i * 2 / 100
            r = 2 * math.fabs(math.sin(2 * theta)) + math.fabs(math.sin(4 * theta))
            x = r * math.sin(theta)
            y = r * math.cos(theta)
            # 通过位置模块可以偏移粒子的位置 .offset()
            particle_list.append(particle.offset_free(
                list(map(lambda tick: Vec3(x, math.fabs(y) * math.sin(0.5 * tick), y), range(age)))))
        return particle_list

    return inner


def line(x1, y1, z1, x2, y2, z2, count) -> Callable[[Particle], list[Particle]]:
    def inner(particle: Particle) -> list[Particle]:
        x_add = (x2 - x1) / (count - 1)
        y_add = (y2 - y1) / (count - 1)
        z_add = (z2 - z1) / (count - 1)
        particle_list: list[Particle] = list()
        for i in range(count):
            particle_list.append(particle.offset_static(Vec3(x1 + x_add * i, y1 + y_add * i, z1 + z_add * i)))
        return particle_list

    return inner


def random_position(range: float) -> Callable[[Particle], Particle]:
    def inner(particle: Particle) -> Particle:
        return particle.offset_static(Vec3(
            (random.random() - 0.5) * range,
            (random.random() - 0.5) * range,
            (random.random() - 0.5) * range
        ))

    return inner


def speed(speed: Vec3, age: int) -> list[Vec3]:
    position_list: list[Vec3] = list()
    for i in range(age):
        position_list.append(Vec3(speed.x * i, speed.y * i, speed.z * i))
    return position_list

# def random_move():
#     def inner(particle: Particle) -> Particle:
#         return particle.offset(DataVec3Free()).rotate(DataVec3Free())
#
#     return inner
