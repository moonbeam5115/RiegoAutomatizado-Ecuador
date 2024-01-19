import pyfirmata
import time
from pyfirmata import util

board = pyfirmata.Arduino('COM4')

#iterator thread
it = util.Iterator(board)
it.start()

board.analog[0].enable_reporting()
board.analog[0].read()

'''
If you use a pin more often, it can be worth it to use the get_pin method of the board.
It let's you specify what pin you need by a string, composed of 'a' or 'd' (analog or digital pin),
the pin number, and the mode ('i' for input, 'o' for output, 'p' for pwm). All seperated by :

e.g. a:0:i for analog 0 as input, or
     d:3:p for digital pin 3 as pwm.
'''

analog_0 = board.get_pin('a:0:i')
analog_0.read()

pin3 = board.get_pin('d:3:p')
pin3.write(0.6)


while True:
    # board.digital[13].write(1)
    # time.sleep(0.1)
    # board.digital[13].write(0)
    # time.sleep(0.1)
    print("Sending Info to Arduino...")
    time.sleep(2)
    print("Receiving sensor data from Arduino")
    time.sleep(3)
