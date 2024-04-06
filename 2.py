import math

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def func (x, x1):
    return math.sin(x) * math.cos(x1)

eps = 0.001
a0 = 0.01
prevY = 90
i = 0
a = a0
values = [0, 0]
y = func(values[0], values[1])


while (abs(y - prevY) > eps):
    while (i < len(values)):
        y = prevY
        sign = 1
        while(True):
            while (True):
                y = prevY
                values[i] = values[i] + sign * a
                prevY  = func(values[0], values[1])
                if (y < prevY ): break
            sign = sign * (-1)
            if (sign > 0): break
            a = a * 0.1

        i = i + 1

print(values[0], values[1], func(values[0], values[1]))

print("Другие значения в окрестности \n")
print(values[0] + 0.01, values[1], func(values[0] + 0.01, values[1]))
print(values[0] - 0.01, values[1], func(values[0] - 0.01, values[1]))
print(values[0], values[1] + 0.01, func(values[0], values[1] + 0.01))
print(values[0], values[1] - 0.01, func(values[0], values[1] - 0.01))


#ax_3d.plot(x, x, z)
#x = np.arange(-10, 10, 0.2)
#y = np.arange(90, 110, 0.2)
#xgrid, ygrid = np.meshgrid(x, y)
#zgrid = np.sin(xgrid) * np.sin(ygrid) / (xgrid * ygrid)
#zgrid = func(xgrid, ygrid)
#ax_3d.plot_wireframe(xgrid, ygrid, zgrid)