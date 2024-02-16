import math
import string

from example import util
from openparticle.api.activity.activity import Activity
from openparticle.api.output.Identifier import Identifier
from openparticle.api.output.Vec3 import Vec3
from openparticle.api.particle.particle import Particle


class TestActivity(Activity):

    def get_path(self) -> string:
        # 文件路径
        return 'particles.par'

    def get_position(self) -> Vec3:
        # 偏移粒子实际要生成粒子的位置
        return Vec3(0, -58, 0)

    def create_particle(self) -> None:
        age = 80
        # 创建粒子 Particle.create()
        basic_particle = Particle.create(Identifier.create_minecraft("end_rod"), age)
        self.add_particle(
            basic_particle
            # 通过合并模块可以把多个模块合并起来 .compound()
            .compound(util.butterfly(age))
            # 通过旋转模块让蝴蝶倾斜45度（绕z轴旋转45度），这里的角度使用弧度制，45度角用0.25pi表示 .rotate()
            .rotate_static(Vec3(0, 0, math.pi / 4))
        )
        self.add_particle(
            basic_particle
            # 通过合并模块可以把多个模块合并起来 .compound()
            .compound(util.line(0, 0, 0, 10, 10, 10, 100))
            # 改变颜色 .color()
            .color_static(0xFF00FF)
            # 改变生成时间 .tick()
            .tick(10)
        )

# 更多功能

# 单个粒子: Particle.create(identifier, age)
# 合并粒子: Particle.compound(list[Particle]) 或者 .compound(Callable[[Particle], list[Particle]])
# 改变时间: .tick(int)
# 改变位置: .offset(DataVec3)
# 改变角度: .rotate(DataVec3)
# 改变颜色: .color(DataColor)

# DataVec3 位置偏移和旋转支持三种模式
# 1. DataVec3Static 偏移固定的位置
# 2. DataVec3Simple 初始位置，初速度，摩擦力，重力
# 3. DataVec3Free 为每一个tick设置位置

# DataColor 颜色支持三种模式
# 1. DataColorStatic 固定颜色
# 2. DataColorSimple 多个颜色之间渐变
# 3. DataColorFree 为每一个tick设置颜色
