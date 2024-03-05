import numpy as np
import ctypes
import math

def SampEn2D(img, m = 3, ratio = 0.24):
    row, col = img.shape

    # Call C++ library
    arr = []
    for i in range(row):
        arr.append((ctypes.c_double * col) (*img[i]))
    lib = ctypes.CDLL("cpplib/SampEn2D.dll", winmode = 0)
    SampEn2DCaller = lib.SampEn2DCaller
    SampEn2DCaller.restype = ctypes.c_double
    ret = SampEn2DCaller(((ctypes.c_double * col) * row) (*arr), (ctypes.c_int32) (row), (ctypes.c_int32) (col), (ctypes.c_int32) (m), (ctypes.c_double) (ratio * np.std(img)))

    if ret == -1:
        return math.inf
    elif ret == -2:
        return math.nan
    else:
        return ret