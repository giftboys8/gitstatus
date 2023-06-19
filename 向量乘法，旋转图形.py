import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 定义旋转矩阵


def rotation_matrix(degrees):
    theta = np.radians(degrees)
    return np.array([
        [np.cos(theta), np.sin(theta), 0],
        [-np.sin(theta), np.cos(theta), 0],
        [0, 0, 1]
    ])


# 定义长方体的顶点
cuboid = np.array([
    [2, 1, 3],
    [2, 1, -3],
    [2, -1, 3],
    [2, -1, -3],
    [-2, 1, 3],
    [-2, 1, -3],
    [-2, -1, 3],
    [-2, -1, -3]
]).T  # 转置以使每一列代表一个顶点
print(cuboid)

# 连接长方体的顶点，形成长方体的面
faces = np.array([
    [0, 1, 3, 2],
    [4, 5, 7, 6],
    [0, 1, 5, 4],
    [2, 3, 7, 6],
    [0, 2, 6, 4],
    [1, 3, 7, 5]
])

# 绘制长方体
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(*cuboid, color='b')
for face in faces:
    # 绘制每个面
    # plot()的参数为x, y, z三个坐标轴的值
    # 由于我们的顶点坐标是以列的形式存储的，因此我们需要使用cuboid[:, face]来获取每个面的坐标
    ax.plot(cuboid[0, face], cuboid[1, face], cuboid[2, face], color='b')


# 应用旋转矩阵
rotated_cuboid = np.dot(rotation_matrix(90), cuboid)

# 绘制旋转后的长方体
ax.scatter(*rotated_cuboid, color='r')
for face in faces:
    ax.plot(rotated_cuboid[0, face], rotated_cuboid[1, face],
            rotated_cuboid[2, face], color='r')
# 标识坐标轴
ax.text(0, 0, 0, 'O')
ax.text(3, 0, 0, 'x')
ax.text(0, 3, 0, 'y')
ax.text(0, 0, 3, 'z')

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
    
# 显示图形
plt.show()

# 标识顶点
for i in range(8):
    ax.text(*cuboid[:, i], i)
    ax.text(*rotated_cuboid[:, i], i)



# 创建3D图形
ax = fig.add_subplot(111, projection='3d')

# 绘制原始的长方体
ax.scatter(*cuboid, color='b', label='Original cuboid')

# 绘制旋转后的长方体
ax.scatter(*rotated_cuboid, color='r', label='Rotated cuboid')

# 添加图例
ax.legend()

# 显示图形
plt.show()
