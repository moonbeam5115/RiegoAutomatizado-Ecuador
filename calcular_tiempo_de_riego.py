Caudal = 0.03703    # en L/s    mililitro por segundo - Determinado a base de experimentos


def calcular_tiempo(volumen):
    
    Tiempo_de_riego = volumen/Caudal

    return Tiempo_de_riego

