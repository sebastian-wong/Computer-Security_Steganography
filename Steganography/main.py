import os
import cv2
import LSB_steganography as lsb
import ImageComparison
import numpy as np
import sys
import pyexiv2

def lsbEncoding(secret,name,coverImg):
    # Hiding text message
    if (secret == '1'):
        # read hidden text
        hidden_text = lsb.readHiddenText(name)
        # convert text to binary bits
        msg_in_bin = lsb.Msg2Binary(hidden_text)
        # hide in lsb bits of cover image
        img_result = lsb.encodeTextLSB(coverImg,msg_in_bin)
        cv2.imwrite(os.getcwd() + "/Results/LSBtext.png",img_result)
        #get metadata of image
        metadata = pyexiv2.ImageMetadata(os.getcwd() + "/Results/LSBtext.png")
        metadata.read()
        key = 'Exif.Photo.UserComment'
        value = str(len(hidden_text))
        metadata[key] = pyexiv2.ExifTag(key, value)
        #write hidden msg length to metadata
        metadata.write()

    if (secret == '2'):
        #read hidden image
        hidden_img = cv2.imread(os.getcwd() + "/Input/" + name)
        #get binarys bit for 3 colour spaces
        bin_msg_B ,bin_msg_G, bin_msg_R = lsb.Img2Binary(hidden_img)
        #hide lsb in lsb bits of cover img
        img_result = lsb.encodeImageLSB(bin_msg_B ,bin_msg_G, bin_msg_R,coverImg)
        cv2.imwrite(os.getcwd() + "/Results/LSBimage.png",img_result)
        #get metadata tof image
        metadata = pyexiv2.ImageMetadata(os.getcwd() + "/Results/LSBimage.png")
        metadata.read()
        key = 'Exif.Photo.UserComment'
        height, width , channels = hidden_img.shape
        value = str(height) + " " + str(width)
        metadata[key] = pyexiv2.ExifTag(key, value)
        #write hidden msg dimensions to metadata
        metadata.write()

def lsbDecoding(secret,name):
    #decode hidden text
    if (secret == '1'):
        img = cv2.imread(os.getcwd() + "/Results/LSBtext.png" )
        metadata = pyexiv2.ImageMetadata(os.getcwd() + "/Results/LSBtext.png")
        metadata.read()
        tag = metadata['Exif.Photo.UserComment']
        text_len = tag.value
        bin_text = lsb.decodeTextLSB(img,int(text_len))
        text = lsb.constructText(bin_text)
        #write to .txt file
        lsb.writeHiddenText(text)

    #decode for hidden image
    if (secret == '2'):
        img = cv2.imread(os.getcwd() + "/Results/LSBimage.png")
        metadata = pyexiv2.ImageMetadata(os.getcwd() + "/Results/LSBimage.png")
        metadata.read()
        tag = metadata['Exif.Photo.UserComment']
        msg_len = []
        msg_len = tag.value.split()
        msg_B ,msg_G, msg_R  = lsb.decodeImageLSB(img,int(msg_len[0]),int(msg_len[1]))
        img_result = lsb.constructImg(int(msg_len[0]),int(msg_len[1]),msg_B, msg_G, msg_R)
        img_result.astype('uint8')
        cv2.imwrite(os.getcwd() + "/Results/LSBhidden.jpg",img_result)
        
##def waveletEncoding(secret,name):
##    # Hiding text image
##    if (secret == 1):
##        # encoding for text
##        hiddenText = readHiddenText(name)
##        binaryTextImage
##        
        


def main():
    
    steganographyType = raw_input("Please enter the mode of steganography. \n 1) Least Significant Bit \n 2) Wavelet Transform")
    secret = raw_input("Please enter the type of message to hide. \n 1) Text \n 2) Picture")
    path = raw_input("Please enter the name of the file")
    mainImage = cv2.imread(os.getcwd() + "/Input/flower.jpg")

    if (steganographyType == "1"):
        lsbEncoding(secret,path,mainImage)
        lsbDecoding(secret,mainImage)
        
    #elif (steganographyType == '2'):
        

    else:
        print "Invalid Input, please select one or two"
    
if __name__ == "__main__":
    main()
