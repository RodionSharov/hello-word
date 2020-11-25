# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 19:09:00 2020

@author: Родион
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 14:57:05 2020

@author: Родион
"""

import orvd_functions as orvd 
import math
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import random
from sympy import Point,Line
import numpy as np



random.seed()
plt.ion()
kolvo_otmetok = list(range(1,20)) # Количество ложных отметок в каждый осчёт рабочего цикла.
disp = 6           # Дисперсия погрешности руления ЛА.
bound_Len = list(range(5,20,1))     #  Размер границ допустимого расположения ЛА, м         
v_LA = list(range(5,20,1))        # Скорость ЛА, м/с.
            # Счётчик количества проходов основного цикла.
time_step = 1      # Временной шаг, с.
 # Минимальное расстояние от поворотного пункта.    
X, Y = [0], [0]    # Массивы рассчётных координат ЛА, без зашумления.  
false_x,false_y = [], [] # Массивы для координат ложных отметок.

x = [-1000, -900, -500,
     0, 500, 700,
     1000,1500, 2000] #  Координаты Х поворотных пунктов. 

y = [225, 250, 250,
     200, 200,250,
     250,150,150]  #  Координаты Y поворотных пунктов. 
x.append(y[len(y)-1]-y[len(y)-2]+ x[len(x)-1])
y.append(-x[len(y)-1]+x[len(y)-2]+y[len(y)-1])

x.insert(0,-y[1]+y[0]+x[0])
y.insert(0,y[0]+x[2]-x[1])


def scalar_product(vector1,vector2):
    return vector1[0]*vector2[0] + vector1[1]*vector2[1]

XR, YR = [], [] # Массивы зашумлённых координат
MASSIV_S_XR_I_XO, MASSIV_S_YR_I_YO = [], [] # Многомерные массивы с координатами  ложных отметок и зашумлёнными координатами ЛА
Phi_List =[] # Список для курсов ЛА
vector,summ_vector= [],[] # Создание списков: напрявляющих и суммарных векторов участков траектории ЛА
coefs_list = [] # Список коэффициентов уравнений в общем виде для прямых участков траектории ЛА
biss_coefs = [] # Список коэффициентов уравнений в общем виде для биссектрисс углов между двумя соседними участками траектории ЛА 
# Создание списков для координат точек истинных/ложных, принятых за истинные/ложные
# Формат имён списков: КООРДИНАТА(X/Y)_Насамомделе(True/False)_Зачтопринята(True/False)
X_False_False, Y_False_False = [], []
X_False_True, Y_False_True= [],[]
X_True_False, Y_True_False = [], []
X_True_True, Y_True_True = [], []
print("Координаты X пунктов: ",*x)
print("Координаты Y пунктов: \n",*y)
print ("Начальная путевая скорость = ",v_LA ,"м/с")
print("Ширина дпоустимых границ = ",bound_Len)
print("Количество ложных точек в каждый момент времени:",kolvo_otmetok)
steps = 10


def Main_Function(V_LA,Bound_Len,Kolvo_otmetok):
    dmin = V_LA * time_step * math.sqrt(2)
    n = 2 
    j = 1
    X.clear(),Y.clear(),XR.clear(),YR.clear(),Phi_List.clear()
    vector.clear(),summ_vector.clear()
    coefs_list.clear(),biss_coefs.clear()
    X_False_False.clear(),Y_False_False.clear()
    X_True_False.clear(),Y_True_False.clear()
    X_False_True.clear(),Y_False_True.clear()
    X_True_True.clear(),Y_True_True.clear()
    # Массивы с координатами границ.
    x_bound1 = [x[1] - Bound_Len, 0, 0, 
                0, 0, 0,
                0, 0, 0 ]
    y_bound1 = [y[1], 0, 0,
                0, 0, 0,
                0, 0, 0 ]

    x_bound2 = [x[1] + Bound_Len, 0, 0,
                0, 0, 0,
                0, 0, 500 ]
    y_bound2 = [y[1], 0, 0,
                0, 0, 0,
                0, 0,0]
     # Радиус допустимой окружности
    bound_radius =  V_LA * 3 * time_step
    Phi = orvd.Phi_LA(x[1],x[2],y[1],y[2])  # Определение начального курса
    Phi_List.append(Phi*180/math.pi) # Добавление начального курса в список
    # Запись в массивы рассчётных координат ЛА начальных значений - координаты первого пункта
    X.append(x[1]) 
    Y.append( y[1] )
    # Основной цикл, формирующий траекторию ЛА (рассчётную и зашумлённую), а также заполняющий многомерные массивы.
    while n < len(x)-1:  # Пока порядковый номер поворотного пункта меньше своего наибольшего значения, равного длинне массива х (или у) 
        # Вставка в массивы расчётных координат рассчитанных по проекциям скорости значений
        X.insert(j,X[j-1] + V_LA *math.cos(Phi)*time_step)  
        Y.insert(j,Y[j-1] + V_LA *math.sin(Phi)*time_step)
        # Рассчёт расстояния до следующего поворотного пункта
        d = orvd.distance([X[j],Y[j]],[x[n],y[n]])
       
        
        
        
        noise_list = orvd.Noise(0,disp,X[j],Y[j]) # Создание списка с зашумлёнными координатами
        XR.insert(j-1,noise_list[0])         # Вставка зашумлённого значения координаты Х
        YR.insert(j-1,noise_list[1])         # Вставка зашумлённого значения координаты Y
        # Очистка списков с координатами ложных отметок
        false_x.clear()
        false_y.clear()
        #  Заполнение списков с координатами ложных отметок, с одной дополнительной
        for i in range(Kolvo_otmetok+1):
            false_y.insert(i,random.uniform(min(y), max(y)))
            false_x.insert(i,random.uniform(min(x), max(x)))
            # Удаление последнего элемента из заполенных списков.
        false_x.pop(Kolvo_otmetok)
        false_y.pop(Kolvo_otmetok)
        # Добавление в конце списков соответствующей зашумленной координаты
        false_x.append(XR[j-1])
        false_y.append(YR[j-1])
        # Вставка в многомерные массивы копий соответствующих списков  
        MASSIV_S_XR_I_XO.insert(j-1,false_x.copy())
        MASSIV_S_YR_I_YO.insert(j-1,false_y.copy())
        # Ложные попали ли в окружность?
        for f in range(len(false_x)-1):
            if orvd.distance([MASSIV_S_XR_I_XO[j-1][f], MASSIV_S_YR_I_YO[j-1][f]], [X[j-1],Y[j-1]]) <= bound_radius:
                X_False_True.append(MASSIV_S_XR_I_XO[j-1][f])
                Y_False_True.append(MASSIV_S_YR_I_YO[j-1][f])
        # Зашумлённая отметка попадает в окружность?
        if orvd.distance([MASSIV_S_XR_I_XO[j-1][Kolvo_otmetok], MASSIV_S_YR_I_YO[j-1][Kolvo_otmetok]], [X[j-1],Y[j-1]]) <= bound_radius:
            X_True_True.append(MASSIV_S_XR_I_XO[j-1][Kolvo_otmetok])    
            Y_True_True.append(MASSIV_S_YR_I_YO[j-1][Kolvo_otmetok])
        
        
        # Проверка условия близости ЛА к поворотному пункту
        if d < dmin:       
            if n == len(x)-2:  # Если порядковый номер совпадает с его конечным значением - завершение работы цикла.
                break
            else:              # В остальных случаях: 
                Phi = orvd.Phi_LA(x[n],x[n+1],y[n],y[n+1])  # Пересчёт курса ЛА
                n += 1                                 # Переход к следующему по порядку пункту
                Phi_List.append(Phi*180/math.pi)       # Вставка пересчитанного курса в список курсов.
        j += 1  # Увеличение счётчика проходов 

# Рассчёт коэффициентов уравнений в общем виде для прямых, на которых будут располагаться точки допустимых границ.
   


# Цикл заполнения списка направляющих векторов участков траектории ЛА 
    for i in range(len(x)-1):
        vector.insert(i, [x[i+1]-x[i],y[i+1]-y[i]])

# Цикл заполнения списка суммарных векторов направления двух соседних участков траектрии ЛА
    for i in range(len(vector)-1):
        summ_vector.append([vector[i][0]+vector[i+1][0],
                            vector[i][1]+vector[i+1][1]])


   

    for i in range(len(x)-1):
        p0,p1= Point(x[i],y[i]),Point(x[i+1],y[i+1]) # Создание двух объектов -двумерных точек (функция Point(x,y) из библиотеки sympy)
        l = Line(p0,p1)   # Создание объекта - прямой линии на плоскости, проходящей через две точки p0,p1 (функция Line(Point(x1,y1),Point(x2,y2)) из библиотеки sympy )
        coefs_list.append(l.coefficients) # Дополнение списка коэффициентов, к объекту-прямой на плоскости применяется метод coefficients

    # Цикл определения необходимой биссектрисы и определение её коэффициентов в уравнении общего вида
    for i in range(1,len(x)-1): # Отсчёт начинается с 1 из-за наличия дополнительной точки в начале списков x и y, не входящей в траекторию ЛА
        A = float(coefs_list[i-1][0]) # Коэффициент А предыдущей прямой
        B = float(coefs_list[i-1][1]) # Коэффициент B предыдущей прямой
        C = float(coefs_list[i-1][2]) # Коэффициент C предыдущей прямой
        A1 = float(coefs_list[i][0])  # Коэффициент А текущей  прямой        
        B1 = float(coefs_list[i][1])  # Коэффициент B текущей  прямой
        C1 = float(coefs_list[i][2])  # Коэффициент C текущей  прямой
        const = math.sqrt((A**2 + B**2)/(A1**2+B1**2))  # Общая для двух биссектрис константа, выводится из уравнения для биссектрисы угла между прямыми
        norm1_coef = math.sqrt((A-A1*const)**2+(B-B1*const)**2) # Нормирующий коэффициент для первой биссектрисы
        norm2_coef = math.sqrt((A+A1*const)**2+(B+B1*const)**2) # Нормирующий коэффициент для второй биссектрисы
        norm_biss1 = [(A-A1*const)/norm1_coef,
                      (B-B1*const)/norm1_coef] # Единичный вектор нормали первой биссектрисы
        norm_biss2 = [(A+A1*const)/norm2_coef, 
                      (B+B1*const)/norm2_coef] # Единичный вектор нормали второй биссектрисы    
        # Проверка условия выбора нужной биссектрисы - 
        # Если скалярное произведние(по модулю) вектора нормали первой биссектрисы 
        # на суммарный направляющий ветор в данной точке больше, чем такое же произведение(по модулю)
        # для нормали второй биссектрисы, то выбираем первую биссектрису 
        # иначе - выбираем вторую    
        if abs(orvd.scalar_product(norm_biss1,summ_vector[i-1]/np.linalg.norm(summ_vector[i-1]))) > abs(orvd.scalar_product(norm_biss2,summ_vector[i-1]/np.linalg.norm(summ_vector[i-1]))):
            biss_coefs.append(((A-A1*const)/norm1_coef,(B-B1*const)/norm1_coef,(C-C1*const)/norm1_coef))
        else:
            biss_coefs.append(((A+A1*const)/norm2_coef,(B+B1*const)/norm2_coef,(C+C1*const)/norm2_coef))
        # Коэффициенты биссектрис при записи нормируются.

    # Формирование границ допустимой области 

    for i in range(len(x)-2): 
        if i == len(x)-3: break
        x1 = x[i+2] + Bound_Len * biss_coefs[i+1][1]
        x2 = x[i+2] - Bound_Len * biss_coefs[i+1][1]
        if biss_coefs[i+1][1] != 0:
            y1 = (-biss_coefs[i+1][2]-x1*biss_coefs[i+1][0])/biss_coefs[i+1][1]
            y2 = (-biss_coefs[i+1][2]-x2*biss_coefs[i+1][0])/biss_coefs[i+1][1]
        if biss_coefs[i+1][1] == 0:
            y1 = y[i+2] + Bound_Len
            y2 = y[i+2] - Bound_Len
        
        bound1 = [x_bound1[i],y_bound1[i]]
        cros11 = orvd.Cross_point(bound1,[x1,y1],[x[i+1],y[i+1]],[x[i+2],y[i+2]])
        cros21 = orvd.Cross_point(bound1,[x2,y2],[x[i+1],y[i+1]],[x[i+2],y[i+2]])  
        if type(cros11[0]) == str:
            y_bound1[i+1] = y1 
            x_bound1[i+1] = x1
            y_bound2[i+1] = y2 
            x_bound2[i+1] = x2 
        if type(cros21[0]) == str:
            y_bound1[i+1] = y2  
            x_bound1[i+1] = x2
            y_bound2[i+1] = y1 
            x_bound2[i+1] = x1
        if   type(cros11[0]) != str and type(cros21[0]) != str:  
            d_cr11_to_bound1_i = orvd.distance(cros11,bound1)
            d_cr21_to_bound1_i = orvd.distance(cros21,bound1)
            if d_cr11_to_bound1_i > d_cr21_to_bound1_i: 
                y_bound1[i+1] = y1 
                x_bound1[i+1] = x1
                y_bound2[i+1] = y2 
                x_bound2[i+1] = x2  
            if d_cr11_to_bound1_i < d_cr21_to_bound1_i:
                y_bound1[i+1] = y2  
                x_bound1[i+1] = x2
                y_bound2[i+1] = y1 
                x_bound2[i+1] = x1

    for i in range(len(X)-1):
        for f in range(Kolvo_otmetok):
            for k in range(len(x)-3):
                x_pol = (x_bound1[k],x_bound2[k],x_bound2[k+1], x_bound1[k+1])
                y_pol = (y_bound1[k],y_bound2[k],y_bound2[k+1], y_bound1[k+1])
                if orvd.inPolygon(MASSIV_S_XR_I_XO[i][f], MASSIV_S_YR_I_YO[i][f], x_pol, y_pol):
                    X_False_True.append(MASSIV_S_XR_I_XO[i][f])
                    Y_False_True.append(MASSIV_S_YR_I_YO[i][f])
                    break
                elif k == len(x)-4:
                    X_False_False.append(MASSIV_S_XR_I_XO[i][f])
                    Y_False_False.append(MASSIV_S_YR_I_YO[i][f])
            
    for f in range(len(X)-1):
        for k in range(len(x)-3):
                x_pol = (x_bound1[k],x_bound2[k],x_bound2[k+1], x_bound1[k+1])
                y_pol = (y_bound1[k],y_bound2[k],y_bound2[k+1], y_bound1[k+1])
                if orvd.inPolygon(MASSIV_S_XR_I_XO[f][Kolvo_otmetok],MASSIV_S_YR_I_YO[f][Kolvo_otmetok],x_pol,y_pol):
                    X_True_True.append(MASSIV_S_XR_I_XO[f][Kolvo_otmetok])
                    Y_True_True.append(MASSIV_S_YR_I_YO[f][Kolvo_otmetok])
                    break
                elif k == len(x)-4:
                    X_True_False.append(MASSIV_S_XR_I_XO[f][Kolvo_otmetok])
                    Y_True_False.append(MASSIV_S_YR_I_YO[f][Kolvo_otmetok])
    
    True_False_mean = 100*len(X_True_False)/(len(X_True_False)+len(X_True_True))
    False_True_mean = 100*len(X_False_True)/(len(X_False_True) + len(X_False_False))
    return [True_False_mean, False_True_mean]

meanTF,meanFT = 0,0
meanFT_to_plotVLA = []
meanTF_to_plotVLA = []
for i in range(len(v_LA)):
    cycle_count = 0
    while cycle_count < steps:
        meanTF += Main_Function(v_LA[i],bound_Len[9],kolvo_otmetok[1])[0]
        meanFT += Main_Function(v_LA[i],bound_Len[9],kolvo_otmetok[1])[1]
        cycle_count += 1
    meanTF_to_plotVLA.append(meanTF/steps)
    meanFT_to_plotVLA.append(meanFT/steps)
    meanTF,meanFT = 0,0


meanFT_to_plotBL = []
meanTF_to_plotBL = []
for i in range(len(bound_Len)):
    cycle_count = 0
    while cycle_count < steps:
        meanTF += Main_Function(v_LA[5],bound_Len[i],kolvo_otmetok[1])[0]
        meanFT += Main_Function(v_LA[5],bound_Len[i],kolvo_otmetok[1])[1]
        cycle_count += 1
    meanTF_to_plotBL.append(meanTF/steps)
    meanFT_to_plotBL.append(meanFT/steps)
    meanTF,meanFT = 0,0
    
meanFT_to_plotKT = []
meanTF_to_plotKT = []

for i in range(len(kolvo_otmetok)):
    cycle_count = 0
    while cycle_count < steps:
        meanTF += Main_Function(v_LA[5],bound_Len[9],kolvo_otmetok[i])[0]
        meanFT += Main_Function(v_LA[5],bound_Len[9],kolvo_otmetok[i])[1]
        cycle_count += 1
    meanTF_to_plotKT.append(meanTF/steps)
    meanFT_to_plotKT.append(meanFT/steps)
    meanTF,meanFT = 0,0


fg = plt.figure(figsize=(9,9),constrained_layout = True)
gs = gridspec.GridSpec(ncols = 2, nrows = 3,figure = fg)

fig_ax_1 = fg.add_subplot(gs[0,0],xlabel =  "Скорость ЛА, м/с",ylabel = ' meanTrue_False, % ',title = 'meanTrue_False(V_LA)') 
plt.plot(v_LA, meanTF_to_plotVLA,'--')

fig_ax_2 = fg.add_subplot(gs[1,0],xlabel =  "Длина границ, м",ylabel = ' meanTrue_False, % ',title = 'meanTrue_False(Bound_Len)') 
plt.plot(bound_Len, meanTF_to_plotBL,'--')

fig_ax_3 = fg.add_subplot(gs[2,0],xlabel =  "Число ложных меток",ylabel = ' meanTrue_False, % ',title = 'meanTrue_False(Kolvo_octmetok)') 
plt.plot(kolvo_otmetok,meanTF_to_plotKT,'--')

fig_ax_4 = fg.add_subplot(gs[0,1],xlabel =  "Скорость ЛА, м/с",ylabel = ' meanFalse_True, % ',title = 'meanFalse_True(V_LA)') 
plt.plot(v_LA, meanFT_to_plotVLA,'--')

fig_ax_5 = fg.add_subplot(gs[1,1],xlabel =  "Длина границ, м",ylabel = ' meanFalse_True, % ',title = 'meanFalse_True(Bound_Len)') 
plt.plot(bound_Len, meanFT_to_plotBL,'--')

fig_ax_6 = fg.add_subplot(gs[2,1],xlabel =  "Число ложных меток",ylabel = ' meanFalse_True, % ',title = 'meanFalse_True(Kolvo_octmetok)') 
plt.plot(kolvo_otmetok,meanFT_to_plotKT,'--')



plt.show()



