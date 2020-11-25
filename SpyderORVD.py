

import math
import matplotlib.pyplot as plt
import random
disp = 10
n = 1
V_LA = 10
j = 1
time_step = 1
dmin = 0.5
X = [0]*1
Y = [0]*1
x = [1000, 1000, 2000,
     2000, 3500, 3500,
     1700,1700, 2500]

y = [150, 500, 500,
     300, 300,200,
     200,100,100]
print("Координаты X пунктов: ",*x)
print("Координаты Y пунктов: ",*y)
if  x[1]- x[0] == 0:
    if y[1]-y[0] > 0:
        Phi = math.pi/2
    else :
        Phi = - math.pi/2
elif x[1] - x[0] < 0:
    if y[1]-y[0] != 0 :
        Phi = math.pi + math.atan((y[1]-y[0])/(x[1]-x[0]))
    else :
        Phi = math.pi      
else :
    Phi = math.atan((y[1]-y[0])/(x[1]-x[0]))
print ("Начальная путевая скорость = ",V_LA ,"м/с")
print ("Начальный курс = %.1f" % (Phi*180/math.pi),"град")
Phi_List =[]
Phi_List.append(Phi*180/math.pi)
X[0] = x[0]
Y[0] = y[0]
while n < len(x):
    X.insert(j,X[j-1] + V_LA *math.cos(Phi)*time_step)
    
    Y.insert(j,Y[j-1] + V_LA *math.sin(Phi)*time_step)
    
    d = math.sqrt((X[j]-x[n])**2+(Y[j]-y[n])**2)
    
    if d < dmin: 
        if n == len(x)-1:
            break
        if x[n+1]- x[n] == 0:
            if y[n+1]-y[n] > 0:
                Phi = math.pi/2
            Phi = -math.pi/2
        elif  x[n+1]- x[n] < 0:  
            if y[n+1]-y[n] !=0:
                Phi = math.pi + math.atan((y[n+1]-y[n])/(x[n+1]-x[n]))
            else :
                Phi = math.pi
        else :
            Phi =  math.atan((y[n+1] - y[n])/(x[n+1]-x[n]))
        n += 1
        Phi_List.append(Phi*180/math.pi)
    j += 1
     
XR = []
for i in range(len(X)):
    rndx = random.normalvariate(0.1, disp)
    XR.insert(i,X[i]+ rndx)

YR = []
for i in range(len(Y)):
    rndY = random.normalvariate(0.1, disp)
    YR.insert(i,Y[i]+ rndY)

print('Список курсов:',*Phi_List)


print ("Расстояние до конечной точки = %.3f" % (d),"м")
print ("Время движения =  ",(j*time_step),"c")
print ("Конечный курс %.1f" % (Phi*180/math.pi),"град")
plt.figure(figsize=(12,7))
plt.title("Результат АЗНВ за ЛА в аэропорту",
          fontsize ="16",
          color = "b")
plt.xlabel("X",fontsize="13")
plt.ylabel("Y",fontsize="13")

plt.minorticks_on()


plt.grid(which='minor',
         linestyle =':',
         linewidth = 0.5,
         color='green')
plt.grid(which='major',
         linestyle='-',
         linewidth=1,
         color='black')
for l in range(len(x)):
    d = str(l+1)
    plt.text(x[l]+50,y[l]+10,"Пукт "+d,
             color = "red",
             fontsize = 8)


plt.plot(XR,YR,'-',
         color = "black",
         ms=0.1,
         lw=1)
plt.plot(x,y,"bx",color="r",ms=15)
plt.legend(['Траектория ЛА','Контрольные пункты'],
           facecolor='orange',
           edgecolor='blue',
           loc='lower left',
           title='Обозначения',)

plt.show()