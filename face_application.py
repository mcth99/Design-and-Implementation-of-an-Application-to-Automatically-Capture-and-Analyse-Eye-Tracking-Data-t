import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
import face_alignment_program as fa
import os
import eye_tracking_study as ets

from matplotlib.figure import Figure

from PIL import ImageTk, Image
import numpy as np
import matplotlib.pyplot as plt
import csv

from win32api import GetSystemMetrics
import glob

#input = 'C:\\Users\\maxhb\\Pictures\\Pictures\\Dissertation Photos\\Images for annotation\\Baby black and white.jpg'

HEADER_FONT = ("Courier", 20)

bw = 60

width_of_screen = GetSystemMetrics(0)
height_of_screen = GetSystemMetrics(1)

class AssessmentTool(tk.Tk):
        
        def __init__(self, *args, **kwargs):

                tk.Tk.__init__(self, *args, **kwargs)

                #Change the app icon here
                tk.Tk.iconbitmap(self, default = "")

                tk.Tk.wm_title(self, "Assessment Tool for Judging the Aesthetic Outcomes of Cleft Lip and Palate Surgery")
                
                container = tk.Frame(self)
                container.pack(side = "top", fill = "both", expand = True)
                container.grid_rowconfigure(0, weight = 1)
                container.columnconfigure(0, weight = 1)

                self.frames = {}

                for F in (StartPage, FaceAlignmentPage, EyeTrackingPage, AnalysisPage):

                        frame = F(container, self)

                        self.frames[F] = frame

                        frame.grid(row = 0, column = 0, sticky = "nsew")

                self.show_frame(StartPage)

        def show_frame(self, cont):

                frame = self.frames[cont]
                frame.tkraise()

class StartPage(tk.Frame):

        def __init__(self, parent, controller):

                tk.Frame.__init__(self, parent)

                title = tk.Label(self, text = "Assessment Tool for Judging the Aesthetic Outcomes of Cleft Lip and Palate Surgery", font = HEADER_FONT)
                title.grid(row = 1, column = 0, columnspan = 4, padx = 10, pady = 10, sticky = "nesw")

                home_page_button = ttk.Button(self, text = "Go to Home Page", width = bw, command = lambda: controller.show_frame(StartPage))
                home_page_button.grid(row = 0, column = 0, sticky = "nesw")

                fa_page_button = ttk.Button(self, text = "Go to Face Annotation Page", width = bw, command = lambda: controller.show_frame(FaceAlignmentPage))
                fa_page_button.grid(row = 0, column = 1, sticky = "nesw")

                et_page_button = ttk.Button(self, text = "Go to Eye Tracking Page", width = bw, command = lambda: controller.show_frame(EyeTrackingPage))
                et_page_button.grid(row = 0, column = 2, sticky = "nesw")

                ap_button = ttk.Button(self, text = "Go to Analysis Page", width = bw, command = lambda: controller.show_frame(AnalysisPage))
                ap_button.grid(row = 0, column = 3, sticky = "nesw")

                #Write an intro
                intro1 = tk.Label(self, text = "Welcome!")
                intro1.grid(row = 5, column = 0, columnspan = 4, sticky = "nesw")
                intro2 = tk.Label(self, text = "This is a tool to provide a standardised assessment of the aesthetic outcomes of cleft lip and palate surgery.")
                intro2.grid(row = 6, column = 0, columnspan = 4, sticky = "nesw")
                intro3 = tk.Label(self, text = "It is able to receive new images and automatically annotate them; record people viewing an image; and display data in a useful manner.")
                intro3.grid(row = 7, column = 0, columnspan = 4, sticky = "nesw")

