import os
import cv2
import numpy as np

# custom modified version of haar transform mapping integer to integer
# values range from -510 to 1010
def wt(img):
    img = img.astype(int)
    h, w = img.shape
    res = np.zeros((h-h%2, w-w%2))

    odd = img[:,1::2]
    even = img[:,0::2]
    res = np.hstack((even + odd, even - odd))
    odd = res[1::2]
    even = res[0::2]

    [LL, LH] = np.split(even + odd, 2, 1)
    [HL, HH] = np.split(even - odd, 2, 1)
    return LL, LH, HL, HH

def iwt(LL, LH, HL, HH):
    h,w = LL.shape
    img = np.zeros((h*2, w*2))
    for i in range(0, h):
        for j in range(0, w):
            z = (LL[i][j] - HL[i][j] - LH[i][j] + HH[i][j]) / 4
            y = (LL[i][j] - HL[i][j] - 2 * z) / 2
            x = (LL[i][j] - LH[i][j] - 2 * z) / 2
            img[i*2][j*2] = LL[i][j] - x - y - z
            img[i*2][j*2+1] = x
            img[i*2+1][j*2] = y
            img[i*2+1][j*2+1] = z
    return img

def img_to_bin(img):
    res = ""
    for index, val in np.ndenumerate(img):
        res += bin(val)[2:].zfill(8)
    return res

def bin_to_msg(bits):
    res = []
    for i in range(0, len(bits), 8):
        res.append(int(bits[i:i+8], 2))
    return res

def replace_bits(msg, rep):
    bits = bin(msg)
    bits1 = bits[:bits.index('b')+1]
    bits2 = bits[bits.index('b')+1:].zfill(10)
    return int(bits1 + bits2[:6] + rep + bits2[8:], 2)

# in the encoding process, we replace the bits in HH coefficients
# at position 3-4 (int values of 4 and 8). This prevents the iwt
# from returning floating point values
def encode(img, msg):
    LL, LH, HL, HH = wt(img)
    h, w = LL.shape
    msg = img_to_bin(msg)

    HH = np.ravel(HH)
    for i in range(0, len(msg)/2):
        HH[i] = replace_bits(HH[i], msg[i*2:i*2+2])
    HH = np.reshape(HH, (h, w))
    return iwt(LL, LH, HL, HH)

def decode(img, (h,w)):
    LL, LH, HL, HH = wt(img)
    msg = ""
    HH = np.ravel(HH)
    for i in range(0, h*w*4):
        bits = bin(HH[i])
        bits = bits[bits.index('b')+1:].zfill(10)
        msg += bits[6:8]
    img = bin_to_msg(msg)
    return np.reshape(img, (h,w))

def test():
    image = cv2.imread("flower.jpg")
    b,g,r = cv2.split(image)
    image2 = cv2.imread("chrome2.png")
    b2,g2,r2 = cv2.split(image2)
    res = cv2.merge((encode(b, b2), encode(g, g2), encode(r, r2)))
    cv2.imwrite("stegged.png", res)

    res = cv2.imread("stegged.png")
    b3,g3,r3 = cv2.split(res)
    s = b2.shape
    decoded = cv2.merge((decode(b3, s), decode(g3, s), decode(r3, s)))
    cv2.imwrite("extracted.png", decoded)
test()
