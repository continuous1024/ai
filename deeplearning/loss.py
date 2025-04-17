# 1. 什么是损失函数（What）
# 损失函数（Loss Function）是深度学习中用于衡量模型预测结果与真实标签之间差异的数学函数。
# 它是模型优化的目标，通过反向传播调整参数，使损失最小化。

# 2. 为什么需要损失函数（Why）
# 核心作用：量化模型误差，指导模型优化方向。

# 关键意义：不同的任务需要不同的损失函数（如分类 vs. 回归）。

# 实际价值：选择合适的损失函数直接影响模型性能和收敛速度。


import numpy as np


# 均方误差损失函数
def mean_squared_error(y_true, y_pred):
    return 0.5 * np.sum(np.power(y_true - y_pred, 2))


y = [0.1, 0.05, 0.6, 0.0, 0.05, 0.1, 0.0, 0.1, 0.0, 0.0]
t = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]  # one-hot
print(mean_squared_error(np.array(y), np.array(t)))
y = [0.1, 0.05, 0.1, 0.0, 0.05, 0.1, 0.0, 0.6, 0.0, 0.0]
print(mean_squared_error(np.array(y), np.array(t)))


# 交叉熵损失函数
def cross_entropy_error(y_pred, y_true):
    delta = 1e-7  # 避免 np.log(0) 出现负无限大 -inf
    return -np.sum(y_true * np.log(y_pred + delta))


y = [0.1, 0.05, 0.6, 0.0, 0.05, 0.1, 0.0, 0.1, 0.0, 0.0]
t = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]  # one-hot
print(cross_entropy_error(np.array(y), np.array(t)))
y = [0.1, 0.05, 0.1, 0.0, 0.05, 0.1, 0.0, 0.6, 0.0, 0.0]
print(cross_entropy_error(np.array(y), np.array(t)))


# minibatch
def cross_entropy_error_minibatch(y_pred, y_true):
    if y_pred.ndim == 1:
        y_pred = y_pred.reshape(1, y_pred.size)
        y_true = y_true.reshape(1, y_true.size)

    batch_size = y_pred.shape[0]
    delta = 1e-7
    return -np.sum(y_true * np.log(y_pred + delta)) / batch_size


def cross_entropy_error(y_pred, y_true):
    if y_pred.ndim == 1:
        y_pred = y_pred.reshape(1, y_pred.size)
        y_true = y_true.reshape(1, y_true.size)
    batch_size = y_pred.shape[0]
    # t为one-hot表示时通过t * np.log(y)计算的地方
    # 在t为标签形式时，可用np.log(y_pred[np.arange (batch_size), y_true] )实现相同的处理
    # （为了便于观察，这里省略了微小值1e-7）​。
    return -np.sum(np.log(y_pred[np.arange(batch_size), y_true])) / batch_size

# np.arange 会生成一个从0到batch_size-1的数组。
# 比如当batch_size为5时，np.arange(batch_size)会生成一个NumPy数组[0, 1, 2, 3, 4]​。
# 因为t中标签是以[2, 7, 0,9, 4]的形式存储的，
# 所以y[np.arange(batch_size), t]能抽出各个数据的正确解标签对应的神经网络的输出
# (在这个例子中，y[np.arange(batch_size), t]
# 会生成NumPy数组[y[0,2], y[1,7], y[2,0], y[3,9], y[4,4]​]​）​
