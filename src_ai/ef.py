import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import numpy as np


# 假设你的数据集存储在df中
df = pd.read_csv('your_dataset.csv')

# 设定独立变量和因变量
X = df[['提交频率', '代码规模', '缺陷数量']]
y = df['效率']

# 将数据分为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# 创建并训练多元线性回归模型
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# 在测试集上做预测
y_pred = regressor.predict(X_test)

# 输出回归模型的参数
print('Intercept: ', regressor.intercept_)
print('Coefficients: ', regressor.coef_)

# 输出模型的性能指标
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
