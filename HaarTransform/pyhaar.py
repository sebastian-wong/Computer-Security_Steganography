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

def img_to_bin(img):
    res = []
    for index,bits in np.ndenumerate(img):
        res += (bin(bits))[2:].zfill(8)
    return res

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

def best_bits(a, b, c):
    res = ''
    for i in range(0,len(a)):
        if a[i] == b[i] or a[i] == c[i]:
            res += a[i]
        else:
            res += b[i]
    return res


def test_encode_img(img, wm):
    h, w = img.shape
    LL, LH, HL, HH = dwt(img)
    bin_img = combine_bin(img_to_bin(wm))
    HH = np.ravel(HH)

    LH = np.ravel(LH)
    HL = np.ravel(HL)

    for i in range(0, len(bin_img)):
        bits = bin_img[i]
        _hh = bin(int(round(HH[i])))
        _hh_index = _hh.index('b')+1
        hh_bin = _hh[:_hh_index] + _hh[_hh_index:].zfill(3)
        HH[i] = int(hh_bin[:len(hh_bin)-len(bits)] + bits, 2)

        _lh = bin(int(round(LH[i])))
        _lh_index = _lh.index('b')+1
        lh_bin = _lh[:_lh_index] + _lh[_lh_index:].zfill(3)
        LH[i] = int(lh_bin[:len(lh_bin)-len(bits)] + bits, 2)

        _hl = bin(int(round(HL[i])))
        _hl_index = _hl.index('b')+1
        hl_bin = _hl[:_hl_index] + _hl[_hl_index:].zfill(3)
        HL[i] = int(hl_bin[:len(hl_bin)-len(bits)] + bits, 2)

    HH = np.reshape(HH, LL.shape)
    LH = np.reshape(LH, LL.shape)
    HL = np.reshape(HL, LL.shape)
    res = idwt(LL, LH, HL, HH)
    return res

def test_decode_img(img, owm):
    h,w = owm.shape
    ll, lh, hl, hh = dwt(img)
    #decode
    bits1 = ""
    bits2 = ""
    bits3 = ""
    hh = np.ravel(hh)
    lh = np.ravel(lh)
    hl = np.ravel(hl)
    for i in range(0, h*w*4):
        hh_bin = bin(int(round(hh[i])))
        hh_bin = hh_bin[hh_bin.index('b')+1:]
        bit_pairs1 = hh_bin[len(hh_bin)-2:] if len(hh_bin) >= 2 else '0' + hh_bin
        bits1 += bit_pairs1

        lh_bin = bin(int(round(lh[i])))
        lh_bin = lh_bin[lh_bin.index('b')+1:]
        bit_pairs2 = lh_bin[len(lh_bin)-2:] if len(lh_bin) >= 2 else '0' + lh_bin
        bits2 += bit_pairs2

        hl_bin = bin(int(round(hl[i])))
        hl_bin = hl_bin[hl_bin.index('b')+1:]
        bit_pairs3 = hl_bin[len(hl_bin)-2:] if len(hl_bin) >= 2 else '0' + hl_bin
        bits3 += bit_pairs3
        if len(bits1) != len(bits2) or len(bits1) != len(bits3) or len(bits2) != len(bits3):
            print bit_pairs1, bit_pairs2, bit_pairs3

    print len(bits1), len(bits2), len(bits3)
    bits = best_bits(bits1, bits2, bits3)
    bin_res = ""
    img_res = []
    for i in range(0, len(bits), 8):
        bin_char = bits[i:i+8]
        img_res += [int(bin_char, 2)]
    final = np.reshape(img_res, owm.shape)
    #cv2.imwrite(os.getcwd()  + '/Results/test_img.jpg', final)
    return final

image = cv2.imread(os.getcwd() + '/Input/flower2.jpg')
image2 = cv2.imread(os.getcwd() + '/Input/watermark.jpg')
def test():
    b1,g1,r1 = cv2.split(image)
    b2,g2,r2 = cv2.split(image2)
    b_r = test_encode_img(b1, b2)
    g_r = test_encode_img(g1, g2)
    r_r = test_encode_img(r1, r2)
    result = cv2.merge((b_r, g_r, r_r))
    fractional, integral = np.modf(result)
    cv2.imwrite(os.getcwd()  + '/Results/stegged.jpg', integral)
    stegged = cv2.imread(os.getcwd()  + '/Results/stegged.jpg')
    stegged = np.add(stegged, fractional)
    b3,g3,r3 = cv2.split(stegged)
    b_r2 = test_decode_img(b3,b2)
    g_r2 = test_decode_img(g3,g2)
    r_r2 = test_decode_img(r3,r2)
    result2 = cv2.merge((b_r2, g_r2, r_r2))
    cv2.imwrite(os.getcwd()  + '/Results/recovered.jpg', result2)
    print result
    print stegged
