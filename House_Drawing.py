
from math import pi, sin
import turtle as t
t.hideturtle()
t.speed(10)

    
class House:
    def __init__(self,x,y):
        self.X_Main = x
        self.Y_Main = y
    def Locate(self):    
        t.penup()
        t.setpos(self.X_Main,self.Y_Main)
    
    
    
    
class Geometry_Draw:
    
    def Draw_Rectangle(self,X_0,Y_0,W,H,color="White"):
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
        
    def Draw_Triangle(self,X_0,Y_0,base_lengh,H,color="White"):
        t.fillcolor(color) 
        t.setposition(X_0,Y_0)
        t.begin_fill()
        t.pendown()
        t.forward(base_lengh)
        t.setposition(X_0 +base_lengh/2,Y_0 + H)
        t.setposition(X_0,Y_0)
        t.end_fill()
        t.penup()
        
    def Draw_Trapeze(self,X_0,Y_0,base1_lengh,base2_lengh,H,color="White"):
        t.fillcolor(color) 
        t.setposition(X_0,Y_0)
        t.begin_fill()
        t.pendown()
        t.forward(base1_lengh)
        t.setposition(X_0 +(base1_lengh + base2_lengh)/2,Y_0 + H)
        t.setposition(X_0 +(base1_lengh - base2_lengh)/2,Y_0 + H)
        t.setposition(X_0,Y_0)
        t.end_fill()
        t.penup()
    
    def Draw_Poligon(self,X_0,Y_0,radius,N,color ="White"):
        t.fillcolor(color)
        k = 0
        a = radius * 2 * sin(pi/N)
        t.setposition(X_0,Y_0)
        
        t.sety(Y_0 - radius * sin(pi/N))
        t.setx(X_0 - a)
        t.begin_fill()
        t.pendown()
        while k < N:
            t.forward(a)
            t.left(360/N)
            k += 1
        t.end_fill()
        t.penup()
        

    
    
        
    def Erase(self,X_0,Y_0,W,H,kind,W2 = 0):
        if kind == "Roof Triangle":
            t.pencolor("White")
            Geometry_Draw.Draw_Triangle(self,X_0,Y_0,W,H,color="White")
            t.pencolor("Black")
        if kind == "Roof Rectangle":
            t.pencolor("White")
            Geometry_Draw.Draw_Rectangle(self,X_0,Y_0,W,H,color="White")
            t.pencolor("Black")
        if kind == "Roof Trapeze":
            t.pencolor("White")
            Geometry_Draw.Draw_Trapeze(self,X_0,Y_0,W,W2,H,color="White")
            t.pencolor("Black")
            
            
        if kind in ["Walls","Foundation","Door","Window"]:
            t.pencolor(Walls.Walls_Color)
            Geometry_Draw.Draw_Rectangle(self,X_0,Y_0 + 1,W,H,color=Walls.Walls_Color)
            t.pencolor("Black")
       
        
               
class Foundation(Geometry_Draw,House):
    def __init__(self,x,y,w_f = 400,h_f = 15,fcolor = "Black"):
        House.__init__(self,x,y)
        self.Found_Width = w_f 
        self.Found_Height =  h_f 
        self.Found_Color = fcolor
        self.X_Found = self.X_Main -  self.Found_Width * 0.1  
        self.Y_Found = self.Y_Main -  self.Found_Height
    
    def Draw_Foundation(self):
        Geometry_Draw.Draw_Rectangle(self,self.X_Found, self.Y_Found, 
                              self.Found_Width, self.Found_Height,
                              self.Found_Color)
        
class Walls(Foundation):
    def __init__(self, x , y, w_f = 400, h_f = 15, fcolor ="Black",wcolor="Red"):
        
        Foundation.__init__(self,x,y, w_f, h_f, fcolor)
        self.Walls_Color = wcolor
        self.Walls_Width  = self.Found_Width * 0.8
        self.Walls_Height = self.Found_Height * 15
    

    def change_walls_color(self,new_color):
        self.Walls_Color = new_color
        self.Draw_Walls()
        
    def Draw_Walls(self):
        Geometry_Draw.Draw_Rectangle(self,self.X_Main,self.Y_Main,
                         self.Walls_Width,self.Walls_Height,
                         self.Walls_Color)
    
