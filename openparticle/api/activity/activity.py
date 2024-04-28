import os.path
import string
import time
from abc import ABCMeta, abstractmethod

from openparticle.api.output.Identifier import Identifier
from openparticle.api.math.vec3 import Vec3
from openparticle.api.output.data_particle import DataParticleManager
from openparticle.api.particle.particle import Particle


class Activity:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.particle_list: list[Particle] = list()

    @abstractmethod
    def get_path(self) -> string:
        pass

    @abstractmethod
    def get_position(self) -> Vec3:
        pass

    @abstractmethod
    def create_particle(self) -> None:
        pass

    def add_particle(self, particle: Particle) -> None:
        self.particle_list.append(particle)

    def run(self) -> None:
        print(f'-----{self.__class__.__name__}-----')
        # 获取粒子数据
        time_start = time.time()
        self.create_particle()
        if len(self.particle_list) == 0:
            print('粒子为空，你是不是忘记调用addParticle()')
            return
        particle = Particle.compound(self.particle_list).offset_static(self.get_position())
        # 计算粒子数据
        data_particle = particle.run()
        manager = DataParticleManager(data_particle)
        # 写入粒子数据
        path = self.get_path()
        manager.output(path)
        time_end = time.time()
        print('运行耗时: {:.4f}s'.format(time_end - time_start))
        print(f'粒子数量: {data_particle.get_particle_count()}')
        size = os.path.getsize(path)
        if size < 1024:
            size_str = '{:.0f}B'.format(size)
        elif size < 1024 * 1024:
            size_str = '{:.0f}KB'.format(size / 1024)
        elif size < 1024 * 1024 * 1024:
            size_str = '{:.0f}MB'.format(size / 1024 / 1024)
        else:
            size_str = '{:.0f}GB'.format(size / 1024 / 1024 / 1024)
        print(f'文件大小: {size_str}')


class ActivityManager:

    def __init__(self):
        self.activity_list: list[Activity] = list()

    def add(self, activity: Activity):
        self.activity_list.append(activity)

    def run(self):
        for activity in self.activity_list:
            activity.run()
