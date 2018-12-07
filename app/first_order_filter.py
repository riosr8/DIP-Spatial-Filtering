from math import sqrt
import numpy

def prewitt_filter(image, size):
    row = len(image)
    col = len(image[0])
    FOD = [0]*row
    for i in range(0,row):
        FOD[i] = [0]*col
    pad = int(size / 2)
    for i in range(0 + pad, row - pad):
        for j in range(0 + pad, col - pad):
            sumV = 0.0
            sumH = 0.0
            for x in range(0, size):
                for y in range(0, size):
                    if y < pad:
                        sumH -= image[i + y - pad][j + x - pad]
                    elif y > pad:
                        sumH += image[i + y - pad][j + x - pad]
                    if x < pad:
                        sumV -= image[i + y - pad][j + x - pad]
                    elif x > pad:
                        sumV += image[i + y - pad][j + x - pad]
            sumH = min(255.0, abs(sumH))
            sumV = min(255.0, abs(sumV))
            FOD[i][j] = max(sumH, sumV, image[i][j])
            # Enable for fliter output
            # FOD[i][j] = max(sumH, sumV) 
    return numpy.asarray(FOD, numpy.uint8)

def sobel_filter(image, size, threshold =0):
    row = len(image)
    col = len(image[0])
    #FOD = image.copy()
    FOD = [0]*row
    for i in range(0,row):
        FOD[i] = [0]*col
    pad = int(size / 2)
    maxS = 0
    minS = 100000
    for i in range(0 + pad, row - pad):
        for j in range(0 + pad, col - pad):
            sumV = 0.0
            sumH = 0.0
            for x in range(0, size):
                for y in range(0, size):
                    weightH = size - pad - (abs(pad - x))+abs(pad - y)-1
                    weightV = size - pad - (abs(pad - y))+abs(pad - x)-1
                    if x == pad:
                        weightH = weightH * min(1, (pad - abs(pad - y)))
                    if y == pad:
                        weightV = weightV * min(1, (pad - abs(pad - x)))
                    if x < pad:
                        weightV = weightV * -1
                    if y < pad:
                        weightH = weightH * -1
                    if y != pad:
                        sumH += weightH * image[i + y - pad][j + x - pad]
                    if x != pad:
                        sumV += weightV * image[i + y - pad][j + x - pad]
            sumH = min(255.0, abs(sumH))
            sumV = min(255.0, abs(sumV))
            temp = sqrt(sumH * sumH + sumV * sumV)
            minS = min(minS, temp)
            maxS = max(maxS, temp)
            FOD[i][j] = temp
    for i in range(0 + pad, row - pad):
        for j in range(0 + pad, col - pad):
            FOD[i][j] = (FOD[i][j] - minS)/(maxS - minS)*255.0
            if FOD[i][j] >= threshold:
                FOD[i][j] = min(255, (FOD[i][j] + image[i][j]) / 2)
            else:
                FOD[i][j] = image[i][j]
    return numpy.asarray(FOD, numpy.uint8)
