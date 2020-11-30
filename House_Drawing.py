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

class Geometry_Draw:
    
    def Draw_Rectangle(self,X_0,Y_0,W,H,color):
        t.setposition(X_0, Y_0)
        t.pendown()
        t.fillcolor(color)
        t.begin_fill()
        t.forward(W)
        t.left(90)
        t.forward(H)
        t.left(90)
        t.forward(W)
        t.left(90)
        t.forward(H)
        t.left(90)
        t.end_fill()
        t.penup()
        
    def Draw_Triangle(self,X_0,Y_0,base_lengh,H,color):
        t.fillcolor(color) 
        t.setposition(X_0,Y_0)
        t.begin_fill()
        t.pendown()
        t.forward(base_lengh)
        t.setposition(X_0 +base_lengh/2,Y_0 + H)
        t.setposition(X_0,Y_0)
        t.end_fill()
        t.penup()
               
class Foundation(Geometry_Draw):
    X_Found = 0
    Y_Found = 0
    Found_Width  = 0
    Found_Height = 0
    Found_Color = "Black"
    def Set_Found(self,w,h,color = "Black"):
        
        Foundation.Found_Width = w 
        Foundation.Found_Height =  h 
        Foundation.Found_Color = color
        Foundation.X_Found = House.X_Main -  Foundation.Found_Width*0.1  
        Foundation.Y_Found = House.Y_Main -  Foundation.Found_Height
    
    def Draw_Founation(self):
        Foundation.Draw_Rectangle(self,Foundation.X_Found, Foundation.Y_Found, 
                              Foundation.Found_Width, Foundation.Found_Height,
                              Foundation.Found_Color)
        
class Walls(Geometry_Draw):
    Walls_Width  = 0
    Walls_Height = 0
    Walls_Color = "Red"
    
    def Set_Walls(self,color="Red"): 
        Walls.Walls_Color = color
        Walls.Walls_Width  = Foundation.Found_Width * 0.8
        Walls.Walls_Height = Foundation.Found_Height * 15
       

    def change_walls_color(self,new_color):
        Walls.Set_Walls(self,color = new_color)
        Walls.Draw_Walls(self)
    def Draw_Walls(self):
        Walls.Draw_Rectangle(self,House.X_Main,House.Y_Main,
                         Walls.Walls_Width,Walls.Walls_Height,
                         Walls.Walls_Color)
    
class Roof(Geometry_Draw):
    
    Roof_Color = "Red"
    Roof_Width = 0
    Roof_Hieght = 0
    X_Roof = 0
    Y_Roof = 0
    def Set_Roof(self,color = "Red"):
        Roof.Roof_Color = color
        Roof.Roof_Width = Walls.Walls_Width * 1.2
        Roof.Roof_Hieght = Walls.Walls_Height*0.3
        Roof.X_Roof = House.X_Main + Walls.Walls_Width/2 -Roof.Roof_Width/2
        Roof.Y_Roof = Walls.Walls_Height + House.Y_Main
        
    
    def Ch_Rf_Clr(self,new_color):
       Roof.Set_Roof(self,color = new_color)
       Roof.Draw_Roof(self)
    def Draw_Roof(self):
        Roof.Draw_Triangle(self,Roof.X_Roof,Roof.Y_Roof,Roof.Roof_Width,Roof.Roof_Hieght,Roof.Roof_Color)

class Door(Geometry_Draw):
    Door_Color = "Brown"
    Door_Width = 0
    Door_Height = 0
    Door_X = 0
    
    def Set_Door(self,Door_location,color="Brown"):
        Door.Door_Color = color
        Door.Door_X = House.X_Main + Door_location
        Door.Door_Width = Walls.Walls_Width * 0.15
        Door.Door_Height = Walls.Walls_Height * 0.8
    def Draw_Door(self):
        Door.Draw_Rectangle(self, Door.Door_X, House.Y_Main, 
                            Door.Door_Width, Door.Door_Height, 
                            Door.Door_Color)


X = -200
Y = -100

House_Object = House()
House_Object.Locate(X,Y)       
House_Object.First_move()

Foundation_Obj = Foundation()
Foundation_Obj.Set_Found(400, 15,color = "Black")
Foundation_Obj.Draw_Founation()


Walls_Obj = Walls()
Walls_Obj.Set_Walls(color = "Green")
Walls_Obj.Draw_Walls()

Door_Obj = Door()
Door_Obj.Set_Door(30,color = "Blue")
Door_Obj.Draw_Door()

Roof_Obj = Roof()
Roof_Obj.Set_Roof(color = "Green")
Roof_Obj.Draw_Roof()


while True:
    ans = input("Поменять цвет стен? Yes/No : ")
    if ans == "Yes":
        color = input("Введите новый цвет: ")
        Walls_Obj.change_walls_color(color)
    if ans == "No":
        break


while True:
    ans = input("Поменять цвет крыши? Yes/No : ")
    if ans == "Yes":
        color = input("Введите новый цвет: ")
        Roof_Obj.Ch_Rf_Clr(color)
    if ans == "No":
        break
 
t.done()

