





import math
import matplotlib.pyplot as plt
import random
from sympy import Point,Line
import numpy as np
random.seed()
plt.ion()
Kolvo_otmetok = 50 # Количество ложных отметок в каждый осчёт рабочего цикла.
disp = 5           # Дисперсия погрешности руления ЛА.
n = 2              # Порядковый номер элементов в массиве поворотных точек.
V_LA = 3         # Скорость ЛА, м/с.
j = 1              # Счётчик количества проходов основного цикла.
time_step = 1      # Временной шаг, с.
dmin = V_LA*time_step* math.sqrt(2) # Минимальное расстояние от поворотного пункта.    
X, Y = [0], [0]    # Массивы рассчётных координат ЛА, без зашумления.  
false_x,false_y = [], [] # Массивы для координат ложных отметок.

x = [-100, -100, -50,
     0, 50, 70,
     100,150, 200] #  Координаты Х поворотных пунктов. 

y = [225, 260, 250,
     200, 200,230,
     250,220,150]  #  Координаты Y поворотных пунктов. 
x.append(y[len(y)-1]-y[len(y)-2]+ x[len(x)-1])
y.append(-x[len(y)-1]+x[len(y)-2]+y[len(y)-1])

x.insert(0,-y[1]+y[0]+x[0])
y.insert(0,y[0]+x[2]-x[1])



Bound_Len = 10     #  Размер границ допустимого расположения ЛА, м

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

def Phi_LA(X0,X1,Y0,Y1):  
    """Функция определения курса ЛА.
    
    Аргументы:
    Х0, Y0 -- координаты предыдушего поворотного пункта.
    Х1, Y1 -- координаты следуюшего поворотного пункта.
    
    """
    if X1 - X0 == 0:
        if Y1-Y0 >0:
            return math.pi/2
        else:
            return -math.pi/2
    elif X1 - X0 < 0:
        if Y1 - Y0 > 0:
            return math.pi + math.atan((Y1-Y0)/(X1-X0))
        if Y1 - Y0 <= 0:
            return -math.pi + math.atan((Y1-Y0)/(X1-X0))
        else:
            return math.pi
    else:
        return math.atan((Y1-Y0)/(X1-X0))


def Noise(mu,D,Xi,Yi):  
    """Функция зашумления траектории
    
    Аргументы:
    mu -- математическое ожидание ошибки.
    D -- дисперсия ошибки.
    Xi,Yi -- истинные координаты ЛА, рассчитываемые внутри цикла. 
        
    """
    xr = random.normalvariate(0, math.sqrt(D))
    yr = random.normalvariate(0, math.sqrt(D))
    return [Xi+xr, Yi+ yr]

def inPolygon(x, y, xp, yp): # 

    """Функция определения, находмтся ли точка внутри полинома.
    
     Parameters
    ----------
    x,y : float
        Декартовы координаты точки.
    xp, yp: float 
        Кортежи с координатами вершин полинома.
        
    """
    c=0
    for i in range(len(xp)):
        if (((yp[i]<=y and y<yp[i-1]) or (yp[i-1]<=y and y<yp[i])) and 
            (x > (xp[i-1] - xp[i]) * (y - yp[i]) / (yp[i-1] - yp[i]) + xp[i])): c = 1 - c    
    return c

def Cross_point(xy11,xy12,xy21,xy22):
    ''' Функция для нахождения координат двух пересекающихся прямых
    Parameters
    ----------
    xy11 : list
        Координаты первой точки первой прямой.
    xy12 : list
        Координаты второй точки первой прямой.
    xy21 : list
        Координаты первой точки второй прямой.
    xy22 : lsit
        Координаты второй точки второй прямой.

    Returns
    -------
    list
        Координаты [х,y] точки пересечения.
        Если пересечения нет - список из двух строк 'Nan' 

    '''
    k1 = 'Nan'
    k2 = 'Nan'
    if xy12[0]-xy11[0] ==  0 and xy22[0]-xy21[0] ==  0 :
        return ['Nan','Nan']
    
    if xy12[0]-xy11[0] !=0:
        k1 = (xy12[1]-xy11[1])/(xy12[0]-xy11[0])
        b1 = xy11[1] - k1* xy11[0]
    if xy22[0]-xy21[0] !=0:
        k2 = (xy22[1]-xy21[1])/(xy22[0]-xy21[0])
        b2 = xy21[1] - k2 * xy21[0]
    if xy12[0]-xy11[0] ==  0:
        x_cross = xy12[0]
        y_cross = k2* x_cross + b2
        return [x_cross,y_cross]
    if xy22[0]-xy21[0] ==  0:
        x_cross = xy22[0]
        y_cross = k1* x_cross +b1
        return [x_cross,y_cross]
    
    if k1 !='Nan' and k2 != 'Nan':
        if k1-k2 !=0:
            x_cross = (b2-b1)/(k1-k2)
            y_cross = k1* x_cross + b1
            return [x_cross,y_cross]
    if k1 - k2 == 0:
        return ['Nan','Nan']

