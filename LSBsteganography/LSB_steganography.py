'''
This program takes in a message from a text file and hides it
in a coloured image using the LSB method of steganography on
the time domain. The message hidden in the image is then
retrieved and written to a text file. 
'''

import os
import cv2
import numpy as np
import math
import pyexiv2

#converts characters in msg to binary
def Msg2Binary(hidden_txt):
    msg_size = len(hidden_txt)
    #creates a string array
    bin_msg=[None]*msg_size*7
    msg_index = 0
    for index in range(0,msg_size):
        #converts character in hidden msg to 8bit binary
        bin_char = bin(ord(hidden_txt[index]))
        #get 7 bit binary  
        bin_char = bin_char[2:9]
        #store each bit of ascii character in array
        for bin_index in range(0,7):
            bin_msg[msg_index] = bin_char[bin_index]
            msg_index += 1
    return bin_msg
    
def modifyLSB(img,bin_msg):
    rows,columns,channels = img.shape
    msg_index = 0
    for r in range(0,rows):
        for c in range(0,columns):
            blue,green,red = img[r][c]
        
            if(msg_index < len(bin_msg)) and (blue%2 != int(bin_msg[msg_index],10)):
                #modify lsb bit of pixel binary
                if (blue%2 == 0):
                    blue += 1
                else:
                    blue -= 1
                        
            msg_index += 1

            if(msg_index < len(bin_msg)) and (green%2 != int(bin_msg[msg_index],10)):
                #modify lsb bit of pixel binary
                if (green%2 == 0):
                    green += 1
                else:
                    green -= 1    

            msg_index += 1

            if(msg_index < len(bin_msg)) and (red%2 != int(bin_msg[msg_index],10)):
                #modify lsb bit of pixel binary
                if (red%2 == 0):
                    red += 1
                else:
                    red -= 1   

            msg_index += 1

            img[r][c] = [blue,green,red]
            if msg_index >= len(bin_msg):
                return img   

def getBinaryText(img,text_len):
    rows,columns,channels = img.shape
    bin_text=['']*text_len
    bit_count = 0
    msg_index = 0
    for r in range (0,rows):
        for c in range (0,columns):
            blue,green,red = img[r][c]
        
            #wrap around every 7 bits
            if bit_count == 7:
                bit_count = 0
                msg_index += 1
                    
            if msg_index < text_len: 
                lsb = blue%2
                bin_text[msg_index] += str(lsb)

            bit_count += 1

            #wrap around every 7 bits
            if bit_count == 7:
                bit_count = 0
                msg_index += 1

            if msg_index < text_len:
                lsb = green%2
                bin_text[msg_index] += str(lsb)

            bit_count += 1

            #wrap around every 7 bits
            if bit_count == 7:
                bit_count = 0
                msg_index += 1

            if msg_index < text_len:
                lsb = red%2
                bin_text[msg_index] += str(lsb) 

            bit_count += 1

            if msg_index >= text_len:
                return bin_text

def Img2Binary(img):
    rows, columns, layers = img.shape
    bin_msg_B = ['']*rows*columns*8
    bin_msg_G = ['']*rows*columns*8
    bin_msg_R = ['']*rows*columns*8
    index = 0
    bin_string_B = ''
    bin_string_G = ''
    bin_string_R = ''
    for r in range (0,rows):
        for c in range (0,columns):
            bin_string_B = bin(img[r][c][0])[2:].zfill(8)
            bin_string_G = bin(img[r][c][1])[2:].zfill(8)
            bin_string_R = bin(img[r][c][2])[2:].zfill(8)

            for bit_index in range (0,8):
                bin_msg_B[index] = bin_string_B[bit_index]
                bin_msg_G[index] = bin_string_G[bit_index]
                bin_msg_R[index] = bin_string_R[bit_index]     
                index = index + 1
                              
    return bin_msg_B, bin_msg_G, bin_msg_R

def encodeLSB(bin_msg_B, bin_msg_G, bin_msg_R,img):
    rows, columns, layers = img.shape
    index = 0
    for r in range (0,rows):
        for c in range (0,columns):
            blue,green,red = img[r][c]
            
            if (blue % 2 > int(bin_msg_B[index],2)):
                img[r][c][0] = img[r][c][0] - 1
                
            if (blue % 2 < int(bin_msg_B[index],2)):
                img[r][c][0] = img[r][c][0] + 1

            if (green % 2 > int(bin_msg_G[index],2)):
                img[r][c][1] = img[r][c][1] - 1
                
            if (green % 2 < int(bin_msg_G[index],2)):
                img[r][c][1] = img[r][c][1] + 1

            if (red % 2 > int(bin_msg_R[index],2)):
                img[r][c][2] = img[r][c][2] - 1
                
            if (red % 2 < int(bin_msg_R[index],2)):
                img[r][c][2] = img[r][c][2] + 1

            index = index + 1

            if (index >= len(bin_msg_B)):
                return img

