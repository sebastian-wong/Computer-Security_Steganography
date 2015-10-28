#!/usr/bin/env python
import os
import cv2
import numpy as np
import pywt
from rs import RSCoder

import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

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

def img_to_bin(img):
    res = ""
    for index,bits in np.ndenumerate(img):
        res += (bin(bits))[2:].zfill(8)
    return res
def img_to_str(img):
    res = ""
    for index,bits in np.ndenumerate(img):
        res += unichr(bits)
    return res
def bin_to_str(bin_msg):
    msg = ""
    for i in range(0, len(bin_msg), 8):
        b = bin_msg[i:i+8]
        msg += str(unichr(int(b, 2)))
    return msg

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

def to_bin(c):
    return bin(ord(c))[2:].zfill(8)

def msg_to_bin(msg):
    rs = RSCoder(255, 223)
    final_msg = ""
    for i in range(0, len(msg), 223):
        ecc_msg = rs.encode(msg[i:i+223])
        ecc_msg = map(to_bin, list(ecc_msg))
        final_msg += ''.join(ecc_msg)
    return final_msg

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
    return idwt(np.add(LL,3), LH, HL, HH)

def test_encode(img, txt):
    h, w = img.shape
    LL, LH, HL, HH = dwt(img)
    bin_msg = combine_bin(txt_to_bin(txt))
    HH = np.ravel(HH)

    #encode
    for i in range(0, len(bin_msg)):
        bits = bin_msg[i]
        _hh = bin(int(round(HH[i])))
        _hh_index = _hh.index('b')+1
        hh_bin = _hh[:_hh_index] + _hh[_hh_index:].zfill(3)
        HH[i] = int(hh_bin[:len(hh_bin)-len(bits)] + bits, 2)

    HH = np.reshape(HH, LL.shape)
    res = idwt(LL, LH, HL, HH)
    #print res
    #cv2.imwrite(os.getcwd()  + '/Results/test_1.png', res)
    #res = cv2.imread(os.getcwd() + '/Results/test_1.png', cv2.CV_LOAD_IMAGE_GRAYSCALE)
    #print res
    ll, lh, hl, hh = dwt(res)
    #decode
    bits = ""
    hh = np.ravel(hh)
    for i in range(0, len(bin_msg)):
        hh_bin = bin(int(round(hh[i])))
        hh_bin = hh_bin[hh_bin.index('b')+1:]
        bit_pairs = hh_bin[len(hh_bin)-2:] if len(hh_bin) >= 2 else '0' + hh_bin
        bits += bit_pairs
    str_res = ""
    for i in range(0, len(bits), 7):
        bin_char = bits[i:i+7]
        str_res += str(unichr(int(bin_char, 2)))
    return str_res

def test_encode_img(img, wm):
    h, w = img.shape
    LL, LH, HL, HH = dwt(img)
    msg_str = img_to_str(wm)
    print len(msg_str)
    msg = msg_to_bin(msg_str)
    HH = np.ravel(HH)
    rs = RSCoder(255, 223)

    #encode image
    for i in range(0, len(msg), 2):
        bits = msg[i:i+2]
        _hh = bin(int(round(HH[i])))
        _hh_index = _hh.index('b')+1
        hh_bin = _hh[:_hh_index] + _hh[_hh_index:].zfill(3)
        HH[i] = int(hh_bin[:len(hh_bin)-len(bits)] + bits, 2)

    HH = np.reshape(HH, LL.shape)
    LH = np.reshape(LH, LL.shape)
    HL = np.reshape(HL, LL.shape)
    res = idwt(LL, LH, HL, HH)
    res = np.around(res)
    return res

def test_decode_img(img, wm):
    rs = RSCoder(255,223)
    msg_str = img_to_str(wm)
    msg = msg_to_bin(msg_str)
    LL, LH, HL, HH = dwt(img)
    HH = np.ravel(HH)
    bin_msg = ""
    for i in range(0, len(msg)/2):
        hh_bin = bin(int(round(HH[i])))
        hh_bin = hh_bin[hh_bin.index('b')+1:]
        bit_pairs = hh_bin[len(hh_bin)-2:] if len(hh_bin) >= 2 else '0' + hh_bin
        bin_msg += bit_pairs
    msg_str = ""
    for i in range(0, len(bin_msg), 8):
        digit = bin_msg[i:i+8]
        msg_str += unichr(int(digit, 2))
    decoded = ""
    #11475
    for i in range(0, len(msg_str), 255):
        decoded += rs.decode(msg_str[i:i+255])
    dc_list = list(decoded)
    print(len(dc_list))
    for i in range(0, len(dc_list)):
        dc_list[i] = ord(dc_list[i])

    result = dc_list[:wm.size]
    result = np.reshape(result, wm.shape)
    return result

image = cv2.imread(os.getcwd() + '/Input/flower2.jpg')
image2 = cv2.imread(os.getcwd() + '/Input/chrome.png')
def test():
    b1,g1,r1 = cv2.split(image)
    b2,g2,r2 = cv2.split(image2)
    '''
    b_r = test2_encode_img(b1, image2)
    g_r = test2_encode_img(g1, image2)
    r_r = test2_encode_img(r1, image2)
    result = cv2.merge((b_r, g_r, r_r))
    fractional, integral = np.modf(result)
    cv2.imwrite(os.getcwd()  + '/Results/stegged.jpg', integral)
    stegged = cv2.imread(os.getcwd()  + '/Results/stegged.jpg')
    stegged = np.add(stegged, fractional)
    b3,g3,r3 = cv2.split(stegged)
    x1,x2,x3 = test_decode_img(b3,b2)
    y1,y2,y3 = test_decode_img(g3,g2)
    z1,z2,z3 = test_decode_img(r3,r2)
    result1 = cv2.merge((x1, x2, x3))
    result2 = cv2.merge((y1, y2, y3))
    result3 = cv2.merge((z1, z2, z3))
    result4 = np.divide(np.add(np.add(result1, result2), result3), 3)
    results = np.vstack((np.hstack((result1, result2)), np.hstack((result3, result4))))
    cv2.imwrite(os.getcwd()  + '/Results/recovered.jpg', results)
    '''
    b_r = test_encode_img(b1, b2)
    g_r = test_encode_img(g1, g2)
    r_r = test_encode_img(r1, r2)
    result = cv2.merge((b_r, g_r, r_r))
    cv2.imwrite(os.getcwd()  + '/Results/stegged.png', result)
    stegged = cv2.imread(os.getcwd()  + '/Results/stegged.png')
    b3,g3,r3 = cv2.split(stegged)
    dc1 = test_decode_img(b3,b2)
    dc2 = test_decode_img(g3,g2)
    dc3 = test_decode_img(r3,r2)
    result3 = cv2.merge((dc1, dc2, dc3))
    cv2.imwrite(os.getcwd()  + '/Results/ecc_test.jpg', result3)

test()
