#!/usr/bin/env python
import os
import cv2
import numpy as np

def HaarTransform2D(img):
    img = np.float32(img)
    rows, columns = img.shape
    horizontalTransform = np.zeros([rows,columns])
    # for left and right region
    columnRemainder = columns % 4
    leftSectionEnd = (columns-columnRemainder)/2 - 1
    rightSectionEnd = columns-columnRemainder
    # for top and bottom region
    rowRemainder = rows % 2
    topSectionEnd = (rows-rowRemainder)/2 - 1
    bottomSectionEnd = rows-rowRemainder
    # First operation
    for height in range(0, bottomSectionEnd):
        for width in range(0,rightSectionEnd,4):
            # Processing every 4 pixels in a row
            pixelA = img[height][width]
            pixelB = img[height][width+1]
            pixelC = img[height][width+2]
            pixelD = img[height][width+3]
            # Store sum in left section (Low frequency)
            horizontalTransform[height][width/2] = pixelA + pixelB
            horizontalTransform[height][width/2 + 1] = pixelC + pixelD
            # Store difference in right section (High frequency)
            horizontalTransform[height][width/2 + leftSectionEnd + 1] = pixelA - pixelB
            horizontalTransform[height][width/2 + leftSectionEnd + 2] = pixelC - pixelD
    # Second operation
    verticalTransform = np.zeros([rows,columns])
    for width in range(0,rightSectionEnd):
        for height in range(0,bottomSectionEnd,2):
            # Processing two pixels
            pixelX = horizontalTransform[height][width]
            pixelY = horizontalTransform[height+1][width]
            # Store the sum in top section
            verticalTransform[height/2][width] = pixelX + pixelY
            # Store the difference in bottom section
            verticalTransform[height/2 + topSectionEnd + 1][width] = pixelX - pixelY
    return verticalTransform

def inverseHaarTransform2D(img):
    img = np.float32(img)
    rows, columns = img.shape
    leftSectionEnd = (columns - columns % 4)/2 - 1
    topSectionEnd = int(rows)/2 - 1

    # inverse vertical
    result = np.zeros(img.shape)
    for width in range(0,leftSectionEnd):
        for height in range(0,topSectionEnd):
            W = img[height][width]
            X = img[height][width + leftSectionEnd + 1]
            Y = img[height + topSectionEnd + 1][width]
            Z = img[height + topSectionEnd + 1][width + leftSectionEnd + 1]
            A = np.average([W, X, Y, Z])

            result[height*2][width*2] = A
            result[height * 2][width * 2 + 1] = (W + X - 2 * A)/2
            result[height * 2 + 1][width * 2] = (W + Y - 2 * A)/2
            result[height * 2 + 1][width * 2 + 1] = (W + Z - 2 * A)/2
    return result

image = cv2.imread(os.getcwd() + "/Input/flower.jpg",cv2.CV_LOAD_IMAGE_GRAYSCALE)
res = HaarTransform2D(image)
cv2.imwrite(os.getcwd() + "/Results/haarTransform.jpg", res)
ires = inverseHaarTransform2D(res)
cv2.imwrite(os.getcwd() + "/Results/inverseHaarTransform.jpg", ires)
cv2.imwrite(os.getcwd() + "/Results/originalBW.jpg", image)