def decodeLSB(img,height,width):
    rows, columns, layers = img.shape
    index = 0
    bit_count = 0
    bin_string_B = ''
    bin_string_G = ''
    bin_string_R = ''
    bin_msg_B = []
    bin_msg_G = []
    bin_msg_R = []

    
    for r in range (0,rows):
        for c in range (0,columns):
            blue,green,red = img[r][c]

            lsb = blue%2
            bin_string_B += str(lsb)
            lsb = green%2
            bin_string_G += str(lsb)
            lsb = red%2
            bin_string_R += str(lsb)
            bit_count = bit_count + 1

            if (bit_count == 8):
                bit_count = 0
                bin_msg_B += [int(bin_string_B, 2)]
                bin_msg_G += [int(bin_string_G, 2)]
                bin_msg_R += [int(bin_string_R, 2)]
                bin_string_B = ''
                bin_string_G = ''
                bin_string_R = ''
                index = index + 1  

            if (index >= height*width):
                return bin_msg_B, bin_msg_G, bin_msg_R

def constructImg(height,width,msg_B, msg_G, msg_R):
     img_result = np.zeros([height,width,3])
     index = 0
     for r in range(0,height):
         for c in range(0,width):
             img_result[r][c][0] = msg_B[index]
             img_result[r][c][1] = msg_G[index]
             img_result[r][c][2] = msg_R[index]
             index = index + 1
        
     return img_result
    
def getHiddenText(bin_text):
    text = ['']*len(bin_text)
    for index in range (0,len(bin_text)):
        char = chr(int(bin_text[index], 2))
        text[index] = char
    #return a string
    msg =  ''.join(text)
    print msg
    return msg

def writeHiddenText(text):
    text_file = open(os.getcwd() + "/Results/hiddenMsg.txt", "w")
    text_file.write(text)
    text_file.close()
    return

def readHiddenText():
    text_file = open(os.getcwd() + "/Input/msg.txt", "r")
    msg = text_file.read()
    text_file.close()
    return msg
    
img = cv2.imread(os.getcwd() + "/Input/tree.jpg")
img1 = cv2.imread(os.getcwd() + "/Input/mushroom.png")
height, width,channels = img1.shape

#encoding
bin_msg_B ,bin_msg_G, bin_msg_R = Img2Binary(img1)
img_result = encodeLSB(bin_msg_B ,bin_msg_G, bin_msg_R,img)
cv2.imwrite(os.getcwd() + "/Results/tree.png",img_result)
metadata = pyexiv2.ImageMetadata(os.getcwd() + "/Results/tree.png")
metadata.read()
key = 'Exif.Photo.UserComment'
value = str(height) + " " + str(width)
metadata[key] = pyexiv2.ExifTag(key, value)
metadata.write()

#decoding
img = cv2.imread(os.getcwd() + "/Results/tree.png")
metadata = pyexiv2.ImageMetadata(os.getcwd() + "/Results/tree.png")
metadata.read()
tag = metadata['Exif.Photo.UserComment']
msg_len = []
msg_len = tag.value.split()
msg_B ,msg_G, msg_R  = decodeLSB(img,int(msg_len[0]),int(msg_len[1]))
img_result = constructImg(int(msg_len[0]),int(msg_len[1]),msg_B, msg_G, msg_R)
img_result.astype('uint8')
cv2.imwrite(os.getcwd() + "/Results/hidden.jpg",img_result)


#read msg from .txt file
#hidden_text = readHiddenText()
#text_len = len(hidden_text)
#hiding text in image
#msg_in_bin = Msg2Binary(img1)
#msg_in_bin = Msg2Binary(hidden_text)
#img_result = modifyLSB(img,msg_in_bin)
#cv2.imwrite(os.getcwd() + "/Results/flower.jpg",img_result)
#retrieving text from image
#bin_text = getBinaryText(img_result,text_len)
#text = getHiddenText(bin_text)
#write to .txt file
#writeHiddenText(text)
  
