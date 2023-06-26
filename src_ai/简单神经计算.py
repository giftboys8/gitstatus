import numpy as np

# 假设我们的输入数据是一个2维向量，有两个特征
input_data = np.array([2, 3])

# 初始化我们的权重矩阵，假设隐藏层有3个神经元，那么权重矩阵的形状是(2, 3)
weights = np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])
print(
    f"input_data.shape: {input_data.shape}, weights.shape: {weights.shape}",
    "weights:", weights
)

# 然后，我们用输入数据和权重矩阵进行矩阵乘法，得到隐藏层的输出
hidden_layer_output = np.dot(input_data, weights)

print(hidden_layer_output)
