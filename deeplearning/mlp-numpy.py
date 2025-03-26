import numpy as np


def AND(x1, x2):
    x = np.array([x1, x2])
    w = np.array([0.5, 0.5])
    b = -0.7
    # w1, w2, theta = 0.5, 0.5, 0.7
    # tmp = x1*w1 + x2*w2
    tmp = np.sum(w*x) + b
    if tmp > 0:
        return 1
    else:
        return 0

print('AND')
print(AND(0, 0))
print(AND(1, 0))
print(AND(0, 1))
print(AND(1, 1))


def NAND(x1, x2):
    x = np.array([x1, x2])
    w = np.array([-0.5, -0.5])
    b = 0.7
    tmp = np.sum(w*x) + b
    if tmp > 0:
        return 1
    else:
        return 0


print('NAND')
print(NAND(0, 0))
print(NAND(1, 0))
print(NAND(0, 1))
print(NAND(1, 1))


def OR(x1, x2):
    x = np.array([x1, x2])
    w = np.array([0.5, 0.5])
    b = -0.2
    tmp = np.sum(w*x) + b
    if tmp > 0:
        return 1
    else:
        return 0


print('OR')
print(OR(0, 0))
print(OR(1, 0))
print(OR(0, 1))
print(OR(1, 1))


def XOR(x1, x2):
    s1 = NAND(x1, x2)
    s2 = OR(x1, x2)
    y = AND(s1, s2)
    return y


print('XOR')
print(XOR(0, 0))
print(XOR(1, 0))
print(XOR(0, 1))
print(XOR(1, 1))


def identity_function(x):
    return x


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def init_network():
    network = dict()
    network["W1"] = np.array([[0.1, 0.3, 0.5], [0.2, 0.4, 0.6]])
    print(network["W1"].shape)
    network["b1"] = np.array([0.1, 0.2, 0.3])
    network["W2"] = np.array([[0.1, 0.4], [0.2, 0.5], [0.3, 0.6]])
    print(network["W2"].shape)
    network["b2"] = np.array([0.1, 0.2])
    network["W3"] = np.array([[0.1, 0.3], [0.2, 0.4]])
    print(network["W3"].shape)
    network["b3"] = np.array([0.1, 0.2])
    return network


def forward(network, x):
    W1, W2, W3 = network["W1"], network["W2"], network["W3"]
    b1, b2, b3 = network["b1"], network["b2"], network["b3"]
    a1 = np.dot(x, W1) + b1
    z1 = sigmoid(a1)
    a2 = np.dot(z1, W2) + b2
    z2 = sigmoid(a2)
    a3 = np.dot(z2, W3) + b3
    return identity_function(a3)


network = init_network()
x = np.array([1.0, 0.5])
y = forward(network, x)
print(y)

x = np.array([[0.1, 0.8, 0.1], [0.3, 0.1, 0.6],
              [0.2, 0.5, 0.3], [0.8, 0.1, 0.1]])
# 矩阵的第 0 维是列，第 1 维是行
y = np.argmax(x, axis=1)
print(y)
