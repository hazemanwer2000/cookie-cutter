#! /usr/bin/env python

import argparse
import itertools
import uuid
import cv2
import numpy as np
from util import *

# Helper(s)
def root_squared(val):
    n = 1
    n_2 = 1
    while (not (n_2 > val)):
        n += 1
        n_2 = n**2
        if (n_2 == val):
            return n
    return 0

# Constants:
w_limit = 1920
output_ext = 'png'

if __name__=='__main__':
    parser = argparse.ArgumentParser(
        description='Arrange a number of images as a matrix.')
    parser.add_argument('img', nargs='+', help='Images (w x h files).')
    args = parser.parse_args()

    img_n_2 = len(args.img)
    img_n = root_squared(img_n_2)
    
    if (img_n == 0):
        raise ValueError('Image count is not a squared number.')
    
    w = img_n
    h = img_n
    n = img_n_2

    imgs = [cv2.imread(i) for i in args.img]

    if any(i.shape != imgs[0].shape for i in imgs[1:]):
        raise ValueError('Not all images have the same shape.')

    img_h, img_w, img_c = imgs[0].shape

    imgmatrix = np.zeros((img_h * h,
                          img_w * w,
                          img_c),
                         np.uint8)

    imgmatrix.fill(255)    

    positions = itertools.product(range(w), range(h))
    for (x_i, y_i), img in zip(positions, imgs):
        x = x_i * (img_w)
        y = y_i * (img_h)
        imgmatrix[y:y+img_h, x:x+img_w, :] = img
    
    # Reduce image size, if it exceeds a specific limit

    img_h, img_w, _ = imgmatrix.shape
    
    if (img_w > w_limit):
        new_h = int(img_h * (w_limit / img_w))
        imgmatrix = cv2.resize(imgmatrix, (w_limit, new_h))
    
    f_name = iter_name(args.img[0])
    
    cv2.imwrite(f_name, imgmatrix)