def distance(point1,point2):
    '''
    Функция определения расстояния между двумя точками

    Parameters
    ----------
    point1 : lsit
        Координаты [x,y] точки 1.
    point2 : list
        Координаты [x,y] точки 2.

    Returns
    -------
    float
        Расстояние в метрах между точками point1 и point2.

    '''
    return math.sqrt((point2[0]-point1[0])**2 + (point2[1]-point1[1])**2)

def scalar_product(vector1,vector2):
    return vector1[0]*vector2[0] + vector1[1]*vector2[1]

# Создание списков для координат точек истинных/ложных, принятых за истинные/ложные
# Формат имён списков: КООРДИНАТА(X/Y)_Насамомделе(True/False)_Зачтопринята(True/False)
X_False_False, Y_False_False = [], []
X_False_True, Y_False_True= [],[]
X_True_False, Y_True_False = [], []
X_True_True, Y_True_True = [], []


XR, YR = [], [] # Массивы зашумлённых координат
MASSIV_S_XR_I_XO, MASSIV_S_YR_I_YO = [], [] # Многомерные массивы с координатами  ложных отметок и зашумлёнными координатами ЛА

# Радиус допустимой окружности
bound_radius =  V_LA * 5 * time_step

print("Координаты X пунктов: ",*x)
print("Координаты Y пунктов: ",*y)

Phi = Phi_LA(x[1],x[2],y[1],y[2])  # Определение начального курса
print ("Начальная путевая скорость = ",V_LA ,"м/с")
print ("Начальный курс = %.1f" % (Phi*180/math.pi),"град\n")
Phi_List =[] # Список для курсов ЛА
Phi_List.append(Phi*180/math.pi) # Добавление начального курса в список
# Запись в массивы рассчётных координат ЛА начальных значений - координаты первого пункта
X[0] = x[1] 
Y[0] = y[1] 
# Основной цикл, формирующий траекторию ЛА (рассчётную и зашумлённую), а также заполняющий многомерные массивы.
while n < len(x)-1:  # Пока порядковый номер поворотного пункта меньше своего наибольшего значения, равного длинне массива х (или у) 
    # Вставка в массивы расчётных координат рассчитанных по проекциям скорости значений
    X.insert(j,X[j-1] + V_LA *math.cos(Phi)*time_step)  
    Y.insert(j,Y[j-1] + V_LA *math.sin(Phi)*time_step)
    # Рассчёт расстояния до следующего поворотного пункта
    d = distance([X[j],Y[j]],[x[n],y[n]])
    noise_list = Noise(0,disp,X[j],Y[j]) # Создание списка с зашумлёнными координатами
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
            if distance([MASSIV_S_XR_I_XO[j-1][f], MASSIV_S_YR_I_YO[j-1][f]], [X[j-1],Y[j-1]]) <= bound_radius:
                X_False_True.append(MASSIV_S_XR_I_XO[j-1][f])
                Y_False_True.append(MASSIV_S_YR_I_YO[j-1][f])
    # Зашумлённая отметка попадает в окружность?
    if distance([MASSIV_S_XR_I_XO[j-1][Kolvo_otmetok], MASSIV_S_YR_I_YO[j-1][Kolvo_otmetok]], [X[j-1],Y[j-1]]) <= bound_radius:
        X_True_True.append(MASSIV_S_XR_I_XO[j-1][Kolvo_otmetok])    
        Y_True_True.append(MASSIV_S_YR_I_YO[j-1][Kolvo_otmetok])
    
    
    
    
    
    # Проверка условия близости ЛА к поворотному пункту
    if d < dmin:       
        if n == len(x)-2:  # Если порядковый номер совпадает с его конечным значением - завершение работы цикла.
            break
        else:              # В остальных случаях:
            print("Через время t =",j*time_step,"c осуществляется поворот")
            print("Расстояние до пункта",n,"равно: %.3f" % (d),"м")
            print('')
            Phi = Phi_LA(x[n],x[n+1],y[n],y[n+1])  # Пересчёт курса ЛА
            print("Обновлённый курс: %.1f " % (Phi*180/math.pi),"град")
            n += 1                                 # Переход к следующему по порядку пункту
            Phi_List.append(Phi*180/math.pi)       # Вставка пересчитанного курса в список курсов.
    j += 1  # Увеличение счётчика проходов 


