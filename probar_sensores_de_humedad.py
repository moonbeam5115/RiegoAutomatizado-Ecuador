import pyfirmata
from pyfirmata import util
import time

board = pyfirmata.Arduino('COM4')

#iterator thread
it = util.Iterator(board)
it.start()

analog_0_input = board.get_pin('a:0:i')
analog_0_input.enable_reporting()

while True:
    humedad_sensor_tierra = analog_0_input.read()
    
    print("humedad :", humedad_sensor_tierra)

    time.sleep(1)
