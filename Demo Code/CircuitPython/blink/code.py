import time
import board
from digitalio import DigitalInOut, Direction, Pull


LED0 = DigitalInOut(board.GP0)
LED0.switch_to_output()
LED1 = DigitalInOut(board.GP1)
LED1.switch_to_output()
LED2 = DigitalInOut(board.GP2)
LED2.switch_to_output()
LED3= DigitalInOut(board.GP3)
LED3.switch_to_output()
LED4 = DigitalInOut(board.GP4)
LED4.switch_to_output()
LED5 = DigitalInOut(board.GP5)
LED5.switch_to_output()
LED6 = DigitalInOut(board.GP6)
LED6.switch_to_output()
LED7 = DigitalInOut(board.GP7)
LED7.switch_to_output()
LED20 = DigitalInOut(board.GP20)
LED20.switch_to_output()


LED21 = DigitalInOut(board.GP21)
LED21.switch_to_output()
LED22 = DigitalInOut(board.GP22)
LED22.switch_to_output()
LED23= DigitalInOut(board.GP23)
LED23.switch_to_output()
LED24 = DigitalInOut(board.GP24)
LED24.switch_to_output()
LED25 = DigitalInOut(board.GP25)
LED25.switch_to_output()
LED26 = DigitalInOut(board.GP26)
LED26.switch_to_output()
LED27 = DigitalInOut(board.GP27)
LED27.switch_to_output()
LED28 = DigitalInOut(board.GP28)
LED28.switch_to_output()
LED29 = DigitalInOut(board.A3)
LED29.switch_to_output()





while True:
    LED0.value = True
    LED1.value = True
    LED2.value = True
    LED3.value = True
    LED4.value = True
    LED5.value = True
    LED6.value = True
    LED7.value = True
    LED20.value = True
    LED21.value = True
    LED22.value = True
    LED23.value = True
    LED24.value = True
    LED25.value = True
    LED26.value = True
    LED27.value = True
    LED28.value = True
    LED29.value = True

    time.sleep(0.5)

    LED0.value = False
    LED1.value = False
    LED2.value = False
    LED3.value = False
    LED4.value = False
    LED5.value = False
    LED6.value = False
    LED7.value = False
    LED20.value = False
    LED21.value = False
    LED22.value = False
    LED23.value = False
    LED24.value = False
    LED25.value = False
    LED26.value = False
    LED27.value = False
    LED28.value = False
    LED29.value = False

    time.sleep(0.5)
