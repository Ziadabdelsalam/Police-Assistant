import time
from tkinter import *
import tkinter
import PIL
from tkvideo import tkvideo as tkv
from PIL import ImageTk, Image
from RUN import *
from Get_Plate_Characters import *
import os

Accident = 0
counter = 0
main_window = Tk()
main_window.attributes('-fullscreen', True)
main_window.title("Robot Control")
main_window.configure(background='white')

w = Canvas(main_window, width=1920, height=40, borderwidth=0)
w.create_rectangle(0, 0, 1920, 40, fill="blue", outline='blue', width=0)
w.place(x=0, y=0)

video_label = Label(main_window)
video_label.place(x=0, y=40)
player = tkv("Object Detection.mp4", video_label, loop=1, size=(500, 500))
player.play()

#Add Non Masked Images
'''label = Label(main_window, text="Non Masked Face", bg="white", width=70, height=0)
label.place(x=1060, y=40)
img1 = Image.open("zeze.jpeg")
img1 = img1.resize((400,200), Image.ANTIALIAS)
photoImg1 = ImageTk.PhotoImage(img1)
panel = Label(main_window, image=photoImg1)
panel.place(x=1100, y=60)'''

#Add Criminals Images
'''label = Label(main_window, text="Criminals Faces", bg="white", width=70, height=0)
label.place(x=1060, y=260)
img2 = Image.open("hos.jpeg")
img2 = img2.resize((400,200), Image.ANTIALIAS)
photoImg2 = ImageTk.PhotoImage(img2)
panel = Label(main_window, image=photoImg2)
panel.place(x=1100, y=280)'''


#Add Plates Images
label = Label(main_window, text="Stolen Plates", bg="white", width=70, height=0)
label.place(x=1060, y=480)
#img3 = Image.open("plate.jpeg")
#img3 = img3.resize((400,200), Image.ANTIALIAS)
#image = image.resize((400,200), Image.ANTIALIAS)
#photoImg3 = ImageTk.PhotoImage(image)
photoImg3 = ImageTk.PhotoImage(image=PIL.Image.fromarray(image))  #image is the variable extracted from run script
panel = Label(main_window, image=photoImg3)
panel.place(x=1100, y=500)

#list boc of plates
panel = Label(main_window, text="Plates Detected")
panel.place(x=900, y=600)
listbox = tkinter.Listbox(panel)
for i in range(len(Plates_detected)):
    listbox.insert(0, Plates_detected[i])
listbox.pack()

#list boc of plates
panel = Label(main_window, text="Stolen Plates")
panel.place(x=900, y=200)
listbox = tkinter.Listbox(panel)
for i in range(len(Stolen_Plates_detected)):
    listbox.insert(0, Stolen_Plates_detected[i])
listbox.pack()



#Add Fire State
Fire_State = False
label1 = Label(main_window, text="Fire Status: " + str(Fire_State), bg="white", width=25, height=0, font=("Arial", 15))
label1.place(x=1050, y=730)

#Add Accident State
Accident_State = False
label = Label(main_window, text="Accident Status: " + str(Accident_State), bg="white", width=25, height=0, font=("Arial", 15))
label.place(x=1070, y=780)

def task():
    Accident_State = change()
    label1['text'] = "Fire Status: " + str(Accident_State)
    main_window.after(2000, task)  # reschedule event in 2 seconds

def change():
	Accident_State = True
	return Accident_State

main_window.after(2000, task)

main_window.mainloop()