print ("Расстояние до конечной точки = %.3f" % (d),"м")
print ("Время движения =  ",(j*time_step),"c")
print ("Конечный курс %.1f" % (Phi*180/math.pi),"град")


# Рассчёт коэффициентов уравнений в общем виде для прямых, на которых будут располагаться точки допустимых границ.
vector,summ_vector= [],[] # Создание списков: напрявляющих и суммарных векторов участков траектории ЛА


# Цикл заполнения списка направляющих векторов участков траектории ЛА 
for i in range(len(x)-1):
    vector.insert(i, [x[i+1]-x[i],y[i+1]-y[i]])

# Цикл заполнения списка суммарных векторов направления двух соседних участков траектрии ЛА
for i in range(len(vector)-1):
    summ_vector.append([vector[i][0]+vector[i+1][0],
                        vector[i][1]+vector[i+1][1]])


coefs_list = [] # Список коэффициентов уравнений в общем виде для прямых участков траектории ЛА
biss_coefs = [] # Список коэффициентов уравнений в общем виде для биссектрисс углов между двумя соседними участками траектории ЛА 

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
    const = math.sqrt((A**2 + B**2)/(A1**2 + B1**2))  # Общая для двух биссектрис константа, выводится из уравнения для биссектрисы угла между прямыми
    norm1_coef = math.sqrt((A - A1 * const)**2 + (B - B1 * const)**2) # Нормирующий коэффициент для первой биссектрисы
    norm2_coef = math.sqrt((A + A1 * const)**2 + (B + B1 * const)**2) # Нормирующий коэффициент для второй биссектрисы
    norm_biss1 = [(A-A1*const)/norm1_coef,
                  (B-B1*const)/norm1_coef] # Единичный вектор нормали первой биссектрисы
    norm_biss2 = [(A+A1*const)/norm2_coef, 
                  (B+B1*const)/norm2_coef] # Единичный вектор нормали второй биссектрисы
    
    # Проверка условия выбора нужной биссектрисы - 
    # Если скалярное произведние(по модулю) вектора нормали первой биссектрисы 
    # на суммарный направляющий ветор в данной точке больше, чем такое же произведение(по модулю)
    # для нормали второй биссектрисы, то выбираем первую биссектрису 
    # иначе - выбираем вторую
    
    if abs(scalar_product(norm_biss1,summ_vector[i-1]/np.linalg.norm(summ_vector[i-1]))) > abs(scalar_product(norm_biss2,summ_vector[i-1]/np.linalg.norm(summ_vector[i-1]))):
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
    cros11 = Cross_point(bound1,[x1,y1],[x[i+1],y[i+1]],[x[i+2],y[i+2]])
    cros21 = Cross_point(bound1,[x2,y2],[x[i+1],y[i+1]],[x[i+2],y[i+2]])  
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
        d_cr11_to_bound1_i = distance(cros11,bound1)
        d_cr21_to_bound1_i = distance(cros21,bound1)
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









plt.figure(figsize=(12,10))

plt.title("Результат АЗНВ за ЛА в аэропорту",
          fontsize ="16",
          color = "b")
plt.xlabel("X",fontsize="13")
plt.ylabel("Y",fontsize="13")



plt.minorticks_on()

# Настройка отображения сетки на графике

plt.grid(which='minor',   # Промежуточная сетка
         linestyle ='-.', # Тип линии - штрих-пунктирная
         linewidth = 1,   # Ширина линии = 1
         color = 'blue')  # Цвет линии - синий

plt.grid(which='major',   # Основная сетка
         linestyle ='-',  # Тип линии сплошная
         linewidth = 1,   # Ширина линии = 1
         color ='black')  # Цвет линии - чёрный

for l in range(1,len(x)-1):
    d = str(l)
    plt.text(x[l]+50,y[l]+10,"Пукт " + d,
             color = "red",
             fontsize = 8)
truefalse_str = str(len(X_True_False))

plt.text(150,120, 
         "Число истинных точек, принятых за ложные = "+ truefalse_str, 

         fontsize = 14,


         bbox = dict(boxstyle="round, pad=0.3",ec='black',fc='white'))
x.pop(0)
y.pop(0)
x.pop()
y.pop()

plt.plot(XR,YR,'-',
         color = "black",
         ms=0.1,
         lw=1,)
plt.plot(x,y,"-",color="r",ms=15)
plt.plot(x_bound1,y_bound1,"-",color ='brown')
plt.plot(X_True_True,Y_True_True,'ro',color = "blue",ms=4)
plt.plot(x_bound2,y_bound2,"-",color ='brown')

plt.legend(['Траектория ЛА',' Желаемый путь', 'Границы','Истинные точки, принятые за ложные'],
           facecolor='orange',
           edgecolor='blue',
           loc='lower left',
           title='Обозначения',)
plt.show()

