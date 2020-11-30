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
        t.pendown()
  
   
class Walls:
    def __init__(self,ww,wh,color="Red"):
        self.X_Walls =  House.X_Main
        self.Y_Walls = House.Y_Main
        self.Walls_Width = abs(self.X_Walls)* ww 
        self.Walls_Height = abs(self.Y_Walls)* wh 
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


        
   
    
X = -300
Y = -100



House_Object = House()
House_Object.Locate(X,Y)       
House_Object.First_move()
Walls_Obj = Walls(1.2,1,color = "Green")
Walls_Obj.Draw_Walls()


t.done()
 
