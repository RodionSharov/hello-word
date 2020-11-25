import random
import math

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
