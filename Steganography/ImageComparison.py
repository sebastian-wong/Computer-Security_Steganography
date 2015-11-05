import os
import numpy as np
import cv2
import math

# Computing mean squared error
# image1 is the original image, image2 is the noisy image
# meanSquaredError = 0 indicates complete similarity,
# meanSquaredError > 1, the higher the value the less similar the images
def computeMSE(image1,image2):
    rows, columns = grayImage1.shape
    meanSquaredError = np.sum((grayImage1.astype("float") - grayImage2.astype("float")) ** 2)
    meanSquaredError /= float(rows * columns)
    return meanSquaredError

# Computing Peak Signal to Noise ratio
def computePSNR(image1,image2):
    meanSquaredError = computeMSE(image1,image2)    
    PSNR = 10 * math.log(((255**2)/meanSquaredError),10)
    return PSNR
  
# Computing Peak Signal to Noise ration for luma component
# Human eye is most perceptive to the luma component    n    
def computeColourPSNR(image1,image2):
    lumaImage1 = cv2.cvtColor(image1, cv2.COLOR_BGR2YCR_CB)
    lumaImage2 = cv2.cvtColor(image2, cv2.COLOR_BGR2YCR_CB)
    cv2.imwrite("luma1.jpg",lumaImage1)
    Y1, Cr1, Cb1 = cv2.split(lumaImage1)
    Y2, Cr2, Cb2 = cv2.split(lumaImage2)
    return computePSNR(Y1,Y2)    
    
        
# change these files to test image
img1 = cv2.imread(os.getcwd() + "/Input/flower.jpg")
img2 = cv2.imread(os.getcwd() + "/Input/flower_edit.jpg")
# Testing coloured PSNR
colouredPSNR = computeColourPSNR(img1,img2)
# infinite means images are exactly the same
if (colouredPSNR == infinity):
    print "colouredPSNR for similar images"
    print "infinite"
print "images are different"
print colouredPSNR







