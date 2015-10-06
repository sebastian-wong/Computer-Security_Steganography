#!/usr/bin/env python
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

def readImage():
    image = cv2.imread(os.getcwd() + "/Input/flower.jpg")
    return image
    
def HaarTransform2D(img):
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
    cv2.imwrite(os.getcwd() + "/Results/haarTransform.jpg", verticalTransform)        
            
    
image = cv2.imread(os.getcwd() + "/Input/flower.jpg",cv2.CV_LOAD_IMAGE_GRAYSCALE)
HaarTransform2D(image)            
            
            
            
             
        
