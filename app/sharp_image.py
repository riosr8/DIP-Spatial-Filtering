import numpy as np
import cv2

def neg_zero(image, filter_size):
    filter_size = 3
    if filter_size == 3:
        mask = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
        sharp_image = convolution(image, mask)
        sharp_image = image + sharp_image
        sharp_image = hist_equalization(sharp_image)
    return sharp_image


def neg_nonzero(image, filter_size):
    filter_size = 3
    if filter_size == 3:
        mask = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
        sharp_image = convolution(image, mask)
        sharp_image = image + sharp_image
        sharp_image = hist_equalization(sharp_image)
    return sharp_image


def pos_zero(image, filter_size):
    filter_size = 3
    if filter_size == 3:
        mask = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
        sharp_image = convolution(image, mask)
        sharp_image = image - sharp_image
        sharp_image = hist_equalization(sharp_image)
    return sharp_image


def pos_nonzero(image, filter_size):
    filter_size = 3
    if filter_size == 3:
        mask = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])
        sharp_image = convolution(image, mask)
        sharp_image = image - sharp_image
        sharp_image = hist_equalization(sharp_image)
    return sharp_image


def convolution(image, mask):
    w = image.shape[0]
    h = image.shape[1]

    flip_mask = np.flipud(np.fliplr(mask))
    w1, h1 = np.shape(flip_mask)
    image_pad = np.zeros((w + 2, h + 2))
    image_pad[1:-1, 1:-1] = image

    new_img = np.zeros((w, h))
    for x in range(0, h):
        for y in range(0, w):
             # multiplying mask values with the image matrix of filter size and the summation is stored at (y,x)
            new_img[y, x] = (flip_mask * image_pad[y: y + w1, x: x + h1]).sum()

    return new_img


def hist_equalization(image):
    info = image.copy().flatten()
    hist, div = np.histogram(info, 256, density=True)
    cum_dist = hist.cumsum()
    cum_dist = 255*cum_dist/cum_dist[-1]
    eq_newimg = np.interp(info, div[:-1], cum_dist)
    return eq_newimg.reshape(image.shape)
