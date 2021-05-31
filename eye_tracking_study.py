import tobii_research as tr
import time
import os
##import tkinter as tk
##from tkinter import ttk
##from PIL import ImageTk, Image
import glob
import cv2
from win32api import GetSystemMetrics
import numpy as np
import datetime
import csv
from scipy.spatial import distance

global_gaze_data = ()

width_of_screen = GetSystemMetrics(0)
height_of_screen = GetSystemMetrics(1)

#this method fills a tuple with the gaze data
def gaze_data_callback(gaze_data):

    global global_gaze_data

    left_eye = (gaze_data['left_gaze_point_on_display_area'])
    right_eye = (gaze_data['right_gaze_point_on_display_area'])

    avg_eye_x = (left_eye[0] + right_eye[0])/2
    avg_eye_y = (left_eye[1] + right_eye[1])/2

    x_coord = avg_eye_x*width_of_screen
    y_coord = avg_eye_y*height_of_screen

    eye_data = ((int(x_coord), int(y_coord),),)

    global_gaze_data += eye_data        

#this method displays the slide show of images
def slide_show(time_per_image, image):
    
    white = np.zeros([height_of_screen, width_of_screen, 4], dtype = np.uint8)
    white.fill(255)

    width = image.shape[1]
    height = image.shape[0]

    if (width_of_screen/height_of_screen) <= (width/height):

        ratio = width_of_screen/width

    else:
        
        ratio = height_of_screen/height

    new_width = int(width*ratio)
    new_height = int(height*ratio)

    image = cv2.resize(image, (new_width, new_height))

    x_offset = round((width_of_screen - new_width)/2)
    y_offset = round((height_of_screen - new_height)/2)
    result = white.copy()
    result[y_offset: y_offset + image.shape[0], x_offset: x_offset + image.shape[1]] = image
    
    cv2.namedWindow('screen', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('screen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('screen', result)
    time_per_image = int(time_per_image)
    time_per_image = time_per_image*1000
    cv2.waitKey(time_per_image)
    
#regions is designed to assess what proportion of time is spent looking in each region
def regions(participant_id, img_dir, save_dir, mask_dir, sum_points_dict, num_points_dict):

    global global_gaze_data

    image_name_list = os.listdir(img_dir)
    image_list = []
    hm_image_list = []

    for filename in os.listdir(mask_dir):
        
        img = cv2.imread(os.path.join(mask_dir, filename), cv2.IMREAD_COLOR)
        image_list.append(img)

    for filename in os.listdir(img_dir):
        img = cv2.imread(os.path.join(img_dir, filename))
        hm_image_list.append(img)

    #the following reg_i define the colours of the regions
    reg_1 = (22, 0, 136)
    reg_2 = (38, 127, 255)
    reg_3 = (0, 242, 254)
    reg_4 = (230,191, 199)
    reg_5 = (234, 217, 153)
    reg_6 = (201, 173, 255)
    reg_7 = (87, 122, 185)
    reg_8 = (195, 195, 195)
    reg_9 = (77, 177, 35)
    reg_10 = (163, 73, 163)
    reg_11 = (129, 255, 129)
    reg_12 = (160, 0, 0)
    reg_13 = (13, 201, 255)
    reg_14 = (192, 128, 254)
    reg_15 = (180, 158, 33)
    reg_16 = (255, 127, 128)
    reg_17 = (36, 27, 237)
    reg_18 = (63, 204, 201)
    reg_19 = (0, 106, 213)
    reg_20 = (78, 135, 80)
    reg_21 = (199, 224, 204)
    reg_22 = (195, 194, 228)
    reg_23 = (171, 252, 249)
    reg_24 = (171, 189, 252)

    #pre-defined representative coordinates of regions
    coord_1 = (184, 229)
    coord_2 = (396, 237)
    coord_3 = (140, 388)
    coord_4 = (452, 389)
    coord_5 = (272, 355)
    coord_6 = (304, 352)
    coord_7 = (147, 452)
    coord_8 = (453, 455)
    coord_9 = (267, 415)
    coord_10 = (313, 411)
    coord_11 = (136, 545)
    coord_12 = (452, 546)
    coord_13 = (255, 492)
    coord_14 = (331, 494)
    coord_15 = (251, 575)
    coord_16 = (335, 575)
    coord_17 = (261, 649)
    coord_18 = (334, 655)
    coord_19 = (173, 673)
    coord_20 = (424, 675)
    coord_21 = (261, 728)
    coord_22 = (341, 724)
    coord_23 = (36, 554)
    coord_24 = (563, 552)

##    reg_coords = np.array([coord_1, coord_2, coord_3, coord_4, coord_5, coord_6,
##                           coord_7, coord_8, coord_9, coord_10, coord_11, coord_12,
##                           coord_13, coord_14, coord_15, coord_16, coord_17, coord_18,
##                           coord_19, coord_20, coord_21, coord_22, coord_23, coord_24])
            
    for i in range(len(image_list)):

        reg_coords = np.array([coord_1, coord_2, coord_3, coord_4, coord_5, coord_6,
                           coord_7, coord_8, coord_9, coord_10, coord_11, coord_12,
                           coord_13, coord_14, coord_15, coord_16, coord_17, coord_18,
                           coord_19, coord_20, coord_21, coord_22, coord_23, coord_24])

        #initialise counters
        r1 = 0
        r2 = 0
        r3 = 0
        r4 = 0
        r5 = 0
        r6 = 0
        r7 = 0
        r8 = 0
        r9 = 0
        r10 = 0
        r11 = 0
        r12 = 0
        r13 = 0
        r14 = 0
        r15 = 0
        r16 = 0
        r17 = 0
        r18 = 0
        r19 = 0
        r20 = 0
        r21 = 0
        r22 = 0
        r23 = 0
        r24 = 0
        rgone = 0

        raw_data = []

        hm_image = hm_image_list[i]
        overlay = hm_image.copy()

        hm_width = hm_image.shape[1]
        hm_height = hm_image.shape[0]

        hm_ratio = height_of_screen/hm_height
        
        image = image_list[i]

        width = image.shape[1]
##        print(hm_width)
        height = image.shape[0]

        if (width_of_screen/height_of_screen) <= (hm_width/hm_height):

            hm_ratio = width_of_screen/hm_width

        else:
            
            hm_ratio = height_of_screen/hm_height

        if (width_of_screen/height_of_screen) <= (width/height):

            ratio = width_of_screen/width

        else:
            
            ratio = height_of_screen/height
##        print(ratio)

        new_hm_width = int(hm_width*hm_ratio)
        new_hm_height = int(hm_height*hm_ratio)

        new_width = int(width*ratio)
        new_height = int(height*ratio)

        hm_image = cv2.resize(hm_image, (new_hm_width, new_hm_height))
        overlay = cv2.resize(overlay, (new_hm_width, new_hm_height))

        image = cv2.resize(image, (new_width, new_height))

        def draw_hm(x_coord, y_coord, colour, hm_image, overlay):

            cv2.circle(hm_image, (x_coord, y_coord), 10, colour, -1)

            alpha = 0.2

            hm_image = cv2.addWeighted(overlay, alpha, hm_image, 1 - alpha, 0)

        for j in range(sum_points_dict[i], sum_points_dict[i+1], 1):

            if global_gaze_data[j][0] >= ((width_of_screen/2) + (new_width/2)):

                rgone = rgone + 1

                continue

            elif global_gaze_data[j][0] <= ((width_of_screen/2) - (new_width/2)):

                rgone = rgone + 1

                continue

            elif global_gaze_data[j][1] >= ((height_of_screen/2) + (new_height/2)):

                rgone = rgone + 1

                continue

            elif global_gaze_data[j][1] <= ((height_of_screen/2) - (new_height/2)):

                rgone = rgone + 1

                continue

            else:

                #this line below means the dots are drawn in the correct horizontal position
                x_coord = global_gaze_data[j][0] - ((width_of_screen/2) - (new_width/2))
                hm_x_coord = global_gaze_data[j][0] - ((width_of_screen/2) - (new_hm_width/2))

                y_coord = global_gaze_data[j][1] - ((height_of_screen/2) - (new_height/2))
                hm_y_coord = global_gaze_data[j][1] - ((height_of_screen/2) - (new_hm_height/2))
                
                x_coord = int(x_coord)
                hm_x_coord = int(hm_x_coord)
                y_coord = int(y_coord)
                hm_y_coord = int(hm_y_coord)

                raw_data += [(int(x_coord*(1/hm_ratio)), int(y_coord*(1/hm_ratio)))]

                coords = image[y_coord, x_coord]
                coords = (coords[0], coords[1], coords[2])
##                print(coords)
##                coords_plus = (coords[0]+5, coords[1]+5, coords[2]+5)
##                coords_minus = (coords[0]-5, coords[1]-5, coords[2]-5)

                colour = (0, 0, 255)

                if reg_1 == coords:
                    draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                    r1 = r1 + 1

                elif reg_2 == coords:
                    draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                    r2 = r2 + 1

                elif reg_3 == coords:
                    draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                    r3 = r3 + 1

                elif reg_4 == coords:
                    draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                    r4 = r4 + 1

                elif reg_5 == coords:
                    draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                    r5 = r5 + 1

                elif reg_6 == coords:
                    draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                    r6 = r6 + 1

                elif reg_7 == coords:
                    draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                    r7 = r7 + 1

                elif reg_8 == coords:
                    draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                    r8 = r8 + 1

                elif reg_9 == coords:
                    draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                    r9 = r9 + 1

                elif reg_10 == coords:
                    draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                    r10 = r10 + 1

                elif reg_11 == coords:
                    draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                    r11 = r11 + 1

                elif reg_12 == coords:
                    draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                    r12 = r12 + 1

                elif reg_13 == coords:
                    draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                    r13 = r13 + 1

                elif reg_14 == coords:
                    draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                    r14 = r14 + 1

                elif reg_15 == coords:
                    draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                    r15 = r15 + 1

                elif reg_16 == coords:
                    draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                    r16 = r16 + 1

                elif reg_17 == coords:
                    draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                    r17 = r17 + 1

                elif reg_18 == coords:
                    draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                    r18 = r18 + 1

                elif reg_19 == coords:
                    draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                    r19 = r19 + 1

                elif reg_20 == coords:
                    draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                    r20 = r20 + 1

                elif reg_21 == coords:
                    draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                    r21 = r21 + 1

                elif reg_22 == coords:
                    draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                    r22 = r22 + 1

                elif reg_23 == coords:
                    draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                    r23 = r23 + 1

                elif reg_24 == coords:
                    draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                    r24 = r24 + 1

                else:

                    np_coord = np.array([(x_coord, y_coord)])
                    min_dist = distance.cdist(reg_coords, np_coord)
                    shortest = np.where(min_dist == np.min(distance.cdist(reg_coords, np_coord)))
                    s_index = shortest[0][0]

                    colour = (255, 0, 0)

                    if s_index == 0:
                        draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                        r1 = r1 + 1

                    elif s_index == 1:
                        draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                        r2 = r2 + 1

                    elif s_index == 2:
                        draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                        r3 = r3 + 1

                    elif s_index == 3:
                        draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                        r4 = r4 + 1

                    elif s_index == 4:
                        draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                        r5 = r5 + 1

                    elif s_index == 5:
                        draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                        r6 = r6 + 1

                    elif s_index == 6:
                        draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                        r7 = r7 + 1

                    elif s_index == 7:
                        draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                        r8 = r8 + 1

                    elif s_index == 8:
                        draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                        r9 = r9 + 1

                    elif s_index == 9:
                        draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                        r10 = r10 + 1

                    elif s_index == 10:
                        draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                        r11 = r11 + 1

                    elif s_index == 11:
                        draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                        r12 = r12 + 1

                    elif s_index == 12:
                        draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                        r13 = r13 + 1

                    elif s_index == 13:
                        draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                        r14 = r14 + 1

                    elif s_index == 14:
                        draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                        r15 = r15 + 1

                    elif s_index == 15:
                        draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                        r16 = r16 + 1

                    elif s_index == 16:
                        draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                        r17 = r17 + 1

                    elif s_index == 17:
                        draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                        r18 = r18 + 1

                    elif s_index == 18:
                        draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                        r19 = r19 + 1

                    elif s_index == 19:
                        draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                        r20 = r20 + 1

                    elif s_index == 20:
                        draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                        r21 = r21 + 1

                    elif s_index == 21:
                        draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                        r22 = r22 + 1

                    elif s_index == 22:
                        draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                        r23 = r23 + 1

                    elif s_index == 23:
                        draw_hm(hm_x_coord, hm_y_coord, colour, hm_image, overlay)
                        r24 = r24 + 1

##        print(rgone)
        if rgone == num_points_dict[i]:

            per = 1

        else:

            per = num_points_dict[i] - rgone
            
##        print(per)
        percent_per_region = [["Region 1", r1, int((r1/per)*100)], ["Region 2", r2, int((r2/per)*100)],
                              ["Region 3", r3, int((r3/per)*100)], ["Region 4", r4, int((r4/per)*100)],
                              ["Region 5", r5, int((r5/per)*100)], ["Region 6", r6, int((r6/per)*100)],
                              ["Region 7", r7, int((r7/per)*100)], ["Region 8", r8, int((r8/per)*100)],
                              ["Region 9", r9, int((r9/per)*100)], ["Region 10", r10, int((r10/per)*100)],
                              ["Region 11", r11, int((r11/per)*100)], ["Region 12", r12, int((r12/per)*100)],
                              ["Region 13", r13, int((r13/per)*100)], ["Region 14", r14, int((r14/per)*100)],
                              ["Region 15", r15, int((r15/per)*100)], ["Region 16", r16, int((r16/per)*100)],
                              ["Region 17", r17, int((r17/per)*100)], ["Region 18", r18, int((r18/per)*100)],
                              ["Region 19", r19, int((r19/per)*100)], ["Region 20", r20, int((r20/per)*100)],
                              ["Region 21", r21, int((r21/per)*100)], ["Region 22", r22, int((r22/per)*100)],
                              ["Region 23", r23, int((r23/per)*100)], ["Region 24", r24, int((r24/per)*100)]]

        dt = datetime.datetime.now().strftime("%Y" + "%m" + "%d" + "%H" + "%M" + "%S" + "%f")
        os.chdir(save_dir)

##        print(raw_data)

        img_name = image_name_list[i]
        img_name = img_name.replace(".", "")

        with open("study_data_" + img_name + "_" + participant_id + "_" + dt + ".csv", "w", newline = "") as csvfile:

            writer = csv.writer(csvfile)
            writer.writerow(["Region", "Number of gaze points", "Percentage of gaze points", "Paticipant ID: " + participant_id, "Image: " + image_name_list[i]])
            
            for k in range(len(percent_per_region)):
                
                writer.writerow(percent_per_region[k])

##            writer.writerow(raw_data_x)
##            writer.writerow(raw_data_y)

            writer.writerow(["x coordinates", "y coordinates"])
            for xy in range(len(raw_data)):

                writer.writerow(raw_data[xy])

        hm_image = cv2.resize(hm_image, (hm_width, hm_height))
        filename = participant_id + "_" + dt + "_mask_" + image_name_list[i]
        cv2.imwrite(filename, hm_image)
     
def study(participant_id, time_per_image, img_dir, save_dir, mask_dir):

    global global_gaze_data
        
    #The next two lines of code are what should be in the final program.
    found_eyetrackers = tr.find_all_eyetrackers()
    eyetracker = found_eyetrackers[0]

##    #The line of code below should be removed in the final program.
##    eyetracker = tr.EyeTracker('tet-tcp://172.28.195.1')

    image_list = []
    sum_points_dict = {0:0}
    num_points_dict = {}

    for filename in os.listdir(img_dir):
        
        img = cv2.imread(os.path.join(img_dir, filename))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        image_list.append(img)
    
    eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

    for i in range(len(image_list)):

        slide_show(time_per_image, image_list[i])

        #The following line identifies how many points per image were recorded
        sum_points_dict[i+1] = len(global_gaze_data)
        num_points_dict[i] = len(global_gaze_data) - sum(num_points_dict.values())

    eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)

    cv2.destroyAllWindows()

##    print("Gaze data received:")
##    print(global_gaze_data)
##    print(sum_points_dict)
##    print(num_points_dict)

    regions(participant_id, img_dir, save_dir, mask_dir, sum_points_dict, num_points_dict)

##study("180180765", 5, "C:/Users/maxhb/Pictures/Pictures/Dissertation Photos/Images for annotation", "C:/Users/maxhb/Pictures/Pictures/Dissertation Photos/savedImages", "C:/Users/maxhb/Pictures/Pictures/Dissertation Photos/colouredMaskImages")
