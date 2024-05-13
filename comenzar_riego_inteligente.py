import pyfirmata
import time
from pyfirmata import util
from calcular_datos_met import promedios_datos_met
from calcular_volumen_de_riego import calcular
from calcular_tiempo_de_riego import calcular_tiempo
import schedule
from datetime import datetime
from datetime import date
from grabar_a_base_de_datos import actualizar_base_de_datos
import argparse
from humedad_mapa_sensor import _map

# Initialize parser
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--time", help = "Tiempo de ejecutar")

args = parser.parse_args()
Horario_riego = args.time

data_path = "data/DatosMeteorologicos_Diarios.csv"
tmax, tmin, hr, hr_min, hr_max = promedios_datos_met(path_de_datos=data_path)

volumen_de_riego = calcular(tmax=tmax,
                            tmin=tmin,
                            hr_min=hr_min,
                            hr_max=hr_max) # Returns Volume in L (Liters)

volumen_optimizado_60_pct = 0.9*volumen_de_riego
volumen_optimizado_80_pct = 0.6*volumen_de_riego

Caudal = 0.03703    # en L/s  -  Determinado a base de experimentos
Caudal_mL = 37.03    # en mililitro por segundo - Determinado a base de experimentos

print("Tiempo de riego por Arduino (segundos): ", tiempo)
print("Tiempo de riego por Arduino (minutos): ", tiempo/60)

CONTINUAR = True
CAMPO_RIEGO = 0
HUMEDAD = 0
HUMEDAD_PARA_REGAR_SUELO = 0.6
PORC_HUMEDAD = 0
volumen_optimizado = 0

def iniciar_riego(v_o_60_pct, v_o_80_pct):
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
          global HUMEDAD
          global CAMPO_RIEGO
          global volumen_optimizado

          humedad_sensor_tierra = analog_0.read()
          if humedad_sensor_tierra is None:
               continue

          if humedad_sensor_tierra < 0.3167:
               humedad_sensor_tierra = 0.3167
          if humedad_sensor_tierra > 0.5582:
               humedad_sensor_tierra = 0.5582

          volumen_optimizado_60_pct = 0.9*volumen_de_riego
          volumen_optimizado_80_pct = 0.6*volumen_de_riego
          porcentaje_humedad_arduino = _map(humedad_sensor_tierra, 0.3167, 0.5582, 100, 0)
               

          if porcentaje_humedad_arduino < HUMEDAD_PARA_REGAR_SUELO:
               print(f"Humedad baja detectada... Comenzando Sesion de Riego por {t} segundos")
               tiempo = calcular_tiempo(volumen=volumen_optimizado_60_pct,
                         Caudal=Caudal)

               CAMPO_RIEGO = 1
               HUMEDAD = humedad_sensor_tierra
               PORC_HUMEDAD = porcentaje_humedad_arduino
               volumen_optimizado = volumen_optimizado_60_pct
               # Ejecutar el program por el tiempo determinado, t
               while cambio_en_tiempo <= t:
                    print("cambio ", cambio_en_tiempo,"tiempo",  t)
                    print("Humedad (%): ", porcentaje_humedad_arduino)
                    end = time.time()
                    cambio_en_tiempo = round(end-ahora)
                    digital_5_output.write(0)
               
               CONTINUAR = False
               digital_5_output.write(1)
               break
          elif porcentaje_humedad_arduino >= HUMEDAD_PARA_REGAR_SUELO and porcentaje_humedad_arduino < 0.8:
               tiempo = calcular_tiempo(volumen=volumen_optimizado_80_pct,
                    Caudal=Caudal)
               CAMPO_RIEGO = 1
               HUMEDAD = humedad_sensor_tierra
               PORC_HUMEDAD = porcentaje_humedad_arduino
               volumen_optimizado = volumen_optimizado_80_pct
               # Ejecutar el program por el tiempo determinado, t
               while cambio_en_tiempo <= t:
                    print("cambio ", cambio_en_tiempo,"tiempo",  t)
                    print("Humedad (%): ", porcentaje_humedad_arduino)
                    end = time.time()
                    cambio_en_tiempo = round(end-ahora)
                    digital_5_output.write(0)
               
               CONTINUAR = False
               digital_5_output.write(1)
               break
          else:
               print("No necesita agua... Finalizando Sesion de Riego.")
               print("Humedad (%): ", porcentaje_humedad_arduino)
               digital_5_output.write(1)
               time.sleep(1)

               HUMEDAD = humedad_sensor_tierra
               PORC_HUMEDAD = porcentaje_humedad_arduino    
               CAMPO_RIEGO = 0
               CONTINUAR = False
               volumen_optimizado = 0
               break
               

# Begin Scheduling Logic
schedule.every().day.at(f"{Horario_riego}").do(iniciar_riego, tiempo)

# Run Program continuously
while CONTINUAR:
     print(f"Analizando Condiciones de Riego...{datetime.now()}")
     schedule.run_pending()
     time.sleep(5)

fecha_de_hoy = date.today()
fecha_string = fecha_de_hoy.strftime('%d/%m/%Y')
time_now = datetime.now()
current_time = time_now.strftime("%H:%M:%S")
SISTEMA_UTILIZADO = "Inteligente"

new_data = [fecha_string, current_time, CAMPO_RIEGO, volumen_optimizado, HUMEDAD, PORC_HUMEDAD, SISTEMA_UTILIZADO]
filename = 'database/' + 'datos_riego_inteligente.csv'
actualizar_base_de_datos(filename, new_data)
