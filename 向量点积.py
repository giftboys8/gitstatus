import numpy as np
from Scaled import Quiver
from math import sqrt

# 向量的点积

def is_off_course(position, destination, direction):
    # 计算目标方向向量
    target_direction = destination - position

    print("target_direction:",target_direction)
    # 计算目标方向向量与航行方向向量的点积
    dot_product = np.dot(target_direction, direction)
    print("dot_product:",dot_product)

    # 计算目标方向向量与航行方向向量的长度
    target_magnitude = np.linalg.norm(target_direction)
    direction_magnitude = np.linalg.norm(direction)
    print("target_magnitude:",target_magnitude)
    print("direction_magnitude:",direction_magnitude)

    # 计算目标方向向量与航行方向向量之间的角度
    cos_angle = dot_product / (target_magnitude * direction_magnitude)
    angle = np.arccos(cos_angle)
    print("cos_angle:",cos_angle)
    print("angle:",angle)


    # 如果角度大于某个阈值（例如，5度），则判断船只偏离了航线
    threshold = np.radians(5)
    if angle < threshold:
        return True
    else:
        return False



# 假设船只的位置是[0, 0]，目标位置是[10, 10]，航行方向是[5, 5]
position = np.array([0, 0])
destination = np.array([10, 10])
direction = np.array([5, 5])

print(is_off_course(position, destination, direction))

q = Quiver(np.stack((position, destination, direction, np.array([-10, 10]), np.array([10, 20]))))
print(q.v[0])
a=q.plt_quiver()
a.show()
