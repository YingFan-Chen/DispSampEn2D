import cv2
import matplotlib.pyplot as plt
import os

### Dataset groups
brodatz_groups = ['D5', 'D15', 'D30', 'D36', 'D45', 'D75', 'D93', 'D95', 'D102']
kylberg_groups = ['blanket1', 'canvas1', 'ceiling1', 'floor1', 'floor2', 'rice1', 'rug1', 'scarf1', 'scarf2', 'screen1']

### Helper function for reading/saving images
def create_folders_for_path(file_path):
    dir = os.path.dirname(file_path)
    if os.path.exists(dir):
        return
    os.makedirs(dir, exist_ok=True)
    print(f'Create folders for path: {file_path}.')

def save_image(file_path, img):
    create_folders_for_path(file_path)
    plt.imsave(file_path, img, cmap=plt.cm.gray)
    print(f'Save image: {file_path}.')

def load_image(file_path):
    ret = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    print(f'Load image: {file_path}.')
    return ret
