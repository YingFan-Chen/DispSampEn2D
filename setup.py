import gdown
import tarfile
import os
import numpy as np

from lib.utils import save_image, load_image, brodatz_groups, kylberg_groups, create_folders_for_path
from math import sqrt, sin, pi
from random import uniform, random

def main():
    image_row = 128
    image_col = 128

    p_array = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    # Synthetic dataset
    pattern = create_pattern_image(image_row, image_col, 12)
    noise = create_noise_image(image_row, image_col, sqrt(3), -sqrt(3))
    for p in p_array:
        output = mix(pattern, noise, p)
        save_image(f'img/target/mix/{p}.jpg', output)
    print('Create synthetic dataset.')

    # Brodatz dataset
    get_remote_dataset('Brodatz', 'https://drive.google.com/uc?id=1KBS9yZNRp4hNt6fsPoHRcMjYOAhCx0G8')
    noise = create_noise_image(image_row, image_col, 255, 0)
    for group in brodatz_groups:
        index = 1
        src = load_image(f'img/src/Brodatz/{group}.tif')
        row, col = src.shape
        for i in range(0, row - image_row // 2, image_row // 2):
            for j in range(0, col - image_col // 2, image_col // 2):
                img = src[i:i+image_row, j:j+image_col]
                for p in p_array:
                    output = mix(img, noise, p)
                    save_image(f'img/target/Brodatz/{group}_{index}_{p}.jpg', output)
                index += 1
    print('Create Brodatz dataset.')

    # Kylberg dataset
    get_remote_dataset('Kylberg', 'https://drive.google.com/uc?id=1GmeMcIyjRDzZ88DmgIWqOHqSz7NlSG-u')
    noise = create_noise_image(image_row, image_col, 255, 0)
    for group in kylberg_groups:
        index = 1
        for subgroup in ['a', 'b', 'c', 'd']:
            for num in range(1, 41):
                num = str(num).zfill(3)
                src = load_image(f'img/src/Kylberg/{group}-{subgroup}-p{num}.png')
                img = src[0:image_row, 0:image_col]
                for p in p_array:
                    output = mix(img, noise, p)
                    save_image(f'img/target/Kylberg/{group}_{index}_{p}.jpg', output)
                index += 1
    print('Create Kylberg dataset.')

### Helper function for synthetic dataset
def create_pattern_image(row, col, period):
    ret = np.zeros((row, col))
    for i in range(row):
        for j in range(col):
            ret[i, j] = sin(2 * pi * i / period) + sin(2 * pi * j / period)
    print(f'Create pattern with period {period} for image size {row}x{col}.')
    return ret

def create_noise_image(row, col, max_val, min_val):
    ret = np.zeros((row, col))
    for i in range(row):
        for j in range(col):
            ret[i, j] = uniform(max_val, min_val)
    print(f'Create noise in the range {min_val}~{max_val} for image size {row}x{col}.')
    return ret

def mix(image, noise, p):
    assert image.shape == noise.shape

    row, col = image.shape
    ret = np.zeros((row, col))
    for i in range(row):
        for j in range(col):
            if random() >= p:
                ret[i, j] = image[i, j]
            else:
                ret[i, j] = noise[i, j]
    print(f'Mix process with p = {p}.')
    return ret

### Helper function for real-world dataset
def get_remote_dataset(dataset, url):
    tar_path = f'img/src/{dataset}.tar'
    output_path = f'img/src'

    create_folders_for_path(tar_path)
    gdown.download(url, tar_path, quiet=False)
    print(f'Download {dataset}.tar.')

    with tarfile.open(tar_path, 'r') as tar:
        tar.extractall(path=output_path)
    print(f'Unzip {dataset}.tar.')

    os.remove(tar_path)
    print(f'Delete {dataset}.tar.')

if __name__ == '__main__':
    main()
