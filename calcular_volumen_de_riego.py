import math


def calcular(tmax, tmin, hr_min, hr_max):
    # Calcula el volumen de agua requerido a base de teoria
    T_total= (tmax+tmin)/2
    z = 2496.1 # altura a nivel del mar
    Tri= 4098*(0.6108*math.exp((17.27*T_total)/(T_total+237.3)))/(T_total+237.3)
    P = 101.3*((293-(0.0065*z)/293)**5.26)
    y = (0.665*10**3)*P # Constante Psicrosometrica
    e0Tmax = 0.6108*(math.exp((17.27*tmax)/(tmax+237.3)))
    e0Tmin = 0.6108*(math.exp((17.27*tmin)/(tmin+237.3)))
    es = (e0Tmax + e0Tmin)/2
    ea = (e0Tmin*(hr_max/100)+ e0Tmax*(hr_min/100))/2
    G = 0
    krs = 0.17 # Coeficiente de Ajuste
    Ra = 37  # Radiacion Extraterrestre MJ M^-2 Dia^-1 # TODO: Preguntar el valor correcto

    Rs = krs*(math.sqrt(tmax-tmin))*Ra #Radiacion solar ajustada en funcion a invernadero-calculado con hargreaves/Consultar/Rsaj
    # Rsaj = (0.613*Rs)-2.9184
    Rso = (0.75*(10**-5)*z)*Ra
    omega = 4.903*(10**-9) # Constante Stephen Boltzmann - MJ/M^2*Dia
    tmax_k = tmax + 273.16
    tmin_k = tmin + 273.16
    Rnl= omega*((tmax_k + tmin_k)/2)*(0.34-(0.14*math.sqrt(ea)))*((1.35*(Rs/Rso))-0.35)
    alfa = 0.23 # Albedo de la superficie - cultivo de referencia 
    Rns= (1-alfa)*Rs
    Rn= Rns- Rnl
    u2 = 1 # TODO: Preguntar el valor correcto
    Etd= (((0.408*Tri*(Rn-G)))+ (y*(900/(T_total+273))*(u2*(es- ea))))/(Tri+y*(1+(0.34*u2)))

    #Ecuaciones
    Kc = 0.90
    Etc= Kc*Etd
    CC = 8 # TODO: Encontrar valores
    Pmp = 1 # TODO: Encontrar valores
    da = 1 # TODO: Encontrar valores
    z2 = 0.50 # Profundidad de zona reticular 
    Au= (CC - Pmp)*da*z2
    umbral = 0.35 # Sensibilidad del cultivo a la reduccion del agua en el suelo
    Lr = umbral* Au
    Pe = 0 # Aporte efectivo por lluvia
    Ge = 0 # Aporte por agua subterranea
    Ln = Lr - Pe - Ge # Lamina Neta de riego mm TODO: Pasar a cm
    Ib =  1.50 # velocidad de infiltracion basica - cm/hora
    Tr = Ln/Ib
    Fr = Ln/Etc
    Efr = 0.3 # Eficiencia de riego por inundacion
    Lb = (Etc*Fr)/Efr
    area =  1.2 # m^2
    volumen_de_riego = Lb*area 
    Ef = (Etc*Fr/Lb)
    Ea = (Ln/Lb)*100

    return volumen_de_riego    
