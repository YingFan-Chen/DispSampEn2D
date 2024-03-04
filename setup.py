from lib.generate.mix import *
from lib.generate.pattern import *
from lib.generate.noise import *
from lib.misc import *
from math import sqrt

# Sinusoidal + white noise
size_array = [32, 64, 128]
p_array = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

for size in size_array:
    img = sinusoidal_pattern(size, size, 12)
    noise = uniform_white_noise(size, size, sqrt(3), -sqrt(3))
    for p in p_array:
        output = mix(img, noise, p)
        save_image(f'image/target/sin_uniform/{p}_{size}.jpg', output)

# Brodatz + white noise
group_array = ['D5', 'D15', 'D30', 'D36', 'D45', 'D75', 'D93', 'D95', 'D102']
p_array = [0.0, 0.3, 0.5, 0.7]
noise = uniform_white_noise(128, 128, 255, 0)
for group in group_array:
    # size: 640x640
    src = load_image(f'image/src/brodatz/{group}.tif')

    count = 0
    row, col = src.shape
    # 81 samples
    for i in range(0, row - 64, 64):
        for j in range(0, col - 64, 64):
            img = src[i:i+128, j:j+128]
            for p in p_array:
                output = mix(img, noise, p)
                save_image(f'image/target/brodatz_{p}/{group}_{count}.jpg', output)
            count = count + 1

# Klberg + white noise
group_array = ['blanket1', 'canvas1', 'ceiling1', 'floor1', 'floor2', 'rice1', 'rug1', 'scarf1', 'scarf2', 'screen1']
subgroup_array = ['a', 'b', 'c', 'd']
p_array = [0.0, 0.3, 0.5, 0.7]
noise = uniform_white_noise(128, 128, 255, 0)
for group in group_array:
    count = 0
    for subgroup in subgroup_array:
        for j in range(1, 41):
            idx = str(j).zfill(3)
            # size: 576x576
            src = load_image(f'image/src/kylberg/{group}-{subgroup}-p{idx}.png')

            # Take the left-top cornor sample with the size of 128x128.
            img = src[0:128, 0:128]
            for p in p_array:
                output = mix(img, noise, p)
                save_image(f'image/target/kylberg_{p}/{group}_{count}.jpg', output)
            count = count + 1