#!/usr/bin/env python
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt


def InverseHaarTransform2D(img):
    rows, columns = img.shape
	image = np.zeros([rows,columns])
    iVerticalTransform = np.zeros([rows,columns])
    iHorizontalTransform = np.zeros([rows,columns])
    # for left and right region
    columnRemainder = columns % 4
    leftSectionEnd = (columns-columnRemainder)/2 - 1
    rightSectionEnd = columns-columnRemainder
    # for top and bottom region
    rowRemainder = rows % 2
    topSectionEnd = (rows-rowRemainder)/2 - 1
    bottomSectionEnd = rows-rowRemainder
	
    # inverting in blocks of 2 by column then row
	for width in range(0,rightSectionEnd):
        for height in range(0,topSectionEnd+1):
			x = (iVerticalTransform[height][width] + iVerticalTransform[height + topSectionEnd + 1][width])/2
			y = (iVerticalTransform[height][width] - iVerticalTransform[height + topSectionEnd + 1][width])/2
			iHorizontalTransform[2*height][width] = x
			iHorizontalTransform[2*height+1][width] = y
           
	# inverting in blocks of 4 by row then column
    for height in range(0, bottomSectionEnd):
        for width in range(0,leftSectionEnd+1,2):
			a = (iHorizontalTransform[height][width] + iHorizontalTransform[height][width + leftSectionEnd +1])/2
			b = (iHorizontalTransform[height][width] - iHorizontalTransform[height][width + leftSectionEnd +1])/2
			c = (iHorizontalTransform[height][width+1] + iHorizontalTransform[height][width + leftSectionEnd +2])/2
			d = (iHorizontalTransform[height][width+1] - iHorizontalTransform[height][width + leftSectionEnd +2])/2 
			image[height][4*width] = a
			image[height][4*width+1] = b
			image[height][4*width+2] = c
			image[height][4*width+3] = d
			
    cv2.imwrite(os.getcwd() + "/Results/InverseHaarTransform.jpg", image)        
            
    
image = cv2.imread(os.getcwd() + "/Input/flower.jpg",cv2.CV_LOAD_IMAGE_GRAYSCALE)
InverseTransform2D(image)            
            
            
            
             
        
