import time
import random
import board
from analogio import AnalogIn


analog_pins = [board.A0, board.A1, board.A2, board.A3]
pots = []
for pin in analog_pins:
    pots.append(AnalogIn(pin))

while True:
    print((pots[0].value,pots[1].value,pots[2].value,pots[3].value,))
    time.sleep(0.1)




