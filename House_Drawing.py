
from math import pi, sin,sqrt
import turtle as t


Common_House_Parametrs = dict(x = -200,y = -100, w_f = 400, h_f = 15,
                              Door_location = 0.05,N =6,winloc= 0.6,
                              fcolor = "Black",wcolor="Red",
                              rcolor = "Red",dcolor = "Brown",
                              wincolor = "light blue",R_variant = "Trapeze")
#x = -200,y = -100, w_f = 400, h_f = 15,Door_location = 30,N =6,winloc= 0.6,fcolor = "Black",wcolor="Red",rcolor = "Red",dcolor = "Brown",wincolor = "light blue",R_variant = "Trapeze" 

class House:
    def __init__(self,House_Parametrs = Common_House_Parametrs ):
        self.This_House_Parametrs = Common_House_Parametrs.copy()
        self.This_House_Parametrs.update(House_Parametrs)
         
        print("Создаётся дом с параметрами:",self.This_House_Parametrs)
                 
        self.House_Found = Foundation(self.This_House_Parametrs)   #self.X_Main,self.Y_Main, self.F_wh,self.F_ht,self.F_clr
        self.House_Wall = Walls(self.This_House_Parametrs)
        self.House_Roof = Roof(self.This_House_Parametrs)   # self.X_Main,self.Y_Main, self.F_wh,self.F_ht,self.F_clr,self.W_clr,self.R_clr,self.R_Var
        self.House_Door = Door(self.This_House_Parametrs) #self.X_Main,self.Y_Main, self.F_wh,self.F_ht, self.D_Loc,self.D_clr
        self.House_Window = Window(self.This_House_Parametrs)  # self.X_Main,self.Y_Main,self.F_wh,self.F_ht,self.Win_N,self.Win_Loc,self.Win_Clr
      
    # Метод изменения цвет стен 
    def change_walls_color(self,new_color):
        del self.House_Door
        del self.House_Window  
        del self.House_Wall
        self.This_House_Parametrs.update(dict(wcolor = new_color))
        self.House_Wall     = Walls(self.This_House_Parametrs)
        self.House_Door     = Door(self.This_House_Parametrs)
        self.House_Window   = Window(self.This_House_Parametrs)
        
        
    # Метод для изменения цвета крыша
    def change_Roof_color(self,new_color):
        del self.House_Roof  #self.House_Roof.Erase_Roof()
        self.This_House_Parametrs.update(dict(rcolor = new_color))   
        self.House_Roof = Roof(self.This_House_Parametrs)            # House_Roof.__init__(self.This_House_Parametrs)
        
    # Метод изменения типа крыши
    def Choose_New_Roof(self,kind):
        del self.House_Roof
        self.This_House_Parametrs.update(dict(R_variant = kind))  
        print("Новая крыша: \n",self.This_House_Parametrs["R_variant"])
        self.House_Roof = Roof(self.This_House_Parametrs) 
    # Метод изменения цвета дверей
    def change_Door_color(self,new_color):
        del self.House_Door
        self.This_House_Parametrs.update(dict(dcolor = new_color))
        self.House_Door     = Door(self.This_House_Parametrs)
    
    # Метод изменения положения
    def Change_Position(self,x_new,y_new):
        print("Дом перемещается...")
        
        House.__del__(self)
        self.This_House_Parametrs.update(dict(x = x_new,y = y_new))  
        House.__init__(self,self.This_House_Parametrs)
        
    # Метод изменения ширины фундамента
    def Increase_the_width(self,koeff):
        House.__del__(self)
        self.This_House_Parametrs.update(dict(w_f = koeff * self.This_House_Parametrs["w_f"] ))
        House.__init__(self,self.This_House_Parametrs)
    
    # Метод изменения цвета окна 
    def change_Window_color(self,new_color):
        del self.House_Window
        self.This_House_Parametrs.update(dict(wincolor = new_color))  
        self.House_Window = Window(self.This_House_Parametrs)
    
    def change_Window_N(self,new_N):
        del self.House_Window
        del self.House_Door
        del self.House_Wall
        
        self.This_House_Parametrs.update(dict(N = new_N))
        self.House_Wall     = Walls(self.This_House_Parametrs)
        self.House_Window   = Window(self.This_House_Parametrs)
        self.House_Door     = Door(self.This_House_Parametrs)
        
    def __del__(self):
        print("Дом удаляется")
        del self.House_Found
        del self.House_Wall
        del self.House_Roof
        del self.House_Door
        del self.House_Window
        
        # t.pencolor("White")
        # self.House_Roof.Erase_Roof()
        # self.House_Found.Erase_Foundation()
        # self.House_Wall.Erase_Walls()
        # t.pencolor("Black")
    
