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

image = cv2.imread('/Input/flower.jpg',cv2.CV_LOAD_IMAGE_GRAYSCALE)
res = dwt(image)
res_norm = normalize(res)
cv2.imwrite('/Results/test.jpg', res_norm)
cv2.imwrite('/Results/test_inverse.jpg', idwt(res))
