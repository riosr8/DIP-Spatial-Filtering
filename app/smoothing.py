import cv2
import numpy as np
from PIL import Image
import pylab
from pylab import imread,subplot,imshow,show
import matplotlib.pyplot as plt


#--------------------------Method for the filter mask(kernel)-----------------------------#
def filter(image):
    #Taking copy of image
    new_image = image.copy()
    
    #finding shape of image
    height = image.shape[0]
    width = image.shape[1]
    
    #for loop for making the new image
    for i in range(height):
        for j in range(width):
            new_image[i][j] = image[height - i - 1][width - j - 1]

#returning the new image
return new_image


#--------------------------Method for the averaging smoothing-----------------------------#
def averaging_yourchoice(image,n):
    matrix = [[]]
    matrix = [[1 for i in range(n)] for j in range(n)]
    print("Matrix is-:",matrix)
    mask = np.array(matrix)
    
    
    product = n * n
    
    # Finding shape of the image which has to be sharpened
    image_height = image.shape[0]
    image_width = image.shape[1]
    
    # Creating a blabk image with all 0s, hvaing the same size as image
    smooth_img = np.zeros(image.shape)
    
    # calling the  filter method for mask(mask)
    mask = filter(mask)
    
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
                    sum = sum + (mask[mh][mw] * image[i - new_mask_h + mh][j - new_mask_w + mw])/product
    
            # Storing the sum in the final image
        smooth_img[i][j] = sum

# Returning the sharpened image
    return smooth_img

#--------------------------Method for the gaussian smoothing-----------------------------#
def gaussian_yourchoice(image,mask):
    # Finding shape of the image which has to be sharpened
    image_height = image.shape[0]
    image_width = image.shape[1]
    
    mask = mask / np.sum(mask)
    
    # Creating a blabk image with all 0s, hvaing the same size as image
    smooth_img = np.zeros(image.shape)
    
    # calling the  filter method for mask(mask)
    mask = filter(mask)
    
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

def same_img(arr):
    nochange_img = Image.fromarray(arr)
    return nochange_img




def main():
    
    # Uisng Lenna0.jpg image
    img = Image.open("Lenna0.jpg")
    
    # Converting the image into array
    arr = np.array(img)
    
    # Displaying the menu options:
    print("The 4 Smoothing Masks are as follows-:")
    print("1. Averaging Filter")
    print("2. Gaussian Filter")
    print("---------------------------------------------------------------------------------")
    print("Choose 1 of the 2 options for Filters:")
    print("Option 1")
    print("Option 2")
    print(" ")
    option = input("Please enter your choice -:")
    print("Your choice is-:", option)
    
    if ((option == "Option 1") | (option == "1") | (option == "option 1") | (option == "option1") | (
                                                                                                     option == "Option1")):
        
        
        while True:
            try:
                size = int(input("Enter the size of filter in the range of 1 and 12"))
                if 1 <= int(size) <= 12:
                    print("Size entered is-:",abs(size))
                else:
                    size = int(input("Sorry, please try again! Enter the size of filter between 1 and 12"))
                    print("Size entered is-:", size)
            except ValueError:
                print("Not an integer! Try again.")
                continue
            else:
                break
        
        #matrix = [[]]
        #matrix = [[1 for i in range(size)] for j in range(size)]
        #print("Matrix is-:",matrix)
        #matrix_arr = np.array(matrix)
        #convoluted_image = averaging_yourchoice(arr, matrix_arr, size)
    convoluted_image = averaging_yourchoice(arr, size)

elif ((option == "Option 2") | (option == "2") | (option == "option 2") | (option == "option2") | (
                                                                                                   option == "Option2")):
    
    while True:
        try:
            size = int(input("Enter the size of filter in the range of 1 and 12"))
            if 1 <= int(size) <= 12:
                print("Size entered is-:", abs(size))
                else:
                    size = int(input("Sorry, please try again! Enter the size of filter between 1 and 12"))
                    print("Size entered is-:", size)
        except ValueError:
            print("Not an integer! Try again.")
            continue
            else:
                break

img = Image.open("Lenna0.jpg")
arr = np.array(img)

if ( size % 2 == 0):
    # Converting the resultant array into image
    res_img = img
        else:
            g = gaussian(size, size, 2)
            print(g)
            print(" ")
            mat_arr = np.array(g);
            convoluted_image = gaussian_yourchoice(arr, mat_arr)
            res_img = Image.fromarray(convoluted_image)


else:
    print("Wrong Option! Please enter a right choice")
    exit(0)
    
    # Displayign the resultant sharpened image
    imgplot = plt.imshow(res_img)
    plt.title(option)
    plt.xticks([])
    plt.yticks([])
    plt.show()
    plt.savefig(option + '.png')
    pylab.savefig('option.png')

#------------------------------Calling the main method-----------------------------------#
main()


