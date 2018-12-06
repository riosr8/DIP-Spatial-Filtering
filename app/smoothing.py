import numpy as np

def rotate_img(image):
    # Taking copy of image
    new_image = image.copy()

    # finding shape of image
    height = image.shape[0]
    width = image.shape[1]

    # for loop for making the new image
    for i in range(height):
        for j in range(width):
            new_image[i][j] = image[height - i - 1][width - j - 1]

    # returning the new image
    return new_image


#--------------------------Method for the averaging smoothing-----------------------------#
def averaging_yourchoice(image, n):
    matrix = [[]]
    matrix = [[1 for i in range(n)] for j in range(n)]
    print("Matrix is-:", matrix)
    mask = np.array(matrix)

    product = n * n

    # Finding shape of the image which has to be sharpened
    image_height = image.shape[0]
    image_width = image.shape[1]

    # Creating a blabk image with all 0s, hvaing the same size as image
    smooth_img = np.zeros(image.shape)

    # calling the  filter method for mask(mask)
    mask = rotate_img(mask)

    # Finding shape of the mask mask which is being used to sharpen the image
    mask_height = mask.shape[0]
    mask_width = mask.shape[1]

    # Finding the new shape for mask in order to have integer values
    new_mask_h = mask_height // 2
    new_mask_w = mask_width // 2

    # Convolution of image with mask
    for i in range(new_mask_h, image_height - new_mask_h):
        for j in range(new_mask_w, image_width - new_mask_w):
            sum = 0

            for mask_h in range(mask_height):
                for mask_w in range(mask_width):
                    sum = sum + \
                        (mask[mask_h][mask_w] * image[i - new_mask_h + mask_h][j - new_mask_w + mask_w])/product

            # Storing the sum in the final image
            smooth_img[i][j] = sum

    # Returning the sharpened image
    return smooth_img

def gaussian_yourchoice(image,n):
    g = gaussian(n, n, 2)
    mask = np.array(g);
    # Finding shape of the image which has to be sharpened
    image_height = image.shape[0]
    image_width = image.shape[1]

    mask = mask / np.sum(mask)

    # Creating a blabk image with all 0s, hvaing the same size as image
    smooth_img = np.zeros(image.shape)

    # calling the  filter method for mask(mask)
    mask = rotate_img(mask)

    # Finding shape of the mask mask which is being used to sharpen the image
    mask_height = mask.shape[0]
    mask_width = mask.shape[1]

    # Finding the new shape for mask in order to have integer values
    new_mask_h = mask_height // 2
    new_mask_w = mask_width // 2

    # Convolution of image with mask
    for i in range(new_mask_h, image_height - new_mask_h):
        for j in range(new_mask_w, image_width - new_mask_w):
            sum = 0

            for mh in range(mask_height):
                for mw in range(mask_width):
                    sum = sum + (mask[mh][mw] * image[i - new_mask_h + mh][j - new_mask_w + mw])

            # Storing the sum in the final image
            smooth_img[i][j] = sum

    # Returning the sharpened image
    return smooth_img


def gaussian(m,n,sigma):
    gaussian = np.zeros((m,n))
    print(gaussian)
    m = m//2
    n = n//2
    for x in range(-m,m+1):
        for y in range(-n,n+1):
            x1 = sigma * (2*np.pi)** 2
            x2 = np.exp(-(x**2+y**2)/(2*sigma**2))
            gaussian[x+m,y+n]=(1/x1)*x2
    return gaussian
