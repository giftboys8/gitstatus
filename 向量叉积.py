import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


class Plane:
    def __init__(self, position=np.array([0.0, 0.0, 0.0])):
        self.position = position
        self.torque = np.array([0.0, 0.0, 0.0])
        self.plane_points = np.array([[-4.0, 2.0, 0.0],[4.0, 2.0, 0.0],[4.0, -2.0, 0.0],[-4.0, -2.0, 0.0]])

    def apply_force(self, force, distance):
        torque = np.cross(distance, force)
        self.torque += torque


# 创建一个飞机实例
plane = Plane()

# 应用一个力和力的作用点相对于飞机中心的距离
force = np.array([1.0, 0.0, 0.0])
distance = np.array([0.0, 1.0, 0.0])
plane.apply_force(force, distance)
print("plane.torque",plane.torque)

# 创建一个3D绘图
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制飞机的位置（使用小球表示）
ax.scatter(plane.position[0], plane.position[1], plane.position[2], color='b')
for a in plane.plane_points:
    ax.scatter(a[0], a[1], a[2], color='red')


# 绘制力的作用点（使用绿色小球表示）
force_point = plane.position + distance
ax.scatter(force_point[0], force_point[1], force_point[2], color='g')

# 绘制力矩的方向（使用红色箭头表示）
ax.quiver(force_point[0], force_point[1], force_point[2],
          plane.torque[0], plane.torque[1], plane.torque[2], color='r')


# 添加一个表示力矩大小的标签
torque_magnitude = np.linalg.norm(plane.torque)
ax.text(force_point[0], force_point[1], force_point[2],
        f'Torque: {torque_magnitude}', color='r')

# 设置图形的范围
ax.set_xlim([-10, 10])
ax.set_ylim([-10, 10])
ax.set_zlim([-10, 10])

# 显示图形
plt.show()

