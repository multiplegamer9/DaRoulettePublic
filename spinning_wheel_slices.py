import random
import time
import math
import tkinter as tk
from PIL import Image, ImageTk


WheelHasSpun = False
class WheelItem:
    def __init__(self, label: str, portion, color=None):
        """
        Store various information about a portion of a spinning wheel

        label: Name for the given spinning wheel item. This will be displayed on the wheel as it spins
        portion: A fraction out of 1 of how much of the wheel this portion will take up
        size: how many degrees out of 360 this portion will take up of the wheel
        color: hex color code. This will default to a random value
        """
        self.label: str = label
        self.portion: float = portion
        self.size: float = portion*360
        self.color_int = random.randint(0, 256**3-1)
        
        self.color: str = ''#random.choice(tuple(self.color_int))
    
        #self.color: str = '#%06X' % self.color_int if color is None else color
    def spin(self, init_vel=None, friction=150):
        """
        Spin the wheel by rotating all items by a certain angle determined by the calc_spin_loc() function

        init_vel: Initial velocity to spin the wheel at
        friction: how much friction to have while spinning
        """
        if not self.is_spinning:
            if not init_vel:
                init_vel = random.randint(600, 1300)
                print(init_vel)

            offset = 0
            vel = init_vel
            start_time = time.perf_counter()
            current_time = 0

            self.is_spinning = True
            while vel > 0:
                current_time = time.perf_counter()
                offset = self.calc_spin_loc(init_vel, current_time-start_time, friction)
                vel = self.calc_spin_vel(init_vel, current_time-start_time, friction)

                current_pos = offset % 360
                self.draw(current_pos)
                time.sleep(0.01)
                self.screen.update()

            self.is_spinning = False

            # find which item the wheel landed on
            result_item = ""
            result_item_angle = 0
            choice_position = 360-current_pos
            for item in self.items:
                if result_item_angle <= choice_position < result_item_angle+item.size:
                    result_item = item.label
                    print(result_item_angle, result_item_angle+item.size)
                    break
                else:
                    result_item_angle += item.size

            self.itemconfig(self.result_text, text=result_item)
            print(result_item)
            #   self.itemconfig(self.result_text_bg, text=result_item)

WheelItem1 = WheelItem("SUB", 3/48)
WheelItem2 = WheelItem("3 MINUTE TO", 4/48)
WheelItem3 = WheelItem("5 MINUTE TO", 5/48)
WheelItem4 = WheelItem("3 MINUTE TO", 4/48)
WheelItem5 = WheelItem("VIP", 3/48)
WheelItem6 = WheelItem("3 MINUTE TO", 4/48)
WheelItem7 = WheelItem("5 MINUTE TO", 5/48)
WheelItem8 = WheelItem("3 MINUTE TO", 4/48)
WheelItem9 = WheelItem("EMOTE", 3/48)
WheelItem10 = WheelItem("3 MINUTE TO", 4/48)
WheelItem11 = WheelItem("5 MINUTE TO", 5/48)
WheelItem12 = WheelItem("3 MINUTE TO", 4/48)

def rotate_image(image, angle):
    rotated_image = image.rotate(angle)
    return ImageTk.PhotoImage(rotated_image)