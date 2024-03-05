import numpy as np
import math
import ctypes
from scipy.special import ndtr

def DefaultNumberOfClassification(col, row, m):
    return max(2, int(math.floor((row - m) * (col - m)) ** (1 / ((m + 1) * (m + 1)))))

def DispSampEn2D(img, m = 2, c = -1):
    row, col = img.shape

    # If input c < 0, then use the default value.
    if c < 0:
        c = DefaultNumberOfClassification(col, row, m)

    # Preprocessing
    img_ndcf = ndtr((img - np.mean(img)) / np.std(img))
    img_class = np.digitize(img_ndcf, np.arange(0, 1, 1/c))

    # Call C++ library
    arr = []
    for i in range(row):
        arr.append((ctypes.c_double * col) (*img_class[i]))
    lib = ctypes.CDLL("cpplib/DispSampEn2D.dll", winmode = 0)
    DispSampEn2DCaller = lib.DispSampEn2DCaller
    DispSampEn2DCaller.restype = ctypes.c_double
    ret = DispSampEn2DCaller(((ctypes.c_double * col) * row) (*arr), (ctypes.c_int32) (row), (ctypes.c_int32) (col), (ctypes.c_int32) (m))

    if ret == -1:
        return math.inf
    elif ret == -2:
        return math.nan
    else:
        return ret