from math import sqrt
import numpy

class Filter:

    def first_order_filter(self, image, size, threshold =0, sobel=False, second=False):
        row = len(image)
        col = len(image[0])
        FODh = [0] * row  # Matrix containing all horizontal edges
        FODv = [0] * row  # Matrix containing all vertical edges
        FOD = [0] * row
        for a in range(0, row):
            FODh[a] = [0] * col
            FODv[a] = [0] * col
            FOD[a] = [0] * col
        pad = int(size / 2)
        if not second:
            for i in range(0 + pad, row - pad):
                for j in range(0 + pad, col - pad):
                    sumV = 0.0
                    sumH = 0.0
                    for x in range(0, size):
                        for y in range(0, size):
                            if not sobel:
                                weightH = 1
                                weightV = 1
                            else:
                                weightH = size - pad - (abs(pad - x))+abs(pad - y)-1
                                weightV = size - pad - (abs(pad - y))+abs(pad - x)-1
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
                    FODh[i][j] = sumH
                    FODv[i][j] = sumV
                    if sobel:
                        temp = min(255.0, sqrt(FODh[i][j]*FODh[i][j] + FODv[i][j]*FODv[i][j]))
                        if temp >= threshold:
                            FOD[i][j] = temp
                        else:
                            FOD[i][j] = 0
                    else:
                        FOD[i][j] = (FODh[i][j] + FODv[i][j]) / 2
        else:
            for i in range(0 + pad, row - pad):
                for j in range(0 + pad, col - pad):
                    sumV = 0.0
                    sumH = 0.0
                    for x in range(0, size):
                        for y in range(0, size):
                            minusH = False
                            minusV = False
                            if x < pad:
                                minusV = True
                            if y < pad:
                                minusH = True
                            if y != pad:
                                if minusH:
                                    sumH -= image[i + y - pad][j + x - pad]
                                else:
                                    sumH += image[i + y - pad][j + x - pad]
                            if x != pad:
                                if minusV:
                                    sumV -= image[i + y - pad][j + x - pad]
                                else:
                                    sumV += image[i + y - pad][j + x - pad]
                    FODh[i][j] = sumH
                    FODv[i][j] = sumV
                    FOD[i][j] = (FODh[i][j], FODv[i][j])
        return numpy.asarray(FOD, numpy.uint8)

    def second_order_filter(self, image, size, threshold):
        row = len(image)
        col = len(image[0])
        SOD = [0] * row
        SODh = [0] * row
        SODv = [0] * row
        SODf = [0] * row
        for a in range(0, row):
            SOD[a] = [0] * col
            SODh[a] = [0] * col
            SODv[a] = [0] * col
            SODf = [0] * row
        SOD = Filter.first_order_filter(self, image, size, True)
        SOD = Filter.first_order_filter(self, SOD, size, True)
        pad = int(size/2)
        for i in range(1, row - 1):
            for j in range(1, col - 1):
                if (SOD[i-1][j] > 0 and SOD[i+1][j] < 0) or (SOD[i-1][j] < 0 and SOD[i+1][j] > 0): # Zero crossing
                    if abs(SOD[i-1][j] - SOD[i+1][j]) > threshold:
                        SODh[i][j] = 255
                if (SOD[i][j-1] > 0 and SOD[i][j+1] < 0) or (SOD[i][j-1] < 0 and SOD[i][j+1] > 0): # Zero crossing
                    if abs(SOD[i][j-1] - SOD[i][j+1]) > threshold:
                        SODv[i][j] = 255
                SODf = max(SODv[i][j], SODh[i][j])
        return SODf
