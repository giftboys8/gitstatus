from sklearn.decomposition import PCA
from sklearn.datasets import fetch_lfw_people
import matplotlib.pyplot as plt

# 加载数据集
lfw_people = fetch_lfw_people(min_faces_per_person=70, resize=0.4)
n_samples, h, w = lfw_people.images.shape
X = lfw_people.data
n_features = X.shape[1]

# 显示原始图像
plt.figure(figsize=(1.8 * 4, 2.4 * 3))
plt.subplots_adjust(bottom=0, left=.01, right=.99, top=.90, hspace=.35)
for i in range(12):
    plt.subplot(3, 4, i + 1)
    plt.imshow(X[i].reshape((h, w)), cmap=plt.cm.gray)
    plt.title(f'Person {i+1}', size=12)
    plt.xticks(())
    plt.yticks(())
plt.show()

# 进行PCA
n_components = 150  # 降维后的维度
pca = PCA(n_components=n_components,
          svd_solver='randomized', whiten=True).fit(X)

# 将原始数据投影到主成分上
X_pca = pca.transform(X)

# 显示原始图像和主成分
plt.figure(figsize=(1.8 * 4, 2.4 * 3))
plt.subplots_adjust(bottom=0, left=.01, right=.99, top=.90, hspace=.35)
for i in range(12):
    plt.subplot(3, 4, i + 1)
    plt.imshow(pca.components_[i].reshape((h, w)), cmap=plt.cm.gray)
    plt.title(f'Principal Component {i+1}', size=12)
    plt.xticks(())
    plt.yticks(())
plt.show()
