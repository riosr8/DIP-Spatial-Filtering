import cv2
import numpy as np
from app.smoothing import gaussian_yourchoice


def unsharp_mask(image, filter_size, k, threshold=0):
    m = len(image)
    n = len(image[0])
    final_image = np.zeros((m, n), dtype=float)
    image = image.astype(float)
    # Unsharp mask filter
    # smooth_image = cv2.GaussianBlur(image,(filter_size,filter_size),0)  #testing purposes
    smooth_image = gaussian_yourchoice(image, filter_size)
    smooth_image = smooth_image.astype(float)
    image_difference = cv2.absdiff(image, smooth_image)
    for i in range(m):
        for j in range(n):
            if(image_difference[i][j] > threshold):
                final_image[i][j] = image[i][j] + k * image_difference[i][j]
            else:
                final_image[i][j] = image[i][j]
    return final_image
