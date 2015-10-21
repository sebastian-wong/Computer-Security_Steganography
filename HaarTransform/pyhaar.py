#!/usr/bin/env python
import os
import cv2
import numpy as np
import pywt

SUBTRACTION_ARRAY = np.array([
    ['00', '100', '10', '1'], ['000', '01', '101', '11'],
    ['00', '001', '10', '110'], ['0', '01', '010', '11']
])

def dwt(img):
    LL, (LH, HL, HH)= pywt.dwt2(data=img, wavelet='haar')
    #res = np.vstack((np.hstack((LL, LH)), np.hstack((HL, HH))))
    return LL, LH, HL, HH

def idwt(LL, LH, HL, HH):
    coeffs = (LL, (LH, HL, HH))
    return pywt.idwt2(coeffs, 'haar')

def txt_to_bin(txt):
    bin_msg = []
    for i in range(0, len(txt)):
        bin_char = bin(ord(txt[i]))
        bin_char = bin_char[2:]         #strip '0b'
        bin_msg += list(bin_char)
    return bin_msg

def combine_bin(bin_msg):               #combine every 2 consecutive bits
    msg = []
    while len(bin_msg) % 4 != 0:           #pad message
        bin_msg += ['0']
    for i in range(0, len(bin_msg)/2):
        msg += [bin_msg[i*2] + bin_msg[i*2+1]]
    return msg

def diff_sequence(bin_msg):
    seq = []
    pairs = []
    for i in range(0, len(bin_msg)/2):
        num1 = int(bin_msg[i*2], 2)
        num2 = int(bin_msg[i*2+1], 2)
        seq += [abs(num1-num2)]
        val = SUBTRACTION_ARRAY[num1][num2]
        val_len = 2 if len(val) == 3 else 1
        pairs += [ [val[:val_len], val[val_len:]] ]
    return seq, pairs

def encode(img, txt):
    h, w = img.shape
    LL, LH, HL, HH = dwt(img)

    bin_msg = txt_to_bin(txt)
    bin_msg2 = combine_bin(bin_msg[0:(h*w)])
    dif_seq, sub_pair = diff_sequence(bin_msg2)

    #STEP 2: encode message from range (0, M * N) into HH, LH, HL
    HH = np.ravel(HH)
    LH = np.ravel(LH)
    HL = np.ravel(HL)

    for i in range(0, len(dif_seq)):
        hh_bits = bin(dif_seq[i])[2:]
        lh_bits = sub_pair[i][0]
        hl_bits = sub_pair[i][1]

        _hh = bin(int(HH[i]))
        _hh_index = _hh.index('b')+1
        hh_bin = _hh[:_hh_index] + _hh[_hh_index:].zfill(3)
        _lh = bin(int(LH[i]))
        _lh_index = _lh.index('b')+1
        lh_bin = _lh[:_lh_index] + _lh[_lh_index:].zfill(3)
        _hl = bin(int(HL[i]))
        _hl_index = _hl.index('b')+1
        hl_bin = _hl[:_hl_index] + _hl[_hl_index:].zfill(3)

        HH[i] = int(hh_bin[:len(hh_bin)-len(hh_bits)] + hh_bits, 2)
        LH[i] = int(lh_bin[:len(lh_bin)-len(lh_bits)] + lh_bits, 2)
        HL[i] = int(hl_bin[:len(hl_bin)-len(hl_bits)] + hl_bits, 2)

    #STEP 3-4: To be implemented
    HH = np.reshape(HH, LL.shape)
    LH = np.reshape(LH, LL.shape)
    HL = np.reshape(HL, LL.shape)
    return idwt(LL, LH, HL, HH)

image = cv2.imread(os.getcwd() + '/Input/flower.jpg', cv2.CV_LOAD_IMAGE_GRAYSCALE)
msg = 3 * "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
cv2.imwrite(os.getcwd()  + '/Results/test_1.jpg', encode(image, msg))
