import math

from openparticle.api.data_particle import *
from openparticle.api.data_vec3 import *
from openparticle.api.Identifier import *
from openparticle.api.Vec3 import Vec3

# 创建粒子类型
identifierCache = IdentifierCache()
end_rod = Identifier.create_minecraft("end_rod")
# 或者 end_rod = Identifier.create("minecraft", "end_rod")
identifierCache.add(end_rod)

# 通过粒子类型创建持续时长为80粒子 DataParticleSingle
age = 80
base_particle = DataParticleSingle(end_rod, age)

# 通过位置模块可以偏移粒子的位置 DataParticleOffset
particle_list: list[DataParticleOffset] = list()
for i in range(314):
    theta = i * 2 / 100
    r = 2 * math.fabs(math.sin(2 * theta)) + math.fabs(math.sin(4 * theta))
    x = r * math.sin(theta)
    y = r * math.cos(theta)
    # position_list存储单个粒子不同的tick的位置
    position_list: list[Vec3] = list()
    for j in range(age):
        position_list.append(Vec3(x, math.fabs(y) * math.sin(0.5 * j), y))
    particle_list.append(DataParticleOffset(base_particle, DataVec3Free(position_list)))

# 通过合并模块可以把多个模块合并起来 DataParticleCompound
butterfly = DataParticleCompound(True, particle_list)

# 通过旋转模块让蝴蝶倾斜45度（绕z轴旋转45度），这里的角度使用弧度制，45度角用0.25pi表示 DataParticleRotate
butterfly_rotate = DataParticleRotate(butterfly, DataVec3Static(Vec3(0, 0, math.pi / 4)))

# 最后通过位置模块可以偏移粒子实际要生成粒子的位置
particle = DataParticleOffset(base_particle, DataVec3Static(Vec3(0, -58, 0)))

# 添加粒子
dataParticleManager = DataParticleManager()
dataParticleManager.add(particle)

# 文件写入
with open('particles.par', 'wb') as fp:
    identifierCache.write_to_file(fp)
    dataParticleManager.write_to_file(fp)

print('导出成功')

# 更多功能

# 单个粒子: DataParticleSingle
# 合并粒子: DataParticleCompound
# 改变时间: DataParticleTick
# 改变位置: DataParticleOffset
# 改变角度: DataParticleRotate
# 改变颜色: DataParticleColor

# 位置偏移和旋转支持三种模式
# 1. DataVec3Static 偏移固定的位置
# 2. DataVec3Simple 初始位置，初速度，摩擦力，重力
# 3. DataVec3Free 为每一个tick设置位置

# 颜色支持三种模式
# 1. DataColorStatic 固定颜色
# 2. DataColorSimple 多个颜色之间渐变
# 3. DataColorFree 为每一个tick设置颜色
