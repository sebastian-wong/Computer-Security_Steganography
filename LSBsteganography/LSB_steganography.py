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
    
img = cv2.imread(os.getcwd() + "/Input/flower.jpg")
#read msg from .txt file
hidden_text = readHiddenText()
text_len = len(hidden_text)
#hiding text in image
msg_in_bin = Msg2Binary(hidden_text)
img_result = modifyLSB(img,msg_in_bin)
cv2.imwrite(os.getcwd() + "/Results/flower.jpg",img_result)
#retrieving text from image
bin_text = getBinaryText(img_result,text_len)
text = getHiddenText(bin_text)
#write to .txt file
writeHiddenText(text)
  
