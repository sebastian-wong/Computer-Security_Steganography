#!/usr/bin/env python
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt


 def readHiddenText():
    text_file = open(os.getcwd() + "/Input/msg.txt", "r")
    msg = text_file.read()
    text_file.close()
    return msg
	
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
	msg=[None]*len(bin_msg)/2
	size=len(bin_msg)
	for i in range(0, size):
		msg[i] = bin_msg[i] + bin_msg[i+1]
		i += 2
    return msg
	

def encodeImage(img, message) :
	rows, columns = img.shape
	array = np.zeros([rows,columns])
	checkArray = np.zeros([rows,columns])
	# set array to determine placement
	subtractionArray =np.zeros([4,4])
	subtractionArray[0][0] = '00'
	subtractionArray[0][1] = '100'
	subtractionArray[0][2] = '10'
	subtractionArray[0][3] = '1'
	subtractionArray[1][0] = '000'
	subtractionArray[1][1] = '01'
	subtractionArray[1][2] = '101'
	subtractionArray[1][3] = '11'
	subtractionArray[2][0] = '00'
	subtractionArray[2][1] = '001'
	subtractionArray[2][2] = '10'
	subtractionArray[2][3] = '110'
	subtractionArray[3][0] = '0'
	subtractionArray[3][1] = '01'
	subtractionArray[3][2] = '010'
	subtractionArray[3][3] = '11'
	
	bin_msg = Msg2Binary(message)
	
	 # for left and right region
    columnRemainder = columns % 2
    leftSectionEnd = (columns-columnRemainder)/2 - 1
    rightSectionEnd = columns-columnRemainder
    # for top and bottom region
    rowRemainder = rows % 2
    topSectionEnd = (rows-rowRemainder)/2 - 1
    bottomSectionEnd = rows-rowRemainder
	
	HH_heightIndex = topSectionEnd+1
	HH_widthIndex = leftSectionEnd+1
	LH_heightIndex = topSectionEnd+1
	LH_widthIndex = 0
	HL_heightIndex = 0
	HL_widthIndex = leftSectionEnd+1
	
	r = 0
	
	#if (len(bin_msg)<= (1.5 * rows * columns))
		if (len(bin_msg) < rows * columns):
			r = len(bin_msg)  
		else :
			r= rows * columns
		
		# encoding according to raster-scan order (STEP2)
		for i in range(0, r):
			
			x = abs(bin_msg[i] - bin_msg[i+1])
		
			# put values into HH
			array[HH_heightIndex][HH_widthIndex] = x
			
		
			#obtain value from subtractionArray to determine locations
			y = subtractionArray[bin_msg[i]][bin_msg[i+1]]
			array[LH_heightIndex][LH_widthIndex] = y[0]
			checkArray[LH_heightIndex][LH_widthIndex] = 1
		
			if len(y) = 3:
				array[LH_heightIndex][LH_widthIndex+1] = y[1]
				checkArray[LH_heightIndex][LH_widthIndex+1] = 1
				array[HL_heightIndex][HL_widthIndex+1] = y[2]
				checkArray[HL_heightIndex][HL_widthIndex+1] = 1
			else :
				array[HL_heightIndex][HL_widthIndex+1] = y[1]
				checkArray[HL_heightIndex][HL_widthIndex+1] = 1
			
			HH_widthIndex+=1
			LH_widthIndex+=1
			HL_widthIndex+=1
			
			if HH_widthIndex == rightSectionEnd:
				HH_widthIndex = leftSectionEnd+1
				HH_heightIndex += 1
			else HH_widthIndex += 1
		
			if LH_widthIndex == leftSectionEnd:
				lH_widthIndex = 0
				LH_heightIndex += 1
			else LH_widthIndex += 1
		
			if HL_widthIndex == rightSectionEnd:
				HL_widthIndex = leftSectionEnd+1
				HL_heightIndex += 1
			else HL_widthIndex += 1
		
			i+=2
			
		#putting the remaining bits of the message ,if any, into LSB portions of the regions (STEP3)
		if r = rows * columns:
			l = len(bin_msg) - r	
			HH_heightIndex = topSectionEnd+1
			HH_widthIndex = rightSectionEnd
			LH_heightIndex = topSectionEnd+1
			LH_widthIndex = leftSectionEnd
			HL_heightIndex = 0
			HL_widthIndex = rightSectionEnd
			for i in range (0 , l):
				x = abs(bin_msg[r+1+i] - bin_msg[r+2+i])
		
				# put values into HH
				array[HH_heightIndex][HH_widthIndex] = x
		
				#obtain value from subtractionArray to determine locations
				y = subtractionArray[bin_msg[i]][bin_msg[i+1]]
				if len(y) = 3:
					if checkArray[LH_heightIndex][LH_widthIndex-1]==0 : 
						array[LH_heightIndex][LH_widthIndex-1] = y[0]
						checkArray[LH_heightIndex][LH_widthIndex-1] = 1
					if checkArray[LH_heightIndex][LH_widthIndex]==0   :	
						array[LH_heightIndex][LH_widthIndex] = y[1]
						checkArray[LH_heightIndex][LH_widthIndex] = 1
					if checkArray[HL_heightIndex][HL_widthIndex]==0   :							
						array[HL_heightIndex][HL_widthIndex] = y[2]
						checkArray[HL_heightIndex][HL_widthIndex] = 1
					
				else :
					if checkArray[LH_heightIndex][LH_widthIndex]==0 : 
						array[LH_heightIndex][LH_widthIndex] = y[0]
						checkArray[LH_heightIndex][LH_widthIndex] = 1
					if checkArray[HL_heightIndex][HL_widthIndex]==0   :							
						array[HL_heightIndex][HL_widthIndex] = y[1]
						checkArray[HL_heightIndex][HL_widthIndex] = 1
					
				HH_heightIndex+=1
				LH_heightIndex+=1
				HL_heightIndex+=1
			
				if HH_heightIndex == bottomSectionEnd :
					HH_heightIndex = topSectionEnd+1
					HH_widthIndex-=1
				if LH_heightIndex == bottomSectionEnd :
					LH_heightIndex = topSectionEnd+1
					LH_widthIndex-=1
				if HL_heightIndex == topSectionEnd :
					HL_heightIndex = 0
					HH_widthIndex-=1
					
				i+=2
    cv2.imwrite(os.getcwd() + "/Results/haarTransform.jpg", array)       

image = cv2.imread(os.getcwd() + "/Results/haarTransform.jpg")
#read msg from .txt file
hidden_text = readHiddenText()
#hiding text in image
msg_in_bin = Msg2Binary(hidden_text)
encodeImage(image, msg_in_bin)  
