import pyfirmata
from pyfirmata import util
import win32api
import time

state_left = win32api.GetKeyState(0x01)  # Left button up = 0 or 1. Button down = -127 or -128

board = pyfirmata.Arduino('COM5')

#iterator thread
it = util.Iterator(board)
it.start()

analog_0_input = board.get_pin('a:0:i')
analog_0_input.enable_reporting()

digital_5_output = board.get_pin('d:5:o')

comienzo = None
final = None
cambio_en_tiempo = 0
caudal = 0
volumen_experimental = 1

print("Comenzando Experimento Para Determinar Caudal...")
while True:
    humedad_sensor_tierra = analog_0_input.read()
    
    a = win32api.GetKeyState(0x01)
    if a != state_left:  # Button state changed
        state_left = a
        
        if a < 0:
            comienzo = time.time()
            digital_5_output.write(1)
        else:
            final = time.time()
            digital_5_output.write(0)
            cambio_en_tiempo = final - comienzo
            caudal = volumen_experimental/cambio_en_tiempo
            print(f"El Caudal es: {caudal} L/s")
