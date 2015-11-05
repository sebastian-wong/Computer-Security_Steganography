import os
import cv2
import numpy as np
import sys

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
    return int(bits1 + bits2[:7] + rep + bits2[9:], 2)

def extract_bits(msg):
    bits = bin(msg)
    bits = bits[bits.index('b')+1:].zfill(10)
    return bits[7:9]
    
def txt_to_bin(txt):
    bin_msg = []
    for i in range(0, len(txt)):
        bin_char = bin(ord(txt[i]))
        bin_char = bin_char[2:]         #strip '0b'
        bin_msg += list(bin_char)
    return bin_msg    

# in the encoding process, we replace the bits in HH coefficients
# at position 3-4 (int values of 4 and 8). This prevents the iwt
# from returning floating point values
def encode(img, msg):
    LL, LH, HL, HH = wt(img)
    s = LL.shape   
    msg = img_to_bin(msg)

    LL, LH, HL, HH = np.ravel(LL), np.ravel(LH), np.ravel(HL), np.ravel(HH)
    for i in range(0, len(msg)/8):
        LL[i] = replace_bits(LL[i], msg[i*8:i*8+2])
        LH[i] = replace_bits(LH[i], msg[i*8+2:i*8+4])
        HL[i] = replace_bits(HL[i], msg[i*8+4:i*8+6])
        HH[i] = replace_bits(HH[i], msg[i*8+6:i*8+8])
    LL = np.reshape(LL, s)
    LH = np.reshape(LH, s)
    HL = np.reshape(HL, s)
    HH = np.reshape(HH, s)
    return iwt(LL, LH, HL, HH)

def decode(img, (h,w)):
    LL, LH, HL, HH = wt(img)
    msg = ""
    LL = np.ravel(LL)
    LH = np.ravel(LH)
    HL = np.ravel(HL)
    HH = np.ravel(HH)
    for i in range(0, h*w):
        msg += extract_bits(LL[i]) + extract_bits(LH[i])
        msg += extract_bits(HL[i]) + extract_bits(HH[i])
    img = bin_to_msg(msg)
    return np.reshape(img, (h,w))

def encode2(img, msg):
    ll, lh, hl, hh = wt(img)
    res = encode(ll, msg)
    return iwt(res, lh, hl, hh)

def decode2(img, (h,w)):
    ll, lh, hl, hh = wt(img)
    return decode(ll, (h, w))

def test():
    image = cv2.imread("building.jpg")
    # imagex = cv2.imread("building.jpg", 0)
    # ll, lh, hl, hh = wt(imagex)
    # cv2.imwrite("building_wt.png", np.hstack((np.vstack((ll,hl)), np.vstack((lh,hh)))))


    b,g,r = cv2.split(image)
    image2 = cv2.imread("nus.png")
    b2,g2,r2 = cv2.split(image2)
    #res = cv2.merge((encode2(b, b2), encode2(g, g2), encode2(r, r2)))
    res = cv2.merge((encode(b, b2), encode(g, g2), encode(r, r2)))
    #cv2.imwrite("stegged.jpg", res, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    cv2.imwrite("stegged.png", res)

    res = cv2.imread("stegged.png")
    #res = cv2.imread("stegged.jpg")
    b3,g3,r3 = cv2.split(res)
    s = b2.shape
    #decoded = cv2.merge((decode2(b3, s), decode2(g3, s), decode2(r3, s)))
    decoded = cv2.merge((decode(b3, s), decode(g3, s), decode(r3, s)))
    cv2.imwrite("extracted.png", decoded)

def main():
    if (len(sys.argv) <= 1):
        print "No args"
        return
    if (sys.argv[1] == "-e"):
        if (len(sys.argv) != 5):
            print "Error, 4 arguments expected"
        else:
            print "encode"
    elif (sys.argv[1] == "-d"):
        if (len(sys.argv) != 4):
            print "Error, 3 arguments expected"
        else:
            print "decode"
            #stegged = cv2.imread(sys.argv[2])
            #b3,g3,r3 = cv2.split(res)
            #s = b2.shape
            #decoded = cv2.merge((decode2(b3, s), decode2(g3, s), decode2(r3, s)))
            #cv2.imwrite(sys.argv[3], decoded)

if __name__ == "__main__":
    #main()
    test()
