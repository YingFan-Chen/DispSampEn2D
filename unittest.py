# Unit test for entropy library
from lib.misc import *
from lib.entropy.DispEn2D import *
from lib.entropy.DispSampEn2D import *
from lib.entropy.SampEn2D import *
from timeit import default_timer as timer

# Test case1
img = load_image("./image/target/kylberg_0.0/blanket1_0.jpg")

start = timer()
result = SampEn2D(img)
print("SampEn2D run time:", timer() - start)
assert abs(result - 6.5884678) < 0.000001

start = timer()
result = DispSampEn2D(img)
print("DispSampEn2D run time:", timer() - start)
assert abs(result - 0.7339073) < 0.000001

start = timer()
result = DispEn2D(img)
print("DispEn2D run time:", timer() - start)
assert abs(result - 4.7480125) < 0.000001

# Test case2
img = load_image("./image/target/kylberg_0.0/blanket1_1.jpg")

start = timer()
result = SampEn2D(img)
print("SampEn2D run time:", timer() - start)
assert abs(result - 5.9833763) < 0.000001

start = timer()
result = DispSampEn2D(img)
print("DispSampEn2D run time:", timer() - start)
assert abs(result - 0.7574938) < 0.000001

start = timer()
result = DispEn2D(img)
print("DispEn2D run time:", timer() - start)
assert abs(result - 4.7017913) < 0.000001