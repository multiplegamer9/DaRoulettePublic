import tkinter as tk
from tkinter import *
import turtle
import math
import random
from typing import Dict, List
import time
from spinning_wheel_slices import  rotate_image,WheelItem1,WheelItem2,WheelItem3,WheelItem4,WheelItem5,WheelItem6,WheelItem7,WheelItem8,WheelItem9,WheelItem10,WheelItem11,WheelItem12
import asyncio
from PIL import ImageTk,Image
import json

class Spinning_Wheel(tk.Canvas):

    def __init__(self, parent, radius, items: Dict[str, float], **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        
        self.radius: float = radius  
        self.items: List[WheelItem] = items
        self.screen = turtle.TurtleScreen(self)
        self.pen = turtle.RawTurtle(self.screen)
        self.pen.hideturtle()

        self.radius = 200
        self.screen.delay(0)
        self.screen.tracer(0, 0)
        self.screen.bgcolor('green')

        self.canvas_text_ids = [self.create_text(0, 0) for _ in items]
        self.canvas_text_bg_ids = [self.create_text(0, 0) for _ in items]
        self.canvas_text_bg_ids2 = [self.create_text(0, 0) for _ in items]
        # indicates which item will be chosen
        triangle = round(self.radius / 10)
        triangle_points = [self.radius, 0, self.radius+triangle, triangle, self.radius+triangle, -triangle]
        self.tick_mark = self.create_polygon(triangle_points, fill='white')

        # text which will display the result of the spin (which item the wheel lands on)
        #self.result_text_bg = self.create_text(2, radius+50+2, fill='black', font=("Arial", 20, "bold"))
        resulttextsize = round(self.radius / 10)
        resulttextcenter = round(self.radius / 4)
        self.result_text = self.create_text(0, radius+resulttextcenter, fill='black', font=("Impact", resulttextsize, "bold"))
        self.result_bg = self.create_rectangle(0, 0, 0,0, fill="white", outline = 'white')
        self.coords(self.result_bg, -40,100,-41,101)
        self.move(self.result_bg,-90,230)
        self.tag_raise(self.result_text)
        imgsize = round(self.radius * 2.3)
        # make sure the wheel cannot be spinning two times at once
        self.img2 = Image.open('ball.png').resize((imgsize,imgsize), Image.BILINEAR) #(Image.open("ball.png"))
        self.img= ImageTk.PhotoImage(self.img2)
        self.new_image= self.create_image(0,0,image=self.img,anchor="center")#ImageTk.PhotoImage(resized_image)
        self.tag_raise(self.new_image)
        #self.move(self.new_image,240,230)
        
        self.is_spinning = False

    def calc_spin_loc(self, init_vel, time, friction=0) -> float:
        """
        Calculate the current spin position of the wheel (in degrees) with respect to initial velocity, time, and a friction constant
        """
        final_time = init_vel/friction
        if time >= final_time:
            time = final_time
        position = init_vel * time - (friction * (time**2))/2

        return position

    def calc_spin_vel(self, init_vel, time, friction=0) -> float:
        """
        Calculate the current velocity of the spinning wheel
        """
        result = init_vel - friction * time
        
        if result <= 0:
            result = 0
        return result

    def draw(self, offset=0, origin=(0, 0)):
        """
        Draw a pie with the specified items

        pen: turtle object
        radius: radius of the circle
        items: Dictionary of sections of a pie. These values must sum to 1.
        offset: number of degrees to offset the pie by
        """

        self.pen.reset()
        self.pen.ht()
        self.pen.up()
        self.pen.sety(-self.radius)
        self.pen.down()

        current_angle = offset

        # draw the pie
        self.pen.circle(self.radius, offset+90)  # offset the circle by a certain amount. Allows for the entire circle to have a spinning animation
        for i, item in enumerate(self.items):
            # draw a section of the pie
            self.pen.fillcolor(item.color)
            self.pen.begin_fill()
            self.pen.circle(self.radius, item.size)
            position = self.pen.position()
            self.pen.goto(0, 0)
            self.pen.end_fill()

            # draw the label for the current section of the circle
            label_angle = (current_angle+(item.size/2)) % 360
            #print(label_angle)
            x_pos = 0.5*self.radius*math.cos(math.radians(label_angle))
            y_pos = 0.5*self.radius*math.sin(math.radians(label_angle))
            #self.itemconfig(self.canvas_text_ids[i], angle=label_angle, text=item.label, font=("Arial", 10, "normal"), fill='white')
            
            fontsize = round(self.radius / 11.111111111111)
            #self.itemconfig(self.canvas_text_bg_ids[i], angle=label_angle, text=item.label, font=("Arial", 10, "normal"), fill='black')
            self.itemconfig(self.canvas_text_ids[i], angle=label_angle, text=item.label, font=("Burbank Big Cd Bk", fontsize, "normal"), fill='white')
            #self.itemconfig(self.canvas_text_bg_ids[i], angle=label_angle, text=item.label, font=("Burbank Big Cd Bk", 19, "normal"), fill='black')
            #self.itemconfig(self.canvas_text_bg_ids2[i], angle=label_angle, text=item.label, font=("Burbank Big Cd Bk", 19, "normal"), fill='black')
            self.coords(self.canvas_text_ids[i], x_pos, -y_pos)
            #self.coords(self.canvas_text_bg_ids[i], x_pos-0.5, -(y_pos-0.5))
            #self.coords(self.canvas_text_bg_ids2[i], x_pos+0.9, -(y_pos+0.9))


            self.pen.setposition(position)

            current_angle += item.size

        # raise all labels
        for i, item in enumerate(self.items):
            self.tag_raise(self.canvas_text_bg_ids[i])
            self.tag_raise(self.canvas_text_bg_ids2[i])
            self.tag_raise(self.canvas_text_ids[i])

        # draw the tick mark
        self.tag_raise(self.tick_mark)

    def spin(self, init_vel=None, friction=120):
        """ 
        Spin the wheel by rotating all items by a certain angle determined by the calc_spin_loc() function
        init_vel: Initial velocity to spin the wheel at
        
        friction: how much friction to have while spinning
        """
        if not self.is_spinning:
            if not init_vel:
                init_vel = random.randint(500, 1300)
                print(init_vel)
            result_item_empty = ""    
            self.itemconfig(self.result_text, text=result_item_empty)
            self.coords(self.result_bg, 10000,40000,10101,30000)
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
                self.rotated_photo = rotate_image(self.img2, offset)
                self.itemconfigure(self.new_image, image=self.rotated_photo)
                self.draw(current_pos)
                time.sleep(0.0016)
                self.screen.update()

            self.is_spinning = False

            # find which item the wheel landed on
            result_item = ""
            result_item_empty = ""
            result_bg_size = 180, 400
            result_item_angle = 0
            choice_position = 360-current_pos
            for item in self.items:
                if result_item_angle <= choice_position < result_item_angle+item.size:
                    result_item = item.label
                    print(result_item_angle, result_item_angle+item.size)
                    break
                else:
                    result_item_angle += item.size
            resultbgx1 = -abs(round(self.radius / 2.5))
            resultbgy1 = round(self.radius * 1.325)
            self.itemconfig(self.result_text, text=result_item)
            resultbgx2 = round(self.radius / 2.5)
            resultbgy2 = round(self.radius * 1.175)
            resulttextsexo = round(self.radius / 2.5)
            resulttextsexo2 = round(self.radius / 15)
            self.coords(self.result_bg, resultbgx1,resultbgy1,resultbgx2,resultbgy2)
            self.coords(self.result_text, resultbgx1+ resulttextsexo,resultbgy1- resulttextsexo2)
            CONFIG_FILE = "config.json"
            with open(CONFIG_FILE, "r") as configur:
                data = json.load(configur)
            data["latestprize"] = f"{result_item}"
            data["lastvel"] = f"{init_vel}"
            with open(CONFIG_FILE, 'w') as configur:
                json.dump(data, configur,indent=4)
            with open(CONFIG_FILE, "r") as configur:
             data = json.load(configur)
            data["wheelspun"] = "True"
            with open(CONFIG_FILE,"w") as configur:
                json.dump(data, configur, indent=4)


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
        self.size: float = portion*180
        self.color: str = "#ffffff"

