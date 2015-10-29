#!/usr/bin/env python
import os
import cv2
import numpy as np
import pywt
from rs import RSCoder

N = 255
K = 223
rs = RSCoder(N, K)

def dwt(img):
    LL, (LH, HL, HH)= pywt.dwt2(data=img, wavelet='haar')
    return LL, LH, HL, HH

def idwt(LL, LH, HL, HH):
    coeffs = (LL, (LH, HL, HH))
    return pywt.idwt2(coeffs, 'haar')
######################################
def round_multiply(HH):
    HH[np.abs(HH) < 1.0e-10] = 0
    return HH * 10.0

def i_round_multiply(HH):
    return HH / 10.0
######################################
def img_to_str(img):
    res = ""
    for i,d in np.ndenumerate(img):
        res += unichr(d)
    return res

def str_to_img(msg, shape):
    res = []
    for i in range(0, len(msg)):
        res.append(ord(msg[i]))
    res = res[:shape[0]*shape[1]]
    return np.reshape(res, shape)
######################################
def str_to_bin(msg):
    res = ""
    for i in range(0, len(msg)):
        res += bin(ord(msg[i]))[2:].zfill(8)
    return res

def bin_to_str(msg):
    res = ""
    for i in range(0, len(msg), 8):
        res += unichr(int(msg[i:i+8], 2))
    return res
######################################
def ecc_encode(msg):
    res = ""
    for i in range(0, len(msg), K):
        res += rs.encode(msg[i:i+K])
    return res

def ecc_decode(msg):
    res = ""
    for i in range(0, len(msg), N):
        message = msg[i:i+N]
        decoded =  rs.decode(message)
        res += decoded
    return res
######################################
def store_bits(container, bits):
    shape = container.shape
    container = np.ravel(container)
    for i in range(0, len(bits)/2):
        num = bin(int(container[i]))
        num = num[num.index('b') + 1:]
        if (len(num)<2):
            container[i] = int(bits[i*2:i*2+2], 2)
        else:
            container[i] = int(num[:len(num)-2] + bits[i*2:i*2+2],2)
    return np.reshape(container, shape)

def extract_bits(container, length):
    bits = ""
    container = np.ravel(container)
    for i in range(0, length):
        num = bin(int(container[i]))
        num = num[num.index('b') + 1:].zfill(8)
        bits += num[len(num)-2:]
    return bits

######################################
##### Encoding
######################################
def encode(img, msg):
    LL, LH, HL, HH = dwt(img)
    HH = round_multiply(HH)
    #encode msg with error correcting code
    msg_str = img_to_str(msg)
    ecc_bits = str_to_bin(ecc_encode(msg_str))
    #ecc_bits = str_to_bin(ecc_encode(msg))

    #store 2 bits in each HH value
    HH = store_bits(HH, ecc_bits)
    HH = i_round_multiply(HH)

    result =  idwt(LL, LH, HL, HH)
    for (i,j),d in np.ndenumerate(result):
        result[i][j] = round(result[i][j])
    return result
def encode_no_ecc(img, msg):
    LL, LH, HL, HH = dwt(img)
    HH = round_multiply(HH)
    #encode msg with error correcting code
    msg_str = img_to_str(msg)
    ecc_bits = str_to_bin(msg_str)
    #ecc_bits = str_to_bin(ecc_encode(msg))

    #store 2 bits in each HH value
    HH = store_bits(HH, ecc_bits)
    HH = i_round_multiply(HH)

    result =  idwt(LL, LH, HL, HH)
    for (i,j),d in np.ndenumerate(result):
        result[i][j] = round(result[i][j])
    return result

######################################
##### Decoding
######################################
def decode(img, msg):
    LL, LH, HL, HH = dwt(img)
    HH = round_multiply(HH)

    #extract bits
    length = int(np.ceil(msg.size / float(K)) * N * 4)
    bits = extract_bits(HH, length)
    decoded = ecc_decode(bin_to_str(bits))

    result = str_to_img(decoded, msg.shape)
    return result
def decode_no_ecc(img, msg):
    LL, LH, HL, HH = dwt(img)
    HH = round_multiply(HH)
    #extract bits
    length = msg.size * 4
    bits = extract_bits(HH, length)
    decoded = bin_to_str(bits)
    result = str_to_img(decoded, msg.shape)
    return result

def test():
    #image = cv2.imread(os.getcwd() + '/Input/flower2.jpg', cv2.CV_LOAD_IMAGE_GRAYSCALE)
    image = cv2.imread(os.getcwd() + '/Input/flower2.jpg')
    message = cv2.imread(os.getcwd() + '/Input/chrome.png')
    text = "AAA"
    #res = encode(image, text)
    #cv2.imwrite("Result.jpg", res)
    #decode(res, text)

    b,g,r = cv2.split(image)
    x,y,z = cv2.split(message)
    print "encoding blue channel..."
    res1 = encode(b, x)
    res12 = encode_no_ecc(b, x)
    print "encoding green channel..."
    res2 = encode(g, y)
    res22 = encode_no_ecc(g, y)
    print "encoding red channel..."
    res3 = encode(r, z)
    res32 = encode_no_ecc(r, z)

    cv2.imwrite(os.getcwd() + "/Results/Stegged.jpg", cv2.merge((res1,res2,res3)))
    cv2.imwrite(os.getcwd() + "/Results/Stegged2.jpg", cv2.merge((res12,res22,res32)))
    res1,res2,res3 = cv2.split(cv2.imread(os.getcwd() + '/Results/Stegged.jpg'))
    res1,res2,res3 = cv2.split(cv2.imread(os.getcwd() + '/Results/Stegged2.jpg'))

    print "decoding blue channel..."
    dec1 = decode(res1, x)
    dec12 = decode_no_ecc(res12, x)
    print "decoding green channel..."
    dec2 = decode(res2, y)
    dec22 = decode_no_ecc(res22, y)
    print "decoding red channel..."
    dec3 = decode(res3, z)
    dec32 = decode_no_ecc(res32, z)
    print "done."
    result = cv2.merge((dec1,dec2,dec3))
    result2 = cv2.merge((dec12,dec22,dec32))
    cv2.imwrite(os.getcwd() +"/Results/Result.jpg", result)
    cv2.imwrite(os.getcwd() +"/Results/Result2.jpg", result2)
