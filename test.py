### Tests for entropy lib
from lib.utils import load_image
from lib.entropy import disp_en_2d, samp_en_2d, disp_samp_en_2d

# Test case 1
img = load_image('img/target/Kylberg/blanket1_1_0.0.jpg')

result = disp_en_2d(img, (2, 2))
assert abs(result - 4.7480125) < 0.000001

result = samp_en_2d(img, (3, 3))
assert abs(result - 6.5884678) < 0.000001

result = disp_samp_en_2d(img, (2, 2))
assert abs(result - 0.7339073) < 0.000001

# Test case 2
img = load_image('img/target/Kylberg/blanket1_2_0.0.jpg')

result = disp_en_2d(img, (2, 2))
assert abs(result - 4.7017913) < 0.000001

result = samp_en_2d(img, (3, 3))
assert abs(result - 5.9833763) < 0.000001

result = disp_samp_en_2d(img, (2, 2))
assert abs(result - 0.7574938) < 0.000001

print('[Tests all pass.]')