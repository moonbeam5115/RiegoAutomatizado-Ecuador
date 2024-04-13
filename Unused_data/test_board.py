import pyfirmata
from pyfirmata import util

board = pyfirmata.Arduino('COM5')

#iterator thread
it = util.Iterator(board)
it.start()

analog_0 = board.get_pin('a:0:i')
analog_0.enable_reporting()

analog_1 = board.get_pin('a:2:i')
analog_1.enable_reporting()

while True:
    humedad_sensor_tierra = analog_0.read()
    print(humedad_sensor_tierra)
    