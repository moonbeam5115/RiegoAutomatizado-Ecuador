import pyfirmata
import time
from pyfirmata import util

board = pyfirmata.Arduino('COM5')

#iterator thread
it = util.Iterator(board)
it.start()

'''
If you use a pin more often, it can be worth it to use the get_pin method of the board.
It let's you specify what pin you need by a string, composed of 'a' or 'd' (analog or digital pin),
the pin number, and the mode ('i' for input, 'o' for output, 'p' for pwm). All seperated by :

e.g. a:0:i for analog 0 as input, or
     d:3:p for digital pin 3 as pwm.
'''

analog_0 = board.get_pin('a:0:i')
analog_0.enable_reporting()

analog_1 = board.get_pin('a:2:i')
analog_1.enable_reporting()


while True:
     humedad_sensor_0 = analog_0.read()
     humedad_sensor_1 = analog_1.read()
     
     if humedad_sensor_0 is None:
          continue
     if humedad_sensor_1 is None:
          continue

     # if humedad_sensor_0 > 0.5:
     #      print("Regando Agua")
     # else:
     #      print("No se riega...")
     
     print("Sensor 1: ", humedad_sensor_0)
     print("Sensor 2: ", humedad_sensor_1)

     time.sleep(1)
    
