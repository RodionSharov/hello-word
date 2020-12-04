# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 12:17:12 2020

@author: Родион
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 20:17:42 2020

@author: Родион
"""

import tkinter as tk
import House_Drawing as House_Graphics
import turtle as turtle

window = tk.Tk()
window.title("Hellow world")


House_1_Params = dict(wcolor = "Grey")
House_1 = House_Graphics.House(House_1_Params)

colors = ['Жёлтый','Зелёный','Синий','Чёрный',"Красный","Коричневый","Голубой","Лаймовый","Серый","Розовый","Пурпурный"]
color_in_eng = ["yellow","green","blue","black","Red","Brown","light blue","light green","gray","pink","violet"]

col_var = tk.StringVar(window)
col_var.set(colors[0])

types = ["Треугольник","Прямоугольник","Трапеция"]
types_in_eng =["Triangle","Rectangle","Trapeze"]

types_var = tk.StringVar(window)
types_var.set(types[0])


def callback_color(selection):
    CLR = color_in_eng[colors.index(selection)]
    PRT = Third_Menu.what_part
    if PRT == "Roof":
        House_1.change_Roof_color(CLR)
    if PRT == "Walls":
        House_1.change_walls_color(CLR)
    if PRT == "Door":
        House_1.change_Door_color(CLR)
   
def callback_rtype(selection):
    RTP = types_in_eng[types.index(selection)]
    House_1.Choose_New_Roof(RTP)



class Third_Menu():
    label_col  = tk.Label(window,text = "Выберете цвет:")
    label_type  = tk.Label(window,text = "Выберете тип:")
    
    color_menu = tk.OptionMenu(window,col_var,*colors)
    Rf_type_menu = tk.OptionMenu(window,types_var,*types)
    
    what_part = "Roof"
    
    def __init__(self,Type,part): 
        if Type == "Color" and part in ["Roof","Walls","Door"]:
            Third_Menu.what_part = part
            Third_Menu.label_type.destroy()
            Third_Menu.label_type  = tk.Label(window,text = "Выберете цвет:")
            Third_Menu.label_col.grid(column = 0,row =3)
            PARTS_LIST = ["Roof","Walls","Door"]
                     
            Third_Menu.color_menu.destroy()
            Third_Menu.color_menu = tk.OptionMenu(window,col_var,*colors,command = callback_color)
            Third_Menu.color_menu.grid(column = 1 +PARTS_LIST.index(part) , row =3)
            
            
     
    
            
            
        if Type == "Type" and part in ["Roof","Window"]:
            Third_Menu.label_col.destroy()
            Third_Menu.label_col  = tk.Label(window,text = "Выберете тип:")
            Third_Menu.label_type.grid(column = 0,row =3)
            
            Third_Menu.Rf_type_menu.destroy()
            Third_Menu.Rf_type_menu = tk.OptionMenu(window,types_var,*types,command = callback_rtype)
            Third_Menu.Rf_type_menu.grid(column = 1, row=3)
        


class Second_Menu():
    label = tk.Label(window,text ="Выберете часть дома")
    Roof_choise = tk.Button(window, text = "Крыша")
    Walls_choise = tk.Button(window,text ="Стены")
    Door_choise = tk.Button(window,text = "Дверь")
    
    def __init__(self,Type):
        if Type != "Position":
            Second_Menu.label.grid(column = 0,row =2)
        
            
        # Удаление предыдущих менюшек
        Third_Menu.Rf_type_menu.destroy()
        Third_Menu.color_menu.destroy()
        # Удаление предыдущих надписей с реинициализацией
        Third_Menu.label_type.destroy()
        Third_Menu.label_type  = tk.Label(window,text = "Выберете тип:")
        
        Third_Menu.label_col.destroy()
        Third_Menu.label_col  = tk.Label(window,text = "Выберете цвет:")
        
        
        if Type == "Color":
            
            Second_Menu.label.destroy()
            Second_Menu.label = tk.Label(window,text ="Выберете часть дома:")
            Second_Menu.label.grid(column = 0,row =2)
            
            Second_Menu.Roof_choise.destroy()
            Second_Menu.Walls_choise.destroy()
            Second_Menu.Door_choise.destroy()
            
            Second_Menu.Roof_choise = tk.Button(window, text = "Крыша",command = lambda:Third_Menu(Type,"Roof"))
            Second_Menu.Walls_choise = tk.Button(window, text = "Стены",command = lambda: Third_Menu(Type,"Walls"))
            Second_Menu.Door_choise = tk.Button(window,text = "Дверь",command = lambda: Third_Menu(Type, "Door"))
    
            Second_Menu.Roof_choise.grid(row=2,column = 1) 
            Second_Menu.Walls_choise.grid(row=2,column = 2)
            Second_Menu.Door_choise.grid(row=2,column = 3)       
              
        if Type =="Type":
            
            Second_Menu.label.destroy()
            Second_Menu.label = tk.Label(window,text ="Выберете часть дома:")
            Second_Menu.label.grid(column = 0,row =2)
            
            Second_Menu.Roof_choise.destroy()
            Second_Menu.Door_choise.destroy()
            Second_Menu.Walls_choise.destroy()
            
            Second_Menu.Roof_choise = tk.Button(window, text = "Крыша",command = lambda:Third_Menu(Type,"Roof"))
            
            Second_Menu.Roof_choise.grid(row=2,column = 1)
        
        if Type =="Position":
            
            Second_Menu.label.destroy()
            Second_Menu.label = tk.Label(window,text ="Выберете координаты:")
            Second_Menu.label.grid(column = 0,row =2)
            
            Second_Menu.Roof_choise.destroy()
            Second_Menu.Door_choise.destroy()
            Second_Menu.Walls_choise.destroy()
         
            
              

Color_Menu = tk.Button(window, text="Поменять цвет!",command = lambda: Second_Menu("Color"))
Color_Menu.grid(column=1, row=0)

Type_Menu = tk.Button(window,text =" Поменять тип!",command = lambda: Second_Menu("Type"))
Type_Menu.grid(column =2 , row =0)

Position_Menu = tk.Button(window, text = " Изменить положение!",command =lambda: Second_Menu("Position"))
Position_Menu.grid(column =3, row =0)
  


quitButton = tk.Button(window,text ="ЭСКЕЙП НАЖМИТЕ МОЛОДОЙ ЧЕЛОВЕК",command = window.quit)
quitButton.grid(column =4,row =4)

window.mainloop()