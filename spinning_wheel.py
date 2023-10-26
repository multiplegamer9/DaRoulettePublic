from tkinter import *
import tkinter as tk
import threading
import time
from spinning_wheel_objs import Spinning_Wheel, WheelItem, __init__
from spinning_wheel_slices import WheelItem1,WheelItem2,WheelItem3,WheelItem4,WheelItem5,WheelItem6,WheelItem7,WheelItem8,WheelItem9,WheelItem10,WheelItem11,WheelItem12
from PIL import ImageTk,Image
import json
root = tk.Tk()
width = 600
height = 600
root.geometry('{}x{}'.format(width, height))
root.title("Roulette 1.5.1")
root.configure(background='green')



pie_items = [
        WheelItem1,
        WheelItem2,
        WheelItem3,
        WheelItem4,
        WheelItem5,
        WheelItem6,
        WheelItem7,
        WheelItem8,
        WheelItem9,
        WheelItem10,
        WheelItem11,
        WheelItem12,
    ]


canvas_frame = tk.Frame(root)
wheel = Spinning_Wheel(canvas_frame, 200, pie_items, width=str(width), height=str(height-100))
wheel.pack(padx=0, pady=0, side="top", fill="both", expand=True)
canvas_frame.pack(side="top", padx=0, pady=5, fill="both", expand=True)

WheelItem1.color = '#9146FF' 
WheelItem2.color = ''#ffffff'#178de8 
WheelItem3.color = ''#c41212 
WheelItem4.color = ''#ffffff
WheelItem5.color = '#ff00f7' 
WheelItem6.color = ''#ffffff 
WheelItem7.color = ''#c41212 
WheelItem8.color = ''#ffffff
WheelItem9.color = '#1dA1f2'#e8e802  
WheelItem10.color = ''#ffffff 
WheelItem11.color = ''#c41212 
WheelItem12.color = ''#ffffff

# frame for user controls
user_controls = tk.Frame(root)
user_controls.configure(background='green')
spin_button = tk.Button(user_controls, text="spin", command=wheel.spin)
spin_button.pack()
user_controls.pack(side='top')
wheel.draw(offset=0)

print("loaded")
CONFIG_FILE = "config.json"

while True:
  #code
  with open(CONFIG_FILE, "r") as configur:
   data = json.load(configur)
  time.sleep(.1)  
  if data["wheelspun"] == "False":
    print("spun")
    wheel.spin()


  root.update()
  root.update_idletasks()
