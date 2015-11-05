import os
import cv2
import LSB_steganography
import ImageComparison
import steganography



def lsbEncoding(image,secret,name):
    # Hiding text message
    if (secret == 1):
        # encoding for text
        hidden_text = readHiddenText(name)
        text_len = len(hidden_text)
        # hiding text in image
        msg_in_bin = Msg2Binary(hidden_text)
        img_result = modifyLSB(img,msg_in_bin)
        cv2.imwrite(os.getcwd() + "/Results/flower.jpg",img_result)
        metadata = pyexiv2.ImageMetadata(os.getcwd() + "/Results/flower.jpg")
        metadata.read()
        key = 'Exif.Photo.UserComment'
        value = str(text_len)
        metadata[key] = pyexiv2.ExifTag(key, value)
        metadata.write()

def waveletEncoding(image,secret,name):
    # Hiding text image
    # if (secret == 1):
    #     # encoding for text
    #     hiddenText = readHiddenText(name)
    #     binaryText = txt_to_bin(hiddenText)
    #     newImage = encode(image,binaryText)
    
    
    print "secret is ", secret    
    # Hiding image
    if (secret == '2'):
        # encoding for image
        b,g,r = cv2.split(image)
        hiddenImage = cv2.imread(os.getcwd() + "/Input/" + name)
        b2,g2,r2 = cv2.split(hiddenImage)
        binHiddenImage = steganography.img_to_bin(hiddenImage)
        res = cv2.merge((steganography.encode(b, b2), steganography.encode(g, g2), steganography.encode(r, r2)))
        cv2.imwrite(os.getcwd() + "/Results/newMilkyway.png", res)

def waveletDecoding():
    image = cv2.imread(os.getcwd() + "/Results/newMilkyway.png")        
    b,g,r = cv2.split(image)
    hiddenImage = cv2.imread(os.getcwd() + "/Input/mushroom.png")
    b2,g2,r2 = cv2.split(hiddenImage)
    s  = b2.shape        
    decoded = cv2.merge((steganography.decode(b,s), steganography.decode(g, s), steganography.decode(r, s)))    
    cv2.imwrite(os.getcwd() + "/ExtractedSecret/extracted.png", decoded)




steganographyType = raw_input("Please enter the mode of steganography. \n 1) Least Significant Bit \n 2) Wavelet Transform \n")
secret = raw_input("Please enter the type of message to hide. \n 1) Text \n 2) Picture \n")
path = raw_input("Please enter the name of the file \n")
mainImage = cv2.imread(os.getcwd() + "/Input/milkyway.jpg")

if (steganographyType == "1"):
    print "here"    
        
elif (steganographyType == '2'):
    print "Using wavelet encoding"
    waveletEncoding(mainImage,secret,path)
    

else:
    print "Invalid Input, please select one or two"
    