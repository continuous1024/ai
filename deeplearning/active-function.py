import numpy as np
import matplotlib.pyplot as plt


# 阶跃函数
def step_function(x):
    # y = x > 0
    # return y.astype(np.int32)
    return np.array(x > 0, dtype=np.int32)


x = np.arange(-5.0, 5.0, 0.1)
y = step_function(x)
plt.plot(x, y)
plt.ylim(-0.1, 1.1)
plt.show()


# Sigmoid 函数
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


x = np.arange(-5.0, 5.0, 0.1)
y = sigmoid(x)
plt.plot(x, y)
plt.ylim(-0.1, 1.1)  # 指定y轴的范围
plt.show()


# ReLU 函数
def relu(x):
    return np.maximum(0, x)


x = np.arange(-5.0, 5.0, 0.1)
y = relu(x)
plt.plot(x, y)
plt.show()


# 输出层激活函数
# 恒等函数
def identity_function(x):
    return x


# softmax 函数
def softmax(a):
    c = np.max(a)  # 防止溢出，超大数进行除法运算会出现溢出
    exp_a = np.exp(a - c)
    sum_exp_a = np.sum(exp_a)
    y = exp_a / sum_exp_a
    return y


x = np.arange(-5.0, 5.0, 0.1)
y = softmax(x)
plt.plot(x, y)
plt.show()
