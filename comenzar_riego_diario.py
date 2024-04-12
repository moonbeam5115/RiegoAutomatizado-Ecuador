import pyfirmata
import time
from pyfirmata import util
from calcular_datos_met import promedios_datos_met
from calcular_volumen_de_riego import calcular
from calcular_tiempo_de_riego import calcular_tiempo
import schedule
import datetime

data_path = "data/DatosMeteorologicos_Diarios.csv"
tmax, tmin, hr, hr_min, hr_max = promedios_datos_met(path_de_datos=data_path)

volumen_de_riego = calcular(tmax=tmax,
                            tmin=tmin,
                            hr_min=hr_min,
                            hr_max=hr_max) # Returns Volume in L (Liters)

Caudal = 0.03703    # en L/s  -  Determinado a base de experimentos
Caudal_mL = 37.03    # en mililitro por segundo - Determinado a base de experimentos

tiempo = calcular_tiempo(volumen=volumen_de_riego,
                         Caudal=Caudal)

print("Tiempo de riego por Arduino (segundos): ", tiempo)
print("Tiempo de riego por Arduino (minutos): ", tiempo/60)


def determinar_riego(t):
     '''
     If you use a pin more often, it can be worth it to use the get_pin method of the board.
     It let's you specify what pin you need by a string, composed of 'a' or 'd' (analog or digital pin),
     the pin number, and the mode ('i' for input, 'o' for output, 'p' for pwm). All seperated by :

     e.g. a:0:i for analog 0 as input, or
          d:3:p for digital pin 3 as pwm.
     ''' 
     board = pyfirmata.Arduino('COM4')

     #iterator thread
     it = util.Iterator(board)
     it.start()

     digital_6_output = board.get_pin('d:6:o')
     digital_6_output.write(1)
     cambio_en_tiempo = 0
     ahora = time.time()

     while True:
        global CONTINUAR
        print(f"Regando por {t} segundos")
               
        # Ejecutar el program por el tiempo determinado, t
        while cambio_en_tiempo <= t:

            end = time.time()
            cambio_en_tiempo = round(end-ahora)
            digital_6_output.write(0)
        
        CONTINUAR = False
        digital_6_output.write(1)
        break


# Begin Scheduling Logic
schedule.every().day.at("14:00").do(determinar_riego, tiempo)

# Run Program continuously
while CONTINUAR:
     print(f"Comenzando Riego Diario...{datetime.datetime.now()}")
     schedule.run_pending()
     time.sleep(5)
