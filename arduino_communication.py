import pyfirmata
import time

board = pyfirmata.Arduino('COM4')

while True:
    board.digital[13].write(1)
    time.sleep(0.1)
    board.digital[13].write(0)
    time.sleep(0.1)