import cv2
import numpy as np
import pandas as pd
import argparse
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import ttk

#Creating argument parser to take image path from command line
#ap = argparse.ArgumentParser()
#ap.add_argument('-i', '--image', required=True, help="Image Path")
#args = vars(ap.parse_args())
#img_path = args['image']

fwin = tk.Tk()
fwin.configure(background="medium orchid")
fwin.title("Color Detector")
fwin.geometry("1000x600")

color_img = Image.open("color_text.png")
photo = ImageTk.PhotoImage(color_img)

color_label = tk.Label(fwin, image=photo).place(x=80, y=100)

def browseFiles():
	filename = filedialog.askopenfilename(initialdir = "/",
										title = "Select a File",
										filetypes = (("JPG","*.jpg"),("JPEG","*.jpeg"),("PNG","*.png"),
													("All Files",
														"*.*")))
	
	# Change label contents
	pathy.set(filename)

def goon():
    fwin.destroy()

btn = tk.Button(fwin,  text="  browse  ", command=browseFiles).place(x=480, y=500)
btn = tk.Button(fwin,  text="  Detect  ", command=goon).place(x=550, y=500)


pathy = tk.StringVar()
pathEntry = ttk.Entry(fwin, width = 50, textvariable = pathy).place(x=160, y=502)

fwin.mainloop()

img_path = pathy.get()
#Reading the image with opencv
img = cv2.imread(img_path)

#declaring global variables (are used later on)
clicked = False
r = g = b = xpos = ypos = 0

#function to calculate minimum distance from all colors and get the most matching color
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

#function to get x,y coordinates of mouse double click
def draw_function(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

#Reading csv file with pandas and giving names to each column
index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('colors.csv', names=index, header=None)
       
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_function)

while(1):

    cv2.imshow("image",img)
    if (clicked):
   
        #cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle 
        cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)

        #Creating text string to display( Color name and RGB values )
        text = getColorName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
        
        #cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)

        #For very light colours we will display text in black colour
        if(r+g+b>=600):
            cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
            
        clicked=False

    #Break the loop when user hits 'esc' key    
    if cv2.waitKey(20) & 0xFF ==27:
        break

cv2.destroyAllWindows()