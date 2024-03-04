import numpy as np
from random import uniform

def uniform_white_noise(row, col, max_value, min_value):
    ret = np.zeros((row, col))
    for i in range(row):
        for j in range(col):
            ret[i, j] = uniform(max_value, min_value)
    return ret