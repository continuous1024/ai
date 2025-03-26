import matplotlib.pyplot as plt
import numpy as np
from matplotlib.image import imread

# sin 函数曲线
x = np.arange(0, 10, 0.1)
y = np.sin(x)
plt.plot(x, y, label='sin')
# plt.show()

# cos 函数曲线
y2 = np.cos(x)
plt.plot(x, y2, linestyle='--', label='cos')
plt.xlabel('x')
plt.ylabel('y')
plt.title('sin and cos')
plt.legend()
plt.show()

# 展示图片
img = imread('img.webp')
plt.imshow(img)
plt.show()
