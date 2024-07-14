import numpy as np
import ctypes
import math

from time import time
from scipy.special import ndtr

def disp_en_2d(img, m = (2, 2), mapping = 'ncdf', c = 5):
    assert len(m) == 2
    row, col = img.shape
    m_row, m_col = m

    print(f'DispEn2D start: m = {m}, mapping = {mapping}, c = {c}.')
    start_time = time()

    if mapping == 'linear':
        mat = np.digitize(img, np.arange(np.min(img), np.max(img), np.ptp(img) / c))
    elif mapping == 'ncdf':
        mat_tmp = ndtr((img - np.mean(img)) / np.std(img))
        mat = np.digitize(mat_tmp, np.arange(0, 1, 1 / c))
    else:
        raise ValueError('No matching mapping function.')

    arr = []
    for i in range(row):
        arr.append((ctypes.c_double * col) (*mat[i]))

    lib = ctypes.CDLL('lib/entropy.dll', winmode = 0)
    disp_en_2d_caller = lib.DispEn2DCaller
    disp_en_2d_caller.restype = ctypes.c_double
    ret = disp_en_2d_caller(((ctypes.c_double * col) * row) (*arr), (ctypes.c_int32) (row), (ctypes.c_int32) (col), (ctypes.c_int32) (m_row), (ctypes.c_int32) (m_col))

    end_time = time()
    print(f'DispEn2D end: elapsed time = {end_time - start_time}.')
    return ret

def samp_en_2d(img, m = (2, 2), r = 0.24):
    assert len(m) == 2
    row, col = img.shape
    m_row, m_col = m

    print(f'SampEn2D start: m = {m}, r = {r}.')
    start_time = time()

    arr = []
    for i in range(row):
        arr.append((ctypes.c_double * col) (*img[i]))

    lib = ctypes.CDLL('lib/entropy.dll', winmode = 0)
    samp_en_2d_caller = lib.SampEn2DCaller
    samp_en_2d_caller.restype = ctypes.c_double
    ret = samp_en_2d_caller(((ctypes.c_double * col) * row) (*arr), (ctypes.c_int32) (row), (ctypes.c_int32) (col), (ctypes.c_int32) (m_row), (ctypes.c_int32) (m_col), (ctypes.c_double) (r * np.std(img)))

    end_time = time()
    print(f'SampEn2D end: elapsed time = {end_time - start_time}.')
    if ret == -1:
        return math.inf
    elif ret == -2:
        return math.nan
    else:
        return ret

def disp_samp_en_2d(img, m = (2, 2), mapping = 'ncdf', c = -1):
    assert len(m) == 2
    row, col = img.shape
    m_row, m_col = m

    if c <= 0:
        c = max(2, int(math.floor((row - m_row) * (col - m_col)) ** (1 / ((m_row + 1) * (m_col + 1)))))

    print(f'DispEn2D start: m = {m}, mapping = {mapping}, c = {c}.')
    start_time = time()

    if mapping == 'linear':
        mat = np.digitize(img, np.arange(np.min(img), np.max(img), np.ptp(img) / c))
    elif mapping == 'ncdf':
        mat_tmp = ndtr((img - np.mean(img)) / np.std(img))
        mat = np.digitize(mat_tmp, np.arange(0, 1, 1 / c))
    else:
        raise ValueError('No matching mapping function.')

    arr = []
    for i in range(row):
        arr.append((ctypes.c_double * col) (*mat[i]))

    lib = ctypes.CDLL('lib/entropy.dll', winmode = 0)
    disp_samp_en_2d_caller = lib.DispSampEn2DCaller
    disp_samp_en_2d_caller.restype = ctypes.c_double
    ret = disp_samp_en_2d_caller(((ctypes.c_double * col) * row) (*arr), (ctypes.c_int32) (row), (ctypes.c_int32) (col), (ctypes.c_int32) (m_row), (ctypes.c_int32) (m_col))

    end_time = time()
    print(f'DispEn2D end: elapsed time = {end_time - start_time}.')
    if ret == -1:
        return math.inf
    elif ret == -2:
        return math.nan
    else:
        return ret
