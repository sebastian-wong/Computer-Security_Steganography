#!/usr/bin/env python
import os
import cv2
import numpy as np
import pywt

def dwt(img):
    LL, (LH, HL, HH)= pywt.dwt2(data=img, wavelet='haar')
    res = np.vstack((np.hstack((LL, LH)), np.hstack((HL, HH))))
    return res

def idwt(img):
    height, width = img.shape
    height = int(height / 2)
    width = int(width /2)

    LL = img[0:height, 0:width]
    LH = img[0:height, width:]
    HL = img[height:, 0:width]
    HH = img[height:, width:]
    coeffs = (LL, (LH, HL, HH))
    return pywt.idwt2(coeffs, 'haar')

def normalize(img):
    return img * (255/img.max())

image = cv2.imread(os.getcwd() + '/Input/flower.jpg')
res = dwt(image)
res_norm = normalize(res)
cv2.imwrite('/Results/test.jpg', res_norm)
cv2.imwrite('/Results/test_inverse.jpg', idwt(res))

'''
# this is a test for color images
b, g, r = cv2.split(image)
bres = idwt(dwt(b))
gres = idwt(dwt(g))
rres = idwt(dwt(r))
cv2.imwrite(os.getcwd()  + '/Results/test_color.jpg', cv2.merge((bres, gres, rres)))
'''
