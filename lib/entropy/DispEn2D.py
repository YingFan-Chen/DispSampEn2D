import numpy as np
import ctypes
from scipy.special import ndtr

def DispEn2D(img, m = 2, c = 5):
    row, col = img.shape

    # Preprocessing
    img_ndcf = ndtr((img - np.mean(img)) / np.std(img))
    img_class = np.digitize(img_ndcf, np.arange(0, 1, 1/c))

    # Call C++ library
    arr = []
    for i in range(row):
        arr.append((ctypes.c_double * col) (*img_class[i]))
    lib = ctypes.CDLL("cpplib/DispEn2D.dll", winmode = 0)
    DispEn2DCaller = lib.DispEn2DCaller
    DispEn2DCaller.restype = ctypes.c_double
    ret = DispEn2DCaller(((ctypes.c_double * col) * row) (*arr), (ctypes.c_int32) (row), (ctypes.c_int32) (col), (ctypes.c_int32) (m))

    return ret