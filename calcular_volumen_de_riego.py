import math


def calcular(tmax, tmin, hr_min, hr_max):
    # Calcula el volumen de agua requerido a base de teoria
    T_total = (tmax+tmin)/2
    z = 2496.1 # altura a nivel del mar
    Tri= 4098*(0.6108*math.exp((17.27*T_total)/(T_total+237.3)))/(T_total+237.3)
    P = 101.3*((293-(0.0065*z)/293)**5.26)
    y = (0.665*10**3)*P # Constante Psicrosometrica
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
    Tr = (10*Ln)/Ib # (multiplicado por 10 para convertir mm a cm) - no se utiliza
    Fr = Ln/Etc
    Efr = 0.3 # Eficiencia de riego por inundacion
    Lb = (Etc*Fr)/Efr
    area =  1200000 # mm^2
    volumen_de_riego = Lb*area 
    Ef = (Etc*Fr/Lb) 
    Ea = (Ln/Lb)*100
    print("Frecuencia: ", Fr)
    print("volumen de riego (mL) ", volumen_de_riego)

    return volumen_de_riego
