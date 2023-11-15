import math
 #  Valores de entrada
#v=Volumen de agua 
#t= tiempo que tarda en llenar el balde
Tmax=20 #Temperatura maxima en el aire a 2m de altura a cada hora (Sensor)
Tmin=10 #Temperatura minima en el aire a 2m de altura a cada hora (Sensor)
z= 1200 #Ecuacion en P-significa altura sobre nivel del mar
HRmax=13 #Humedad relativa maxima (Sensor)
HRmin=6 #Humedad relativa minima (Sensor)
#u2= Velocidad de viento a 2 m de altura/se supone cero debido al invernadero
#Ra= Radiacion extraterrestre
#es= Presion de vapor de saturacion/ Calcular
#ea= Presion real de vapor/ Calcular
#CC= Capacidad de campo
#Pmp= Contenido de humedad a punto de marchitez permanente
#da= Densidad aparente del suelo
#z2= Produndidad de la zona reteicular 
#Pe= Aporte efectivo por lluvia 
#Ge= Aporte de agua subterranea 
#Ib= Velocidad de infiltracion basica 
#area=area de cultivo

    #Constantes
#krs= Coeficiente de ajuste   
#omega= Constante de Stefan-Boltzmann
#alf= alfa
#y= Constante psicrometrica 
#z= Altura sobre el nivel del mar
#kc= Coeficiente de cultivo
#umbral= Umbral de riego
    #Metodo Volumetrico/Conocer el caudal de salida
#Q=Caudal
V= 1 #Volumen de agua- litros
t_balde_20L= 1 #tiempo-segundos
t_hilera_20L= 1 #Tiempo-segundos
    #Ecuaciones utilziadas
Q=V/t_balde_20L
V=Q*t_hilera_20L #Se puede utilizar para distribucion de agua en cada hilera?

    #Metodo de Penman-Monteith/Evapotrasnpiracion
#Etd= Evapotrasnpiracion diaria en cultivos de referencia 
#Rn= Radiacion neta en la superficie del cultivo
#G= Flujo del calor de suelo
#Thr= Temperatura media del aire a 2 m de altura cada hora/sensor de temperatura 
#u2= Velocidad de viento a 2 m de altura/se supone cero debido al invernadero
#es= Presion de vapor de saturacion
#ea= Presion real de vapor
#Tri= Pendiente de la curva de presion de vapor 
#y= Constante psicrometrica 
#z= Altura sobre el nivel del mar
T= (Tmax+Tmin)/2
Tri= 4098*(0.6108*math.exp((17.27*T)/(T+237.3)))/(T+237.3)
P= 101.3*((293-(0.0065*z)/293)^5.26)
y= (0.665*10^3)*P
e0T=0.6108*(math.exp((17.27*T)/(T+237.3)))
e0Tmax=0.6108*(math.exp((17.27*Tmax)/(Tmax+237.3)))
e0Tmin=0.6108*(math.exp((17.27*Tmin)/(Tmin+237.3)))
es= (e0Tmax+e0Tmin)/2
ea= (e0Tmin*(HRmax/100)+ e0Tmax*(HRmin/100))/2
G=0

    #Radiacion Neta
#Rs=Radiacion solar o de onda corta
#krs= Coeficiente de ajuste 
#Ra= Radiacion extraterrestre 
#Rnl= Radiacion neta de onda larga
#Tmax= Temperatura maxima en Kelvin
#Tmin= Temperatura minima en Kelvin
#omega= Constante de Stefan-Boltzmann
Rs= krs*(math.sqrt(Tmax-Tmin))*Ra

    #Radiacion solar ajustada en funcion a invernadero-calculado con hargreaves/Consultar/Rsaj
Rsaj=(0.613*Rs)-2.9184
Rso= (0.75*(10^-5)*z)*Ra
Rnl= omega*((TmaxK+TminK)/2)*(0.34-(0.14*math.sqrt(ea)))*((1.35*(Rs/Rso))-0.35)
Rns= (1-alf)*Rs
Rn= Rns- Rnl 
Etd= (((0.408*Tri*(Rn-G)))+ (y*(900/(T+273))*(u2*(es- ea))))/(Tri+y*(1+(0.34*u2)))
#Evapotrasnpiracion del cultivo y requerimiento de agua
#Etc= Evapotranspiracion de cultivo
#Kc= Coeficiente de cultivo
#Au= Lamina total de agua disponible en la zona reticular
#CC= Contenido de Humedad a capacidad de campo 
#Pmp= Contenido de humedad a punto de marchitez permanente
#da= Densidad aparente del suelo
#z2= Produndidad de la zona reteicular 
#Lr= Lamina de riego
#umbral= Umbral de riego
#Ln= Lamina neta de riego
#Pe= Aporte efectivo por lluvia 
#Ge= Aporte de agua subterranea 
#Tr= Tiempo de riego
#Ib= Velocidad de infiltracion basica 
#Fr= Frecuencia de riego maximo
#Areac= area cultivada
#Lb= Lamina bruta de riego
#Efr= Eficiencia de Riego
#Vriego= Volumen de riego a aplicar
#Ef= Eficiencia del sistema de riego
#Ea= Eficiencia de aplicacion de riego

    #Ecuaciones
Etc= Kc*Etd
Au= (CC- Pmp)*da*z2
Lr= umbral* Au 
Ln= Lr-Pe-Ge 
Tr= Ln/Ib
Fr= Ln/Etc
Lb= (Etc*Fr)/Efr
Vriego= Lb*area 
Ef= (Etc*Fr/Lb)
Ea= (Ln/Lb)*100

