import numpy as np
from math import sin, pi

def sinusoidal_pattern(row, col, period):
    ret = np.zeros((row, col))
    for i in range(row):
        for j in range(col):
            ret[i, j] = sin(2 * pi * i / period) + sin(2 * pi * j / period)
    return ret