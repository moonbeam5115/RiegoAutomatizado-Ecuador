from calcular_datos_met import promedios_datos_met
from calcular_volumen_de_riego import calcular

def calcular_tiempo(volumen, Caudal):
    
    Tiempo_de_riego = volumen/Caudal # 4.65L*(s/L)

    return Tiempo_de_riego

