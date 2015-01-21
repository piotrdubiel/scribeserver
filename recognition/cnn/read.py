import sys
from draw import draw
from scipy.misc import imresize
import numpy as np
from load import classify

def read(gesture):
    image = draw(gesture)
    gray_image = np.asarray([[sum(p) / 3 for p in line] for line in image])
    shape = image.shape[:2]
    larger = shape.index(max(shape))
    new_shape = [0, 0]
    new_shape[larger] = 20
    new_shape[int(not larger)] = 20 * min(shape) / max(shape)
    new_image = (imresize(gray_image, new_shape)>0).astype(float)
    big_image = np.zeros((28,28))
    left = 14-new_image.shape[0]/2
    top = 14-new_image.shape[1]/2
    right = left + new_image.shape[0]
    bottom = top + new_image.shape[1]
    big_image[left:right, top:bottom] = new_image
    return classify(big_image)

if __name__ == "__main__":
    filename = sys.argv[1]
    read(filename)
