import os
import cv2
import LSB_steganography as lsb
import ImageComparison
import steganography
import numpy as np
import ff   
import pyexiv2


def lsbEncoding(cover, secret):
    #get binarys bit for 3 colour spaces
    bin_msg_B ,bin_msg_G, bin_msg_R = lsb.Img2Binary(secret)
    #hide lsb in lsb bits of cover img
    result = lsb.encodeImageLSB(bin_msg_B ,bin_msg_G, bin_msg_R,cover)
    return result

def lsbDecoding(stego,length):
    #decode for hidden image
    #msg_len = length.split()
    height , width = length.split()
    b,g,r = lsb.decodeImageLSB(stego,int(height), int(width)) 
    decoded = lsb.constructImg(int(height),int(width),b,g,r)
    return decoded

def waveletEncoding(cover,secret):
    # Hiding image
    # encoding for image
    b,g,r = cv2.split(cover)
    b2,g2,r2 = cv2.split(secret)
    result = cv2.merge((steganography.encode2(b, b2), steganography.encode2(g, g2), steganography.encode2(r, r2)))
    return result
    
def waveletDecodeForImage(stego,length):    
    b,g,r = cv2.split(stego)
    height, width = length.split()
    s = np.array([int(height),int(width)])        
    decoded = cv2.merge((steganography.decode2(b,s), steganography.decode2(g, s), steganography.decode2(r, s)))
    return decoded    

def waveletDecode():
    decodeFile = raw_input("Enter name of file to be decoded \n")
    length = raw_input("Enter dimensions of hidden image \n")
    stego = cv2.imread(os.getcwd() + "/Results/" + decodeFile)
    secret = waveletDecodeForImage(stego,length)
    cv2.imwrite(os.getcwd() + "/ExtractedSecret/" + "decoded" + decodeFile,secret)
    return secret

def lsbDecode():
    decodeFile = raw_input("Enter name of file to be decoded \n")
    length = raw_input("Enter dimensions of hidden image \n")
    stego = cv2.imread(os.getcwd() + "/Results/" + decodeFile)
    secret = lsbDecoding(stego,length)
    cv2.imwrite(os.getcwd() + "/ExtractedSecret/" + "decoded" + decodeFile,secret)       
    return secret
    
    
def TestForEncodeAndDecode():
    path = os.getcwd() + "/Original Images/"
    secrets = [
        cv2.imread(path+"secret1.png"), 
        cv2.imread(path+"secret2.jpg"), 
        cv2.imread(path+"secret3.jpg"), 
        cv2.imread(path+"secret4.png")
    ]
    for i in range(0, 20):
        image = cv2.imread(path + "image" + str(i+1) + ".jpg")
        index = i/5
        stego = lsbEncoding(image, secrets[index])
        p = path + "stegged_image" + str(i+1) + ".png"
        cv2.imwrite(p, stego)
        extracted = lsbDecoding(cv2.imread(p))
        cv2.imwrite(path+"extracted"+str(i+1) + ".png", extracted)
            
def TestDecodeAll():  
    length = raw_input("Enter dimensions of hidden image \n")
    path = os.getcwd() + "/LSB"
    folders = ['/BLUR/', '/BRIGHT/', '/CONTRAST/', '/JPG80/','/JPG85/', '/JPG90/', '/JPG95/']
    # folders = ['/PNG/']
    for x,folder in enumerate(folders):
        for i in range (1,21):
            extension = ".jpg" if x >= 3 else ".png" 
            coverImg = cv2.imread(path+folder + "stegged_image" + str(i) + extension)
            #extracted = lsbDecoding(coverImg,length)
            extracted = lsbDecoding(coverImg)
            cv2.imwrite(path + folder + "extracted" + str(i) + ".png",extracted)

def TestPSNRAll():
    # original secret
    secret = ["/Original Images/secret1.png", "/Original Images/secret2.jpg", "/Original Images/secret3.jpg", "/Original Images/secret4.png"]
    path = os.getcwd()    
    folders = ['/L1' , '/L2', "/LSB"]
    subfolders = ['/BLUR/', '/BRIGHT/', '/CONTRAST/', '/JPG80/','/JPG85/', '/JPG90/', '/JPG95/', '/PNG/']
    s = ""
    for folder in folders:
        for subfolder in subfolders:
            s +=  folder+subfolder + ": "
            for i in range(0,20):
                extracted = cv2.imread(os.getcwd() + folder + subfolder + "extracted" + str(i+1) + ".png")
                x = i / 5
                original = cv2.imread(os.getcwd()+ secret[x])
                results = ImageComparison.computeColourPSNR(original,extracted)
                #s += "PSNR values between secret" + str(i) " and" + " extracted" + str(results)
                s += str(results) + "\n"
            s += "\n\n"
        s += "\n\n\n"
    text_file = open(os.getcwd() + "/Results/PSNR.txt", "w")
    text_file.write(s)
    text_file.close()    

                
steganographyType = raw_input("Please enter the mode of steganography. \n 1) Least Significant Bit \n 2) Wavelet Transform \n")
mainImageName  = raw_input("Please enter the name of the main image \n")
secretImageName = raw_input("Please enter the name of the image to hide \n")
mainImage = cv2.imread(os.getcwd() + "/Input/" + mainImageName)
secretImage = cv2.imread(os.getcwd() + "/Input/" + secretImageName)
# remove prefix from name
mainImageName = mainImageName[:len(mainImageName)-4]
secretImageName = secretImageName[:len(secretImageName)-4]

if (steganographyType == "1"):
    print "Using LSB encoding"
    steganographyResult = lsbEncoding(mainImage,secretImage)
    cv2.imwrite(os.getcwd() + "/Results/" + mainImageName + "_lsb_encoded" + ".png",steganographyResult)
        
elif (steganographyType == '2'):
    print "Using wavelet encoding"
    steganographyResult = waveletEncoding(mainImage,secretImage)
    cv2.imwrite(os.getcwd() + "/Results/" + mainImageName + "_wavelet_encoded" + ".png",steganographyResult)    
    
# test mode for lsb
elif (steganographyType == '3'):
    lsbEncoding(file,mainImage,mainImageName)
    length = np.array(['100','100'])
    lsbDecoding(mainImageName + "_lsb_image.png", length)
    
# test mode for wavelet
elif (steganographyType == '4'):
    waveletEncoding(mainImageName,mainImage,file)
    length = np.array(['100','100'])
    waveletDecodeForImage(mainImageName + "_wavelet_image.png",length)        
else:
    print "Invalid Input, please select one or two"
    
