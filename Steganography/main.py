import os
import LSB_steganography
import ImageComparison




def lsbEncoding(secret,name):
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

def waveletEncoding(secret,name):
    # Hiding text image
    if (secret == 1):
        # encoding for text
        hiddenText = readHiddenText(name)
        binaryTextImage
        
        





steganographyType = raw_input("Please enter the mode of steganography. \n 1) Least Significant Bit \n 2) Wavelet Transform")
secret = raw_input("Please enter the type of message to hide. \n 1) Text \n 2) Picture")
path = raw_input("Please enter the name of the file")
mainImage = cv2.imread(os.getcwd() + "/Input/flower.jpg")

if (steganographyType =- "1"):    
        
elif (steganographyType == '2'):
    

else:
    print "Invalid Input, please select one or two"
    