import os
import cv2
import LSB_steganography
import ImageComparison
import steganography
import rs as reedSolomon
import polynomial
import ff   




# def lsbEncoding(image,secret,name):
#     # Hiding text message
#     if (secret == 1):
#         # encoding for text
#         hidden_text = readHiddenText(name)
#         text_len = len(hidden_text)
#         # hiding text in image
#         msg_in_bin = Msg2Binary(hidden_text)
#         img_result = modifyLSB(img,msg_in_bin)
#         cv2.imwrite(os.getcwd() + "/Results/flower.jpg",img_result)
#         metadata = pyexiv2.ImageMetadata(os.getcwd() + "/Results/flower.jpg")
#         metadata.read()
#         key = 'Exif.Photo.UserComment'
#         value = str(text_len)
#         metadata[key] = pyexiv2.ExifTag(key, value)
#         metadata.write()

def waveletEncoding(imageName,image,secret,name):
    # Hiding text image
    if (secret == '1'):
        # encoding for text
        hiddenText = LSB_steganography.readHiddenText(name)
        print "hidden msg is ", hiddenText
        #binaryText = steganography.msg_to_bin(hiddenText)
        binaryText = steganography.msg_to_bin_error_correction(hiddenText)
        print "hidden bin text is ", binaryText
        b,g,r = cv2.split(image)
        res = cv2.merge((steganography.encodeText(b, binaryText), steganography.encodeText(g, binaryText), steganography.encodeText(r, binaryText)))
        cv2.imwrite(os.getcwd() + "/Results/" + imageName + "_wavelet_text.png", res)
         
    # Hiding image
    if (secret == '2'):
        # encoding for image
        b,g,r = cv2.split(image)
        hiddenImage = cv2.imread(os.getcwd() + "/Input/" + name)
        b2,g2,r2 = cv2.split(hiddenImage)
        binHiddenImage = steganography.img_to_bin(hiddenImage)
        res = cv2.merge((steganography.encode(b, b2), steganography.encode(g, g2), steganography.encode(r, r2)))
        cv2.imwrite(os.getcwd() + "/Results/" + imageName + "_wavelet_image.png", res)

def waveletDecodeForImage(decodeImageName):
    image = cv2.imread(os.getcwd() + "/Results/" + decodeImageName)        
    b,g,r = cv2.split(image)
    # problematic, need to determine metadata instead or rereading
    hiddenImage = cv2.imread(os.getcwd() + "/Input/mushroom.png")
    b2,g2,r2 = cv2.split(hiddenImage)
    s  = b2.shape        
    decoded = cv2.merge((steganography.decode(b,s), steganography.decode(g, s), steganography.decode(r, s)))    
    cv2.imwrite(os.getcwd() + "/ExtractedSecret/" + "decoded" + decodeImageName[:len(decodeImageName) - 4] + ".png", decoded)

def waveletDecodeForText(decodeImageName):
    image = cv2.imread(os.getcwd() + "/Results/" + decodeImageName)  
    b,g,r = cv2.split(image)
    first = steganography.decodeText(b,223)
    second = steganography.decodeText(g,223)
    third = steganography.decodeText(r,223)
    print first, second, third    

#def waveletDecodeForText(name):
def waveletDecode():
    decodeType = raw_input("Choose the decode type \n 1) Text \n 2) Image \n")
    decodeFile = raw_input("Enter name of file to be decoded \n")
    if decodeType == '1':
        waveletDecodeForText(decodeFile)
    if decodeType == '2':
        waveletDecodeForImage(decodeFile)    



steganographyType = raw_input("Please enter the mode of steganography. \n 1) Least Significant Bit \n 2) Wavelet Transform \n")
mainImageName  = raw_input("Please enter the name of the main image \n")
secret = raw_input("Please enter the type of message to hide. \n 1) Text \n 2) Picture \n")
file = raw_input("Please enter the name of the file \n")
mainImage = cv2.imread(os.getcwd() + "/Input/" + mainImageName)
# remove .jpg or .png
mainImageName = mainImageName[:len(mainImageName)-4]



if (steganographyType == "1"):
    print "here"    
        
elif (steganographyType == '2'):
    print "Using wavelet encoding"
    waveletEncoding(mainImageName,mainImage,secret,file)
else:
    print "Invalid Input, please select one or two"
    