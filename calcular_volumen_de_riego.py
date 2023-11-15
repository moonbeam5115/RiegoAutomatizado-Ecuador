humedad_relative = 0
sat_spec_hum = 10
R_n = 5
G = 0
d_air_dens = 3
spec_heat = 14
vapor_pressure = 1
g_a = 4.6
velocidad_de_agua = 1        # en L/s    mililitro por segundo


numerador = sat_spec_hum*(R_n - G) + d_air_dens*spec_heat(vapor_pressure)*g_a
denominador = a + b + c

ET = numerador/denominador

Volumen_de_riego = ET*2   # Litros

Tiempo_de_riego = Volumen_de_riego/velocidad_de_agua   # Segundos

