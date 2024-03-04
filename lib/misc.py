import matplotlib.pyplot as plt
import cv2
from pathlib import Path

# Use Matplotlib to save the image with automatic normalization to the range of 0 ~ 255.
def save_image(path, img):
    dir = ""
    str_array = path.split("/")[0:-1]
    for str in str_array:
        dir = dir + str + "/"
    Path(dir).mkdir(parents=True, exist_ok=True)
    plt.imsave(path, img, cmap=plt.cm.gray)

# Use CV2 to load image with grayscale.
def load_image(path):
    return cv2.imread(path, cv2.IMREAD_GRAYSCALE)