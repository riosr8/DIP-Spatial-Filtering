import cv2
import numpy as np
from app.smoothing import gaussian_yourchoice


def unsharp_mask(image, filter_size, k, threshold=0):
    m = len(image)
    n = len(image[0])
    final_image = np.zeros((m, n), dtype=int)

    # Unsharp mask filter
    # smooth_image = cv2.GaussianBlur(image,(filter_size,filter_size),0)  #testing purposes
    smooth_image = gaussian_yourchoice(image, filter_size)
    image_difference = cv2.absdiff(image, smooth_image)
    actual_mask = k * image_difference
    if(threshold == 0):
        final_image = cv2.add(image, actual_mask)
    else:
        for i in range(m):
            for j in range(n):
                if(image_difference[i][j] > threshold):
                    final_image[i][j] = image[i][j] + actual_mask[i][j]
                else:
                    final_image[i][j] = image[i][j]

    return final_image
