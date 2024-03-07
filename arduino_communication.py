import pyfirmata
import time
from pyfirmata import util
import calcular_volumen_de_riego
import calcular_tiempo_de_riego
import schedule
import datetime

volumen_de_agua = calcular_volumen_de_riego.calcular()

tiempo = calcular_tiempo_de_riego.calcular_tiempo(volumen=volumen_de_agua)
CONTINUAR = True

def determinar_riego(t):
     '''
     If you use a pin more often, it can be worth it to use the get_pin method of the board.
     It let's you specify what pin you need by a string, composed of 'a' or 'd' (analog or digital pin),
     the pin number, and the mode ('i' for input, 'o' for output, 'p' for pwm). All seperated by :

     e.g. a:0:i for analog 0 as input, or
          d:3:p for digital pin 3 as pwm.
     ''' 
     board = pyfirmata.Arduino('COM3')

     #iterator thread
     it = util.Iterator(board)
     it.start()

     analog_0 = board.get_pin('a:0:i')
     analog_0.enable_reporting()

     analog_1 = board.get_pin('a:2:i')
     analog_1.enable_reporting()

     digital_5_output = board.get_pin('d:5:o')
     digital_5_output.write(1)
     cambio_en_tiempo = 0
     ahora = time.time()

     while True:
          global CONTINUAR
          humedad_sensor_tierra = analog_0.read()
          humedad_sensor_aire = analog_1.read()
          

          if humedad_sensor_tierra is not None and humedad_sensor_tierra < 0.9:
               print(f"Humedad baja detectada... Comenzando Sesion de Riego por {t} segundos")
               
               # Ejecutar el program por el tiempo determinado, t
               while cambio_en_tiempo <= t:
                    print(cambio_en_tiempo, t)
                    end = time.time()
                    cambio_en_tiempo = round(end-ahora)
                    digital_5_output.write(0)
               
               CONTINUAR = False
               digital_5_output.write(1)
               break
          if humedad_sensor_tierra is not None and humedad_sensor_tierra >= 1.0:
               print(humedad_sensor_tierra)
               print("No necesita agua... Finalizando Sesion de Riego.")
               digital_5_output.write(1)
               time.sleep(1)

               CONTINUAR = False
               break
               

# Begin Scheduling Logic
schedule.every().day.at("23:35").do(determinar_riego, tiempo)


# Run Program continuously
while CONTINUAR:
     print(f"Analizando Condiciones de Riego...{datetime.datetime.now()}")
     schedule.run_pending()
     time.sleep(5)