class FaceAlignmentPage(tk.Frame):

        def __init__(self, parent, controller):

                tk.Frame.__init__(self, parent)

                title = tk.Label(self, text = "Face Annotation Tool", font = HEADER_FONT)
                title.grid(row = 1, column = 0, columnspan = 4, padx = 10, pady = 10, sticky = "nesw")

                home_page_button = ttk.Button(self, text = "Go to Home Page", width = bw, command = lambda: controller.show_frame(StartPage))
                home_page_button.grid(row = 0, column = 0, sticky = "nesw")

                fa_page_button = ttk.Button(self, text = "Go to Face Annotation Page", width = bw, command = lambda: controller.show_frame(FaceAlignmentPage))
                fa_page_button.grid(row = 0, column = 1, sticky = "nesw")

                et_page_button = ttk.Button(self, text = "Go to Eye Tracking Page", width = bw, command = lambda: controller.show_frame(EyeTrackingPage))
                et_page_button.grid(row = 0, column = 2, sticky = "nesw")

                ap_button = ttk.Button(self, text = "Go to Analysis Page", width = bw, command = lambda: controller.show_frame(AnalysisPage))
                ap_button.grid(row = 0, column = 3, sticky = "nesw")

                #The functionality of face alignment

                self.file = tk.StringVar()
                file_btn = ttk.Button(self, text = "Choose image you would like to annotate", command = lambda: self.choose_file(self.file))
                file_btn.grid(row = 2, column = 0, columnspan = 2, sticky = "nesw")

                file_label = tk.Label(self, textvariable = self.file)
                file_label.grid(row = 2, column = 2, columnspan = 2, sticky = "nesw")

                self.save_dir = tk.StringVar()
                file_btn = ttk.Button(self, text = "Choose directory where you would like to save new image", command = lambda: self.browse_files(self.save_dir))
                file_btn.grid(row = 3, column = 0, columnspan = 2, sticky = "nesw")

                dir_label = tk.Label(self, textvariable = self.save_dir)
                dir_label.grid(row = 3, column = 2, columnspan = 2, sticky = "nesw")

                annotate = ttk.Button(self, text="Annotate image", command = lambda: fa.identify_landmarks(self.file.get(), self.save_dir.get()))
                annotate.grid(row = 4, column = 0, columnspan = 4, sticky = "nesw")

        def choose_file(self, file):

                my_file = fd.askopenfilename()
                file.set(my_file)

        def browse_files(self, direct):

                file_dir = fd.askdirectory()
                direct.set(file_dir)

class EyeTrackingPage(tk.Frame):

        def __init__(self, parent, controller):

                tk.Frame.__init__(self, parent)

                title = tk.Label(self, text = "Eye Tracking Tool", font = HEADER_FONT)
                title.grid(row = 1, column = 0, columnspan = 4, padx = 10, pady = 10, sticky = "nesw")

                home_page_button = ttk.Button(self, text = "Go to Home Page", width = bw, command = lambda: controller.show_frame(StartPage))
                home_page_button.grid(row = 0, column = 0, sticky = "nesw")

                fa_page_button = ttk.Button(self, text = "Go to Face Annotation Page", width = bw, command = lambda: controller.show_frame(FaceAlignmentPage))
                fa_page_button.grid(row = 0, column = 1, sticky = "nesw")

                et_page_button = ttk.Button(self, text = "Go to Eye Tracking Page", width = bw, command = lambda: controller.show_frame(EyeTrackingPage))
                et_page_button.grid(row = 0, column = 2, sticky = "nesw")

                ap_button = ttk.Button(self, text = "Go to Analysis Page", width = bw, command = lambda: controller.show_frame(AnalysisPage))
                ap_button.grid(row = 0, column = 3, sticky = "nesw")

                etm_button = ttk.Button(self, text = "Open Eye Tracker Manager to calibrate eye tracker", command = lambda: self.open_app())
                etm_button.grid(row = 2, column = 0, columnspan = 4, sticky = "nesw")

                pid_label = tk.Label(self, text = "Please enter participant ID:")
                pid_label.grid(row = 3, column = 0, columnspan = 2, sticky = "nesw")
                pid_entry = ttk.Entry(self, width = 50)
                pid_entry.grid(row = 3, column = 2, columnspan = 2, sticky = "nesw")

                time_label = tk.Label(self, text = "Please enter time per image in seconds:")
                time_label.grid(row = 4, column = 0, columnspan = 2, sticky = "nesw")
                time_entry = ttk.Entry(self, width = 50)
                time_entry.grid(row = 4, column = 2, columnspan = 2, sticky = "nesw")

                self.img_dir = tk.StringVar()
                img_dir_button = ttk.Button(self, text = "Pick Image Directory", command = lambda: self.browse_files(self.img_dir))
                img_dir_button.grid(row = 5, column = 0, columnspan = 2, sticky = "nesw")
                img_dir_label = tk.Label(self, textvariable = self.img_dir)
                img_dir_label.grid(row = 5, column = 2, columnspan = 2, sticky = "nesw")

                self.save_dir = tk.StringVar()
                save_dir_button = ttk.Button(self, text = "Pick Save Directory", command = lambda: self.browse_files(self.save_dir))
                save_dir_button.grid(row = 6, column = 0, columnspan = 2, sticky = "nesw")
                save_dir_label = tk.Label(self, textvariable = self.save_dir)
                save_dir_label.grid(row = 6, column = 2, columnspan = 2, sticky = "nesw")

                self.mask_dir = tk.StringVar()
                mask_dir_button = ttk.Button(self, text = "Pick Mask Directory", command = lambda: self.browse_files(self.mask_dir))
                mask_dir_button.grid(row = 7, column = 0, columnspan = 2, sticky = "nesw")
                mask_dir_label = tk.Label(self, textvariable = self.mask_dir)
                mask_dir_label.grid(row = 7, column = 2, columnspan = 2, sticky = "nesw")

                study_button = ttk.Button(self, text = "Run Study", command = lambda: ets.study(pid_entry.get(), time_entry.get(), self.img_dir.get(), self.save_dir.get(), self.mask_dir.get()))
                study_button.grid(row = 8, column = 0, columnspan = 4, sticky = "nesw")

        def browse_files(self, direct):

                file_dir = fd.askdirectory()
                direct.set(file_dir)
