import math
import string

from example import util
from openparticle.api.activity.activity import Activity
from openparticle.api.output.Identifier import Identifier
from openparticle.api.math.vec3 import Vec3
from openparticle.api.particle.particle import Particle


class TestActivity2(Activity):

    def get_path(self) -> string:
        # 文件路径
        return 'particles.par'

    def get_position(self) -> Vec3:
        # 偏移粒子实际要生成粒子的位置
        return Vec3(0, -30, 0)

    def create_particle(self) -> None:
        age = 80
        # 创建粒子 Particle.create()
        basic_particle = Particle.create(Identifier.create_minecraft("end_rod"), age)
        self.add_particle(basic_particle
                          # 用多个当前粒子组成一个新粒子 .shape()
                          .shape(util.butterfly(age))
                          # 让蝴蝶倾斜45度（绕z轴旋转45度），这里的角度使用弧度制，45度角用0.25pi表示 .rotate()
                          .rotate_static(Vec3(0, 0, math.pi / 4))
                          # 向前运动
                          .offset_free(util.speed(Vec3(0.6, 0, 0), age))
                          # 随机位置，范围从(-50, -50, -50)到(50, 50, 50)
                          .apply(util.random_position(50))
                          # 重复1000次
                          .repeat(1000)
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
