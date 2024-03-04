import numpy as np
from random import uniform, choice, gauss

def uniform_white_noise(row, col, max_value, min_value):
    ret = np.zeros((row, col))
    for i in range(row):
        for j in range(col):
            ret[i, j] = uniform(max_value, min_value)
    return ret

def salt_and_pepper_noise(row, col, salt_value, pepper_value):
    ret = np.zeros((row, col))
    for i in range(row):
        for j in range(col):
            ret[i, j] = choice([salt_value, pepper_value])
    return ret

def gaussian_white_noise(row, col, mu, sigma):
    ret = np.zeros((row, col))
    for i in range(row):
        for j in range(col):
            ret[i, j] = gauss(mu, sigma)
    return ret