class Roof(Walls):
    def __init__(self,x , y, w_f = 400, h_f = 15, fcolor ="Black", wcolor="Red", rcolor = "Red",R_variant = "Trapeze"):
        Walls.__init__ (self, x , y, w_f, h_f, fcolor,wcolor)
        self.R_variant = R_variant
        self.Roof_Color = rcolor
        self.Roof_Width = self.Walls_Width * 1.2
        self.Roof_Hieght = self.Walls_Height*0.3
        self.X_Roof = self.X_Main + self.Walls_Width/2 - self.Roof_Width/2
        self.Y_Roof = self.Walls_Height + self.Y_Main
        
    
    def Ch_Rf_Clr(self,new_color):
       self.Roof_Color = new_color
       self.Draw_Roof()
       
    def Draw_Roof(self):
        if self.R_variant == "Triangle":
            Geometry_Draw.Draw_Triangle(self,self.X_Roof,self.Y_Roof,self.Roof_Width,self.Roof_Hieght,self.Roof_Color)
        if self.R_variant == "Rectangle":
            Geometry_Draw.Draw_Rectangle(self,self.X_Roof,self.Y_Roof,self.Roof_Width,self.Roof_Hieght,self.Roof_Color)
        if self.R_variant == "Trapeze":
            Geometry_Draw.Draw_Trapeze(self, self.X_Roof,self.Y_Roof,
                              self.Roof_Width, self.Walls_Width,
                              self.Roof_Hieght,self.Roof_Color)
    
    def Erase_Roof(self):
        Geometry_Draw.Erase(self,self.X_Roof,self.Y_Roof,
                   self.Roof_Width,self.Roof_Hieght,
                   "Roof "+ self.R_variant,
                   self.Walls_Width)
    
    
    
    def Choose_new_roof(self,kind):
        self.Erase_Roof()
        self.R_variant = kind
        self.Draw_Roof()
        
           
            
        
class Door(Walls):
    def __init__(self, x , y, w_f = 400, h_f = 15, Door_location = 30,fcolor ="Black",wcolor="Red",dcolor = "Brown",):
    Walls.__init__ (self, x , y, w_f, h_f, fcolor,wcolor)
    self.Door_Color = dcolor
    self.Door_X = self.X_Main + Door_location
    self.Door_Width = self.Walls_Width * 0.2
    self.Door_Height = self.Walls_Height * 0.8
 
    def Draw_Door(self):
        Door.Draw_Rectangle(self, Door.Door_X, House.Y_Main, 
                            Door.Door_Width, Door.Door_Height, 
                            Door.Door_Color)
    def Erase_Door(self):
        Door.Erase(self, Door.Door_X, House.Y_Main, 
                            Door.Door_Width, Door.Door_Height, 
                            "Door")

class Window(Geometry_Draw):
    Window_Color =  "light blue"
    Window_Radius = 0
    Window_N = 6
    
    def Set_Window(self,N= 6 ,color = "light blue"):
        Window.Window_Color  = color
        Window.Window_Radius = Foundation.Found_Height * 3
        Window.Window_N = N
    def Draw_Window(self):
        Window.Draw_Poligon(self, House.X_Main + 0.6 * Walls.Walls_Width ,House.Y_Main + Walls.Walls_Height * 0.5,
                            Window.Window_Radius,Window.Window_N,Window.Window_Color)


X = -200
Y = -100


obj = Roof(X, Y, w_f = 300, h_f = 10, fcolor = "Yellow", wcolor = "Brown", rcolor = "Gray" )

t.penup()
obj.Draw_Foundation()
obj.Draw_Walls()
obj.Draw_Roof()

obj.Choose_new_roof("Triangle")
obj.Ch_Rf_Clr("Green")

obj2 = Roof(X + 350, Y, w_f = 100, h_f = 10, fcolor = "Black", wcolor = "Red", rcolor = "Blue",R_variant = "Rectangle" )
obj2.Draw_Foundation()
obj2.Draw_Walls()
obj2.Draw_Roof()

obj2.Choose_new_roof("Triangle")
obj2.Ch_Rf_Clr("Yellow")
"""
obj2 = Walls(X,Y + 50, w_f =300, h_f = 10, fcolor = "Yellow",wcolor ="Brown") 

obj2.Draw_Foundation()
obj2.Draw_Walls()

obj.Ch_Rf_Clr()
"""
"""  
House_1 = House(X,Y)
print(House_1.X_Main)



ob.Set_Found(House_1.X_Main,House_1.Y_Main)
Foundation.Draw_Foundation()

House_2 = House(10,-100)




House_1.Choose_new_roof("Rectangle")


print("Начальный тип крыши: ",House_1.variant)

House_1.Choose_new_roof("Rectangle")
House_1.Choose_new_roof("Triangle")

while True:
    ans = input("Поменять цвет стен? Yes/No : ")
    if ans == "Yes":
        color = input("Введите новый цвет: ")
        House.change_walls_color(color)
        House_1.Draw_Door()
        House_1.Draw_Window()
        
    if ans == "No":
        break


while True:
    ans = input("Поменять цвет крыши? Yes/No : ")
    if ans == "Yes":
        color = input("Введите новый цвет: ")
        House_1.Ch_Rf_Clr(color)
    if ans == "No":
        break

QA = input("Стереть крышу?")
if QA == "Yes":
    House_1.Erase_Roof()
    
t.done()
"""

