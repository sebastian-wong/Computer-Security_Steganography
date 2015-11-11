import os
import cv2
import LSB_steganography as lsb
#import ImageComparison
import steganography
import rs as reedSolomon
import polynomial
import ff   
import pyexiv2


def lsbEncoding(secret,name,coverImg,coverImgName):
    # Hiding text message
    if (secret == '1'):
        # read hidden text
        hidden_text = lsb.readHiddenText(name)
        # convert text to binary bits
        msg_in_bin = lsb.Msg2Binary(hidden_text)
        # hide in lsb bits of cover image
        img_result = lsb.encodeTextLSB(coverImg,msg_in_bin)
        cv2.imwrite(os.getcwd() + "/Results/" + coverImgName + "_lsb_text.png",img_result)
        #get metadata of image
        #metadata = pyexiv2.ImageMetadata(os.getcwd() + "/Results/" + coverImgName + "_lsb_text.png")
        #metadata.read()
        #key = 'Exif.Photo.UserComment'
        #value = str(len(hidden_text))
        #metadata[key] = pyexiv2.ExifTag(key, value)
        #write hidden msg length to metadata
        #metadata.write()

    if (secret == '2'):
        #read hidden image
        hidden_img = cv2.imread(os.getcwd() + "/Input/" + name)
        #get binarys bit for 3 colour spaces
        bin_msg_B ,bin_msg_G, bin_msg_R = lsb.Img2Binary(hidden_img)
        #hide lsb in lsb bits of cover img
        img_result = lsb.encodeImageLSB(bin_msg_B ,bin_msg_G, bin_msg_R,coverImg)
        cv2.imwrite(os.getcwd() + "/Results/" + coverImgName + "_lsb_image.png",img_result)
        #get metadata tof image
        #metadata = pyexiv2.ImageMetadata(os.getcwd() + "/Results/" + coverImgName + "_lsb_image.png")
        #metadata.read()
        #key = 'Exif.Photo.UserComment'
        #height, width , channels = hidden_img.shape
        #value = str(height) + " " + str(width)
        #metadata[key] = pyexiv2.ExifTag(key, value)
        #write hidden msg dimensions to metadata
        #metadata.write()

def lsbDecoding(secret,coverImgName,length):
    #decode hidden text
    if (secret == '1'):
        #img = cv2.imread(os.getcwd() + "/Results/" + coverImgName + "_lsb_text.png")
        img = cv2.imread(os.getcwd() + "/Results/" + coverImgName)
        #metadata = pyexiv2.ImageMetadata(os.getcwd() + "/Results/" + coverImgName + "_lsb_text.png")
        #metadata = pyexiv2.ImageMetadata(os.getcwd() + "/Results/" + coverImgName)
        #metadata.read()
        #tag = metadata['Exif.Photo.UserComment']
        #text_len = tag.value
        #bin_text = lsb.decodeTextLSB(img,int(text_len))
        bin_text = lsb.decodeTextLSB(img,int(length))
        text = lsb.constructText(bin_text)
        #write to .txt file
        lsb.writeHiddenText(text)

     #decode for hidden image
    if (secret == '2'):
        img = cv2.imread(os.getcwd() + "/Results/" + coverImgName)
        #print img
        #metadata = pyexiv2.ImageMetadata(os.getcwd() + "/Results/" + coverImgName)
        #metadata.read()
        #tag = metadata['Exif.Photo.UserComment']
        msg_len = []
        #msg_len = tag.value.split()
        msg_len = length.split()
        msg_B ,msg_G, msg_R  = lsb.decodeImageLSB(img,int(msg_len[0]),int(msg_len[1]))
        img_result = lsb.constructImg(int(msg_len[0]),int(msg_len[1]),msg_B, msg_G, msg_R)
        img_result.astype('uint8')
        cv2.imwrite(os.getcwd() + "/ExtractedSecret/" + coverImgName + "_lsb_hidden.png",img_result)


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

def lsbDecode():
     decodeType = raw_input("Choose the decode type \n 1) Text \n 2) Image \n")
     decodeFile = raw_input("Enter name of file to be decoded \n")
     length = raw_input("Enter dimensions of hidden file \n")
     
     if decodeType == '1':
         lsbDecoding('1',decodeFile,length)
     if decodeType == '2':
         lsbDecoding('2',decodeFile,length)         

steganographyType = raw_input("Please enter the mode of steganography. \n 1) Least Significant Bit \n 2) Wavelet Transform \n")
mainImageName  = raw_input("Please enter the name of the main image \n")
secret = raw_input("Please enter the type of message to hide. \n 1) Text \n 2) Picture \n")
file = raw_input("Please enter the name of the file \n")
mainImage = cv2.imread(os.getcwd() + "/Input/" + mainImageName)
# remove .jpg or .png
mainImageName = mainImageName[:len(mainImageName)-4]


if (steganographyType == "1"):
    print "Using LSB encoding"
    lsbEncoding(secret,file,mainImage,mainImageName)
    #lsbDecoding(secret,mainImageName)
        
elif (steganographyType == '2'):
    print "Using wavelet encoding"
    waveletEncoding(mainImageName,mainImage,secret,file)
else:
    print "Invalid Input, please select one or two"
    
