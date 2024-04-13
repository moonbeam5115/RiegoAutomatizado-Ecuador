import math
from calcular_datos_met import promedios_datos_met

data_path = "data/DatosMeteorologicos_Diarios.csv"
tmax, tmin, hr, hr_min, hr_max = promedios_datos_met(data_path)


T_total = (tmax+tmin)/2
z = 2496.1 # altura a nivel del mar
Tri= 4098*(0.6108*math.exp((17.27*T_total)/(T_total+237.3)))/(T_total+237.3)
P = 101.3*((293-(0.0065*z)/293)^5.26)
y = (0.665*10^3)*P # Constante Psicrosometrica
e0T= 0.6108*(math.exp((17.27*T_total)/(T_total+237.3)))
e0Tmax= 0.6108*(math.exp((17.27*tmax)/(tmax+237.3)))
e0Tmin= 0.6108*(math.exp((17.27*tmin)/(tmin+237.3)))
es= (e0Tmax+e0Tmin)/2
ea= (e0Tmin*(hr_max/100)+ e0Tmax*(hr_min/100))/2
G=0
krs = 0.17 # Coeficiente de Ajuste
Ra = 36.8  # Radiacion Extraterrestre MJ M^-2 Dia^-1 

Rs = krs*(math.sqrt(tmax-tmin))*Ra


#Radiacion solar ajustada en funcion a invernadero-calculado con hargreaves/Consultar/Rsaj
Rsaj = (0.613*Rs)-2.9184
Rso = (0.75*(10^-5)*z)*Ra
omega = 4.903*(10^-9) # Constante Stephen Boltzmann - MJ/M^2*Dia
tmax_k = tmax + 273.16
tmin_k = tmin + 273.16
Rnl= omega*((tmax_k + tmin_k)/2)*(0.34-(0.14*math.sqrt(ea)))*((1.35*(Rs/Rso))-0.35)
alfa = 0.23 # Albedo de la superficie - cultivo de referencia 
Rns= (1-alfa)*Rs
Rn= Rns- Rnl
u2 = 1 # TODO: Preguntar el valor correcto
Etd= (((0.408*Tri*(Rn-G)))+ (y*(900/(T_total+273))*(u2*(es- ea))))/(Tri+y*(1+(0.34*u2)))*24 # De mm/hora a mm/dia

#Ecuaciones
Kc = 0.95
Etc= Kc*Etd
CC = 172 # Capacidad De Campo
Pmp = 143.71 # Punto de Marchitez Permanente
da = 1.3 # Densidad aparente
z2 = 0.50 # Profundidad de zona reticular 
Au = (CC- Pmp)*da*z2 # Agual Util
umbral = 0.3 # Sensibilidad del cultivo a la reduccion del agua en el suelo
Lr = umbral*Au 
Pe = 0 # Aporte efectivo por lluvia
Ge = 0 # Aporte por agua subterranea
Ln = Lr - Pe - Ge # Lamina Neta de riego mm 
Ib =  1.50 # velocidad de infiltracion basica - cm/hora
Tr = (10*Ln)/Ib # (multiplicado por 10 para convertir mm a cm)
Fr = Ln/Etc
Efr = 0.3 # Eficiencia de riego por inundacion
Lb = (Etc*Fr)/Efr
area =  1200000 # mm^2
Vriego = Lb*area 
Ef = (Etc*Fr/Lb) 
Ea = (Ln/Lb)*100


'''
#Rs=Radiacion solar o de onda corta
#krs= Coeficiente de ajuste 
#Ra= Radiacion extraterrestre 
#Rnl= Radiacion neta de onda larga
#Tmax= Temperatura maxima en Kelvin
#Tmin= Temperatura minima en Kelvin
#omega= Constante de Stefan-Boltzmann

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
'''





    

 #  Valores de entrada
#v=Volumen de agua 
#t= tiempo que tarda en llenar el balde
# Tmax=20 #Temperatura maxima en el aire a 2m de altura a cada hora (Sensor)
# Tmin=10 #Temperatura minima en el aire a 2m de altura a cada hora (Sensor)
# z= 1200 #Ecuacion en P-significa altura sobre nivel del mar
# HRmax=13 #Humedad relativa maxima (Sensor)
# HRmin=6 #Humedad relativa minima (Sensor)
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
# V= 1 #Volumen de agua- litros
# t_balde_20L= 1 #tiempo-segundos
# t_hilera_20L= 1 #Tiempo-segundos
#     #Ecuaciones utilziadas
# Q=V/t_balde_20L
# V=Q*t_hilera_20L #Se puede utilizar para distribucion de agua en cada hilera?

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


# El resultdo sera la Evapotranspiracion para determinar el Volumen (cantidad) 
# de agua requerida para el riego
