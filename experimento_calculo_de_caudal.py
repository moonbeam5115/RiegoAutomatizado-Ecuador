import pyfirmata
from pyfirmata import util
import win32api
import time

state_right = win32api.GetKeyState(0x02)  # Right button up = 0 or 1. Button down = -127 or -128

board = pyfirmata.Arduino('COM3')

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

digital_5_output.write(1)

print("Comenzando Experimento Para Determinar Caudal...")
i = 0
while True:
    humedad_sensor_tierra = analog_0_input.read()
    
    print("output 5: ", digital_5_output)
    a = win32api.GetKeyState(0x02)
    if a != state_right:  # Button state changed
        state_right = a
        
        if a < 0:
            if i == 0:
                i += 1
                comienzo = time.time()
                print('Right Button Pressed')
            digital_5_output.write(0)   
        else:
            print('Right Button Released')
            final = time.time()
            digital_5_output.write(1)
            cambio_en_tiempo = final - comienzo
            caudal = volumen_experimental/cambio_en_tiempo
            print(f"El Caudal es: {caudal} L/s")
            exit(0)