##                print(self.img_dir.get())
##                print(self.save_dir.get())
##                print(self.mask_dir.get())

        def open_app(self):

                etm = fd.askopenfilename()
                os.system(str(etm))

f = Figure(figsize = (5, 5))
a = f.add_subplot(111)

class AnalysisPage(tk.Frame):

        def __init__(self, parent, controller):

                tk.Frame.__init__(self, parent)

                title = tk.Label(self, text = "Analysis of Eye Tracking Data", font = HEADER_FONT)
                title.grid(row = 1, column = 0, columnspan = 4, padx = 10, pady = 10, sticky = "nesw")

                home_page_button = ttk.Button(self, text = "Go to Home Page", width = bw, command = lambda: controller.show_frame(StartPage))
                home_page_button.grid(row = 0, column = 0, sticky = "nesw")

                fa_page_button = ttk.Button(self, text = "Go to Face Annotation Page", width = bw, command = lambda: controller.show_frame(FaceAlignmentPage))
                fa_page_button.grid(row = 0, column = 1, sticky = "nesw")

                et_page_button = ttk.Button(self, text = "Go to Eye Tracking Page", width = bw, command = lambda: controller.show_frame(EyeTrackingPage))
                et_page_button.grid(row = 0, column = 2, sticky = "nesw")

                ap_button = ttk.Button(self, text = "Go to Analysis Page", width = bw, command = lambda: controller.show_frame(AnalysisPage))
                ap_button.grid(row = 0, column = 3, sticky = "nesw")

                self.file = tk.StringVar()
                file_btn = ttk.Button(self, text = "Choose CSV file you would like to display in a bar graph", command = lambda: [self.choose_file(self.file), self.graph(self.file.get())])
                file_btn.grid(row = 2, column = 1, columnspan = 2, sticky = "nesw")

        def choose_file(self, file):

                my_file = fd.askopenfilename()
                file.set(my_file)

        def graph(self, csv_file):

                landmarks = ["Forehead", "Eyes", "Nose", "Mouth", "Cheeks", "Ears", "Lower Jaw"]
                data_list = []

                with open(csv_file, "r") as the_file:

                        reader = csv.reader(the_file)

                        reader = list(reader)

                        for row in range(1, 25, 1):

                                reader[row][2] = int(reader[row][2])

                        data_list.append(reader[1][2] + reader[2][2])
                        data_list.append(reader[3][2] + reader[4][2] + reader[7][2] + reader[8][2])
                        data_list.append(reader[5][2] + reader[6][2] + reader[9][2] + reader[10][2] + reader[13][2] + reader[14][2])
                        data_list.append(reader[15][2] + reader[16][2] + reader[17][2] + reader[18][2])
                        data_list.append(reader[11][2] + reader[12][2])
                        data_list.append(reader[23][2] + reader[24][2])
                        data_list.append(reader[19][2] + reader[20][2] + reader[21][2] + reader[22][2])

                print(landmarks)
                print(data_list)

                x = np.arange(len(landmarks))
                width = 0.8

                fig, ax = plt.subplots()
                rects1 = ax.bar(x, data_list, width, label = "Landmark")

                ax.set_ylabel("Percentages/%")
                ax.set_title("CSV File Data")
                ax.set_xticks(x)
                ax.set_xticklabels(landmarks)
                ax.legend()

                fig.tight_layout()

                plt.show()

window = AssessmentTool()

window.mainloop()
