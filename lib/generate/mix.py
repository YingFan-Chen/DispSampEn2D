import numpy as np
from random import random

def mix(img, noise, p):
    row, col = img.shape
    ret = np.zeros((row, col))
    for i in range(row):
        for j in range(col):
            if random() >= p:
                ret[i, j] = img[i, j]
            else:
                ret[i, j] = noise[i, j]
    return ret