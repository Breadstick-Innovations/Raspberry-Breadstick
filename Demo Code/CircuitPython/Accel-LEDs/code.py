import time
import board
import digitalio
import busio
import random
##Gyro
from adafruit_lsm6ds import Rate, AccelRange, GyroRange
# from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
# from adafruit_lsm6ds.lsm6ds33 import LSM6DS33 as LSM6DS
# from adafruit_lsm6ds.lsm6dso32 import LSM6DSO32 as LSM6DS
# from adafruit_lsm6ds.ism330dhcx import ISM330DHCX as LSM6DS
from adafruit_lsm6ds.lsm6ds3trc import LSM6DS3TRC as LSM6DS
#dotstar
import adafruit_dotstar as dotstar
import adafruit_fancyled.adafruit_fancyled as fancy

# definitions
IMU_SCL = board.GP17
IMU_SDA = board.GP16


### setup Gyro
i2c = busio.I2C(IMU_SCL,IMU_SDA)
sensor = LSM6DS(i2c)

sensor.accelerometer_range = AccelRange.RANGE_4G
print("Accelerometer range set to: %d G" % AccelRange.string[sensor.accelerometer_range])

sensor.gyro_range = GyroRange.RANGE_1000_DPS
print("Gyro range set to: %d DPS" % GyroRange.string[sensor.gyro_range])

sensor.accelerometer_data_rate = Rate.RATE_1_66K_HZ
print("Accelerometer rate set to: %d HZ" % Rate.string[sensor.accelerometer_data_rate])

sensor.gyro_data_rate = Rate.RATE_1_66K_HZ
print("Gyro rate set to: %d HZ" % Rate.string[sensor.gyro_data_rate])


## Gyro not reqired for Pedometer
#sensor.gyro_data_rate = Rate.RATE_SHUTDOWN
## Enable pedometer
#sensor.pedometer_enable = True


def random_color():
    return random.randrange(0, 7) * 32
num_leds = 24
data_pin = board.GP19
clock_pin = board.GP18
dots = dotstar.DotStar(board.GP18, board.GP19, num_leds, brightness=1.0, auto_write=False)

offset = 0  # Positional offset into color palette to get it to 'spin'


while True:
    ##pedometer
    #print("Steps: ", sensor.pedometer_steps)
    #time.sleep(1)

    #print(sensor.temperature)

    acc_x, acc_y, acc_z = sensor.acceleration
    gyro_x, gyro_z, gyro_z = sensor.gyro

    ### accel and Gyro stuff
    # print(
        # "Accel X:%.2f Y:%.2f Z:%.2f ms^2 Gyro X:%.2f Y:%.2f Z:%.2f radians/s"
        # % (sensor.acceleration + sensor.gyro)
    # )

    #print(sensor.acceleration)
    #print("Y:%.2f" % acc_y)
    ##  -10-10 --> 0-24
    myVal = int ((acc_y + 10 )/20 * 24 )
    #print("val:%i" % myVal)
    #print("(%.2f, %.0f)" % (acc_y, myVal))

    # print(sensor.gyro)

    # print("(%f, %f, %f, %f, %f, %f)" % (sensor.acceleration + sensor.gyro))
    #time.sleep(0.05)



    for i in range(num_leds):
        if i == myVal:
            c = fancy.CRGB(fancy.CHSV(i/num_leds+offset,1.0,0.05))
        elif i+1 == myVal:
            c = fancy.CRGB(fancy.CHSV(i/num_leds+offset,0.50,0.01))
        elif i-1 == myVal:
            c = fancy.CRGB(fancy.CHSV(i/num_leds+offset,0.50,0.01))
        else:
            c = fancy.CRGB(0,0,0)
        dots[i] = c.pack()
    dots.show()

    offset += 0.0  # Bigger number = faster spin. was 0.02
    time.sleep(0.01)
