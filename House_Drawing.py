# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 23:05:03 2020

Calendar

@author: Родион
"""

import turtle as t
t.hideturtle()
t.speed(10)
class House:
    X_Main = 0
    Y_Main = 0
    def Locate(self,X,Y):
        House.X_Main = X
        House.Y_Main = Y
    
    def First_move(self):
        t.penup()
        t.setpos(House.X_Main,House.Y_Main)
        
        
  
   
class Walls:
    Walls_Width  = 0
    Walls_Height = 0
    
    Walls_Color = "Red"
    def Set_Walls(self,w,h,color="Red"): 
        Walls.Walls_Color = color
        X_Walls = House.X_Main
        Y_Walls = House.Y_Main
        Walls.Walls_Width  = abs(X_Walls) * w 
        Walls.Walls_Height = abs(Y_Walls) * h  
        
    def Draw_Walls(self):
        t.pendown()
        t.fillcolor(Walls.Walls_Color)
        t.begin_fill()
        t.forward(Walls.Walls_Width)
        t.left(90)
        t.forward(Walls.Walls_Height)
        t.left(90)
        t.forward(Walls.Walls_Width)
        t.left(90)
        t.forward(Walls.Walls_Height)
        t.left(90)
        t.end_fill()
        t.penup()

class Roof:
    def __init__(self,color="Red"):
        self.Roof_Width = Walls.Walls_Width * 1.2
        self.Roof_Hieght = Walls.Walls_Height*0.5
        self.X_Roof = House.X_Main + Walls.Walls_Width/2 -self.Roof_Width/2
        self.Y_Roof = Walls.Walls_Height + House.Y_Main
        
        self.Roof_Color = color
    def Draw_Roof(self):
        
        t.fillcolor(self.Roof_Color) 
        t.setposition(self.X_Roof,self.Y_Roof)
        t.begin_fill()
        t.pendown()
        t.forward(self.Roof_Width)
        t.setposition(self.X_Roof + self.Roof_Width/2,self.Y_Roof + self.Roof_Hieght)
        t.setposition(self.X_Roof,self.Y_Roof)
        t.end_fill()
        t.penup()
        
   
    
X = -100
Y = -200



House_Object = House()
House_Object.Locate(X,Y)       
House_Object.First_move()

Walls_Obj = Walls()


Walls_Obj.Set_Walls(3,1,color = "Green")
Walls_Obj.Draw_Walls()

Roof_Obj = Roof()

Roof_Obj.Draw_Roof()

t.done()
 
