import math
import string

from example import util
from openparticle.api.activity.activity import Activity
from openparticle.api.output.Identifier import Identifier
from openparticle.api.math.vec3 import Vec3
from openparticle.api.particle.particle import Particle


class TestActivity(Activity):

    def get_path(self) -> string:
        # 文件路径
        return 'particles.par'

    def get_position(self) -> Vec3:
        # 可以将粒子偏移到实际要生成粒子的位置
        return Vec3(0, -56, 0)

    def create_particle(self) -> None:
        age = 80
        # 创建粒子 Particle.create()
        basic_particle = Particle.create(Identifier.create_minecraft("end_rod"), age)
        self.add_particle(
            basic_particle
            # 用多个当前粒子组成一个新粒子 .shape()
            .shape(util.butterfly(age))
            # 让蝴蝶倾斜45度（绕z轴旋转45度），这里的角度使用弧度制，45度角用0.25pi表示 .rotate()
            .rotate_static(Vec3(0, 0, math.pi / 4))
            # 用多个当前粒子组成一个新粒子 .shape()
            .shape(util.line(-50, 0, 0, 50, 0, 0, 10))
            # 改变颜色 .color()
            .color_static(0xFF00FF)
        )
        # self.add_particle(
        #     basic_particle
        #     # 用多个当前粒子组成一个新粒子 .shape()
        #     .shape(util.line(0, 0, 0, 10, 10, 10, 100))
        #     # 改变颜色 .color()
        #     .color_static(0xFF00FF)
        #     # 改变生成时间 .tick()
        #     .tick(10)
        # )

# 更多功能

# 单个粒子: Particle.create(identifier, age)
# 合并粒子: Particle.compound(list[Particle]) 或者 .shape(Callable[[Particle], list[Particle]])
# 改变时间: .tick(int)
# 改变位置: .offset_static(DataVec3) 和 .offset_free(list[DataVec3])
# 改变角度: .rotate_static(DataVec3) 和 .rotate_free(list[DataVec3])
# 改变颜色: .color_static(DataColor) 和 .color_free(DataColor)

# DataVec3 位置偏移和旋转支持两种模式
# 1. DataVec3Static 偏移固定的位置
# 2. DataVec3Free 为每一个tick设置位置

# DataColor 颜色支持两种模式
# 1. DataColorStatic 固定颜色
# 2. DataColorFree 为每一个tick设置颜色