class Geometry_Draw:
    
    def Draw_Rectangle(self,X_0,Y_0,W,H,color="White"):
        t.penup()
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
        
 
         
    def Erase(self,X_0,Y_0,W=0,H=0,kind ="none",win_radius = 0,win_N = 6,W2 = 0,lay_color = "White"):
        if kind == "Roof Triangle":
            t.pencolor(lay_color)
            Geometry_Draw.Draw_Triangle(self,X_0,Y_0,W,H,color = lay_color)
            t.pencolor("Black")
        if kind in ["Roof Rectangle","Foundation","Walls"]:
            t.pencolor(lay_color)
            Geometry_Draw.Draw_Rectangle(self,X_0,Y_0,W,H,color = lay_color)
            t.pencolor("Black")
        if kind == "Roof Trapeze":
            t.pencolor(lay_color)
            Geometry_Draw.Draw_Trapeze(self,X_0,Y_0,W,W2,H, color = lay_color)
            t.pencolor("Black")
        if kind == "Door":
            t.pencolor(lay_color)
            Geometry_Draw.Draw_Rectangle(self,X_0,Y_0 + 1,W,H,color=lay_color)
            t.pencolor("Black")
        if kind == "Window":
            t.pencolor(lay_color)
            Geometry_Draw.Draw_Poligon(self,X_0,Y_0,win_radius,win_N,color= lay_color)
            t.pencolor("Black")
       
        
      
               
class Foundation(Geometry_Draw):
    def __init__(self, kwargs):   #x,y,w_f,h_f ,fcolor
        print("Создание объекта - Фундамент")
        self.Found_Width = kwargs["w_f"] 
        self.Found_Height = kwargs["h_f"] 
        self.Found_Color = kwargs["fcolor"]
        self.X_Found = kwargs["x"] -  self.Found_Width * 0.1  
        self.Y_Found= kwargs["y"] -  self.Found_Height
        Geometry_Draw.Draw_Rectangle(self,self.X_Found, self.Y_Found, 
                              self.Found_Width, self.Found_Height,
                              self.Found_Color)
        
        
       
    def Erase_Foundation(self):
        print("Фундамент стирается...")
        Geometry_Draw.Erase(self,self.X_Found,self.Y_Found,
                         self.Found_Width,self.Found_Height,kind = "Foundation")
    
    def __del__(self):
       self.Erase_Foundation()
        
class Walls(Geometry_Draw):
    def __init__(self, kwargs): # x , y, w_f, h_f, fcolor,wcolor
        print("Создание объекта - Стены")
        self.Walls_X = kwargs["x"]
        self.Walls_Y = kwargs["y"]
        self.Walls_Color = kwargs["wcolor"]
        self.Walls_Width  = kwargs["w_f"] * 0.8
        self.Walls_Height = kwargs["h_f"] * 15
        self.Draw_Walls()

 
        
    def Draw_Walls(self):
        Geometry_Draw.Draw_Rectangle(self,self.Walls_X,self.Walls_Y,
                         self.Walls_Width,self.Walls_Height,
                         self.Walls_Color)
    def Erase_Walls(self):
        print("Стены стираются...")
        Geometry_Draw.Erase(self,self.Walls_X,self.Walls_Y,
                            self.Walls_Width,self.Walls_Height,kind = "Walls")
        
    def change_walls_color(self,new_color):
        self.Walls_Color = new_color
        self.Draw_Walls()
        
    def __del__(self):  
        self.Erase_Walls()
        
    
