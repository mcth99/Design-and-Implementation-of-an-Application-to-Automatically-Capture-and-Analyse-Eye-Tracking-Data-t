import face_alignment
import cv2
import os
import tempfile
import numpy as np

from skimage import io

def identify_landmarks(inp, save_dir):
    fa = face_alignment.FaceAlignment(face_alignment.LandmarksType._2D, flip_input=False)
    
    predinput = io.imread(inp)
    preds = fa.get_landmarks(predinput)

##    print (preds[0])

    image = cv2.imread(inp)

##    scale_percent = 200000 # percent of original size
##    width = int(image.shape[1] * scale_percent / 100)
##    height = int(image.shape[0] * scale_percent / 100)
##    dim = (width, height)
##
##    image = cv2.resize(image, dim)

    height = image.shape[0]
    width = image.shape[1]

    white = np.zeros([height, width, 1], dtype = np.uint8)
    white.fill(255)

    def custom_lines(a, b):

        a = preds[0][a]
        b = preds[0][b]

        a = tuple(a)

        b = tuple(b)

        cv2.line(image, a, b, (0,0,0), 1)
        cv2.line(white, a, b, (0,0,0), 1)
##
##    for i in range(len(preds[0])):
##
##        for j in range(len(preds[0])):
##
##            custom_lines(i, j)

    for i in range(16):

        custom_lines(i, i+1)

    for i in range(17,21,1):

        custom_lines(i, i+1)

    for i in range(22,26,1):

        custom_lines(i, i+1)

    for i in range(27,30,1):

        custom_lines(i, i+1)

    for i in range(31,35,1):

        custom_lines(i, i+1)

##    for i in range(36,41,1):
##
##        a = preds[0][i]
##        b = preds[0][i+1]
##
##        a = tuple(a)
##
##        b = tuple(b)
##
##        cv2.line(image, a, b, (255,0,0), 2)

##    for i in range(42,47,1):
##
##        a = preds[0][i]
##        b = preds[0][i+1]
##
##        a = tuple(a)
##
##        b = tuple(b)
##
##        cv2.line(image, a, b, (255,0,0), 2)

##    for i in range(48,59,1):
##
##        a = preds[0][i]
##        b = preds[0][i+1]
##
##        a = tuple(a)
##
##        b = tuple(b)
##
##        cv2.line(image, a, b, (255,0,0), 2)

##    for i in range(60,67,1):
##
##        a = preds[0][i]
##        b = preds[0][i+1]
##
##        a = tuple(a)
##
##        b = tuple(b)
##
##        cv2.line(image, a, b, (255,0,0), 2)

    custom_lines(8, 30)
    custom_lines(0, 28)
    custom_lines(16, 28)
    custom_lines(1, 29)
    custom_lines(15, 29)
    custom_lines(48, 54)
    custom_lines(0, 17)
    custom_lines(16, 26)
    custom_lines(21, 27)
    custom_lines(22, 27)
    custom_lines(21, 31)
    custom_lines(22, 35)
    custom_lines(21, 22)
    custom_lines(31, 48)
    custom_lines(35, 54)
    custom_lines(3, 48)
    custom_lines(13, 54)
    custom_lines(10, 54)
    custom_lines(6, 48)
    custom_lines(13, 27)
    custom_lines(3, 27)
    custom_lines(1, 31)
    custom_lines(15, 35)
    custom_lines(48, 59)
    custom_lines(21, 48)
    custom_lines(22, 54)

    for i in range(54, 59, 1):

        custom_lines(i, i+1)

    cv2.imshow("Image", image)
    cv2.imshow("White", white)

    os.chdir(save_dir)

    split_string = inp.split("/", -1)

    substring = split_string[-1]
##    print(substring)
    
    filename = "annotated_" + substring
    white_file = "mask_" + substring
##    print(filename)
    cv2.imwrite(filename, image)
    cv2.imwrite(white_file, white)
      
    cv2.waitKey(0)
    cv2.destroyAllWindows()

##inp = 'C:/Users/maxhb/Pictures/Pictures/Dissertation Photos/Baby black and white.jpg'
##save_dir = 'C:/Users/maxhb/Pictures/Pictures/Dissertation Photos/savedImages'
##
##identify_landmarks(inp, save_dir)
