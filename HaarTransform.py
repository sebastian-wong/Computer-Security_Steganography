#!/usr/bin/env python
import os
import cv2
from matplotlib import pyplot as plt

def readImage():
    image = cv2.imread(os.getcwd() "Pictures/picture1.jpg")
    return image
    
def HaarTransform2D(img):
    rows, columns = img.shape
    horizontalTransform = np.zeros([rows,columns])
    # for left and right region
    columnRemainder = columns % 4
    leftSectionEnd = (columns-columnRemainder)/2
    rightSectionEnd = columns-columnRemainder
    # for top and bottom region
    rowRemainder = rows % 2
    topSectionEnd = (rows-rowRemainder)/2
    bottomSectionEnd = rows-rowRemainder
    # First operation
    for height in range(0, bottomSectionEnd):
        for width in range(0, rightSectionEnd):
            # Processing every 4 pixels in a row
            pixelA = img[height][width]
            pixelB = img[height][width+1]
            pixelC = img[height][width+2]
            pixelD = img[height][width+3]
            # Store sum in left section (Low frequency)
            horizontalTransform[height][width] = pixelA + pixelB
            horizontalTransform[height][width+1] = pixelC + pixelD
            # Store difference in right section (High frequency)
            horizontalTransform[height][width+leftSectionEnd] = pixelA - pixelB
            horizontalTransform[height][width+leftSectionEnd+1] = pixelC - pixelD
                  s
    # Second operation
    verticalTransform = np.zeros([rows,columns])
    for width in range(0,rightSectionEnd):
        for height in range(0,bottomSectionEnd):
            # Processing two pixels
            pixelX = img[height][width]
            pixelY = img[height+1][width]
            # Store the sum in top section 
            verticalTransform[height][width] = pixelX + pixelY
            # Store the difference in bottom section
            verticalTransform[height+topSectionEnd] = pixelX - pixelY
            
    
            
            
            
            
             
        