class Roof(Geometry_Draw):
    def __init__(self, kwargs):  #x , y, w_f = 400, h_f = 15, fcolor ="Black", wcolor="Red", rcolor = "Red",R_variant = "Trapeze"
        print("Создание объекта - Крыша")
        self.Walls_Width = kwargs["w_f"] * 0.8
        self.Walls_Height = kwargs["h_f"] * 15
        self.R_variant = kwargs["R_variant"]
        self.Roof_Color = kwargs["rcolor"]
        self.Roof_Width = self.Walls_Width * 1.2
        self.Roof_Hieght = self.Walls_Height * 0.3
        self.X_Roof = kwargs["x"] + self.Walls_Width/2 - self.Roof_Width/2
        self.Y_Roof = self.Walls_Height + kwargs["y"]
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
        print("Крыша стирается...")
        Geometry_Draw.Erase(self,self.X_Roof,self.Y_Roof,
                   W = self.Roof_Width, H = self.Roof_Hieght,
                   kind = "Roof "+ self.R_variant,
                   W2 = self.Walls_Width)   
    
    def Choose_new_roof(self,kind):
        self.Erase_Roof()
        self.R_variant = kind
        self.Draw_Roof()
        
    def __del__(self):   
        self.Erase_Roof()
            
        
class Door(Geometry_Draw):
    def __init__(self, kwargs ): #x , y, w_f = 400, h_f = 15, Door_location = 1,dcolor = "Brown"
        print("Создание объекта - Дверь")
      
        self.Door_Color = kwargs["dcolor"]
        self.Walls_Width = kwargs["w_f"] * 0.8
        self.Walls_Height =  kwargs["h_f"] * 15
        self.Walls_Color = kwargs["wcolor"]
        self.Door_Location =  kwargs["Door_location"] * self.Walls_Width
        self.Door_X = kwargs["x"] + self.Door_Location
        self.Door_Y = kwargs["y"]
        self.Door_Width = self.Walls_Width * 0.2
        self.Door_Height = self.Walls_Height * 0.8
        self.Draw_Door()
 
    def Draw_Door(self):
        Geometry_Draw.Draw_Rectangle(self, self.Door_X, self.Door_Y +1, 
                            self.Door_Width, self.Door_Height, 
                            self.Door_Color)
    def Erase_Door(self):
        print("Дверь дома стирается...")
        Geometry_Draw.Erase(self, self.Door_X,self.Door_Y, 
                            self.Door_Width, self.Door_Height, 
                            "Door",lay_color= self.Walls_Color)
    def __del__(self):
        print("Удаление объекта двери")
        self.Walls_Color = "White"
        self.Erase_Door()

class Window(Geometry_Draw):
    def __init__(self,kwargs ):  #x, y, w_f = 400,h_f = 15, N = 6,winloc = 0.6, wincolor = "light blue"
        self.Window_Loc = kwargs["winloc"]
        self.Walls_Width = kwargs["w_f"] * 0.8
        self.Walls_Height = kwargs["h_f"] * 15
        self.Walls_Color = kwargs["wcolor"]
        self.Window_X = kwargs["x"] + self.Window_Loc * self.Walls_Width
        self.Window_Y = kwargs["y"] + 0.5 * self.Walls_Height
        self.Window_Color = kwargs["wincolor"] 
        self.Window_Radius = 0.1 * sqrt(self.Walls_Width*self.Walls_Height) 
        self.Window_N = kwargs["N"]
        self.Draw_Window()
        
        
    def Draw_Window(self):
        Geometry_Draw.Draw_Poligon(self, self.Window_X ,self.Window_Y,
                            self.Window_Radius,self.Window_N,self.Window_Color)
    
    def Erase_Window(self):
        print("Окно дома стриается...")
        Geometry_Draw.Erase(self,self.Window_X ,self.Window_Y,
                            win_radius = self.Window_Radius,win_N = self.Window_N,kind ="Window",
                            lay_color =self.Walls_Color )
    def __del__(self):
        self.Walls_Color = "White"
        self.Erase_Window()
    
    

