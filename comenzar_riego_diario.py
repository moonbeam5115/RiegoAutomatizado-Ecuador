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
board = pyfirmata.Arduino('COM3')

#iterator thread
it = util.Iterator(board)
it.start()

digital_6_output = board.get_pin('d:6:o')
# 1 is off, 0 is on (Arduino is messed up)
digital_6_output.write(1)
# Initialize parser
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--time", help = "Tiempo de ejecutar")

args = parser.parse_args()
Horario_riego= args.time

CONTINUAR = True

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


def iniciar_riego(t):
     '''
     If you use a pin more often, it can be worth it to use the get_pin method of the board.
     It let's you specify what pin you need by a string, composed of 'a' or 'd' (analog or digital pin),
     the pin number, and the mode ('i' for input, 'o' for output, 'p' for pwm). All seperated by :

     e.g. a:0:i for analog 0 as input, or
          d:3:p for digital pin 3 as pwm.
     ''' 
     # 1 is off, 0 is on (Arduino is messed up)
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
schedule.every().day.at(f"{Horario_riego}").do(iniciar_riego, tiempo)

# Run Program continuously
while CONTINUAR:
     print(f"Comenzando Riego Diario...{datetime.now()}")
     schedule.run_pending()
     time.sleep(5)

fecha_de_hoy = date.today()
fecha_string = fecha_de_hoy.strftime('%d/%m/%Y')
time_now = datetime.now()
current_time = time_now.strftime("%H:%M:%S")
CAMPO_RIEGO = 1
SISTEMA_UTILIZADO = "Manual"

new_data = [fecha_string, current_time, CAMPO_RIEGO, volumen_de_riego, "N/A", "N/A", SISTEMA_UTILIZADO]
filename = 'database/' + 'datos_riego_manual.csv'
actualizar_base_de_datos(filename, new_data)
