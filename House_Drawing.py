# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 23:05:03 2020

Calendar

@author: Родион
"""
import turtle as t
t.hideturtle()

class House:
    def __init__(self,X,Y):
        global X_Main
        X_Main = X
        global Y_Main
        Y_Main = Y
    def First_move(self):
        t.penup()
        t.setpos(X_Main,Y_Main)
        t.pendown()
  
   
class Walls():
    def __init__(self,ww,wh,color="Red"):
        self.X_Walls = X_Main 
        self.Y_Walls = Y_Main
        self.Walls_Width = abs(X_Main)* ww 
        self.Walls_Height = abs(Y_Main)* wh 
        self.Walls_Color = color
        
    def Draw_Walls(self):
        t.fillcolor(self.Walls_Color)
        t.begin_fill()
        t.forward(self.Walls_Width)
        t.left(90)
        t.forward(self.Walls_Height)
        t.left(90)
        t.forward(self.Walls_Width)
        t.end_fill()
        t.penup()
 
        
   
    
X = -200
Y = -200



House_Object = House(X,Y)       
House_Object.First_move()
Walls_Obj = Walls(2,1,color = "Blue")
Walls_Obj.Draw_Walls()


t.done()
 
