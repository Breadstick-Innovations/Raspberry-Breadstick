# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# Dotstar painter! Can handle up to ~2300 pixel size image (e.g. 36 x 64)

import gc
import time

import board
import busio
import bitbangio
import digitalio
from adafruit_lsm6ds import Rate, AccelRange, GyroRange
from adafruit_lsm6ds.lsm6ds3trc import LSM6DS3TRC as LSM6DS

i2c = busio.I2C(board.IMU_SCL, board.IMU_SDA)
IMU = LSM6DS(i2c)

IMU.accelerometer_range = AccelRange.RANGE_4G
print("Accelerometer range set to: %d G" % AccelRange.string[IMU.accelerometer_range])

IMU.gyro_range = GyroRange.RANGE_1000_DPS
print("Gyro range set to: %d DPS" % GyroRange.string[IMU.gyro_range])

IMU.accelerometer_data_rate = Rate.RATE_1_66K_HZ
print("Accelerometer rate set to: %d HZ" % Rate.string[IMU.accelerometer_data_rate])

IMU.gyro_data_rate = Rate.RATE_1_66K_HZ
print("Gyro rate set to: %d HZ" % Rate.string[IMU.gyro_data_rate])


FILENAME = "CrowdSupply2.bmp"

IMAGE_DELAY = 0.001
REPEAT = True
BRIGHTNESS = 0.25
PIXEL_DELAY = 0.001

dotstar = bitbangio.SPI(board.DOTSTAR_CLOCK, board.DOTSTAR_DATA)
while not dotstar.try_lock():
    pass
dotstar.configure(baudrate=12000000)

# we'll resize this later
databuf = bytearray(0)

led = digitalio.DigitalInOut(board.D13)
led.switch_to_output()


def read_le(s):
    # as of this writting, int.from_bytes does not have LE support, DIY!
    result = 0
    shift = 0
    for byte in bytearray(s):
        result += byte << shift
        shift += 8
    return result


class BMPError(Exception):
    pass


try:
    with open("/" + FILENAME, "rb") as f:
        print("File opened")
        if f.read(2) != b'BM':  # check signature
            raise BMPError("Not BitMap file")

        bmpFileSize = read_le(f.read(4))
        f.read(4)  # Read & ignore creator bytes

        bmpImageoffset = read_le(f.read(4))  # Start of image data
        headerSize = read_le(f.read(4))
        bmpWidth = read_le(f.read(4))
        bmpHeight = read_le(f.read(4))
        flip = True

        print("Size: %d\nImage offset: %d\nHeader size: %d" %
              (bmpFileSize, bmpImageoffset, headerSize))
        print("Width: %d\nHeight: %d" % (bmpWidth, bmpHeight))

        if read_le(f.read(2)) != 1:
            raise BMPError("Not singleplane")
        bmpDepth = read_le(f.read(2))  # bits per pixel
        print("Bit depth: %d" % (bmpDepth))
        if bmpDepth != 24:
            raise BMPError("Not 24-bit")
        if read_le(f.read(2)) != 0:
            raise BMPError("Compressed file")

        print("Image OK!")

        rowSize = (bmpWidth * 3 + 3) & ~3  # 32-bit line boundary

        # its huge! but its also fast :)
        databuf = bytearray(bmpWidth * bmpHeight * 4)

        for row in range(bmpHeight):  # For each scanline...
            if flip:  # Bitmap is stored bottom-to-top order (normal BMP)
                pos = bmpImageoffset + (bmpHeight - 1 - row) * rowSize
            else:  # Bitmap is stored top-to-bottom
                pos = bmpImageoffset + row * rowSize

            # print ("seek to %d" % pos)
            f.seek(pos)
            for col in range(bmpWidth):
                b, g, r = bytearray(f.read(3))  # BMP files store RGB in BGR
                # front load brightness, gamma and reordering here!
                order = [b, g, r]
                idx = (col * bmpHeight + (bmpHeight - row - 1)) * 4
                databuf[idx] = 0xFF  # first byte is 'brightness'
                idx += 1
                for color in order:
                    databuf[idx] = int(
                        pow((color * BRIGHTNESS) / 255, 2.7) * 255 + 0.5)
                    idx += 1

except OSError as e:
    if e.args[0] == 28:
        raise OSError("OS Error 28 0.25")
    else:
        raise OSError("OS Error 0.5")
except BMPError as e:
    print("Failed to parse BMP: " + e.args[0])

gc.collect()
print(gc.mem_free())
print("Ready to go!")
while True:
    #print("Draw!")
    index = 0

    #acc_x, acc_y, acc_z = IMU.acceleration
    gyro_x, gyro_z, gyro_z = IMU.gyro
    #print(gyro_z)
    #time.sleep(0.05)



    if(gyro_z<0):
        for col in range(bmpWidth):
            gyro_x, gyro_z, gyro_z = IMU.gyro
            if(gyro_z<0):
                pass
            else:
                break
            index = bmpHeight * 4 * col
            row = databuf[index:index + bmpHeight * 4]
            dotstar.write(bytearray([0x00, 0x00, 0x00, 0x00]))
            dotstar.write(row)
            dotstar.write(bytearray([0x00, 0x00, 0x00, 0x00]))
            #index += bmpHeight * 4
            if(abs(gyro_z)<0.001): gyro_z = 0.001
            time.sleep(abs(PIXEL_DELAY/gyro_z))

    else:
        for col in range(bmpWidth,-1,-1):
            gyro_x, gyro_z, gyro_z = IMU.gyro
            if(gyro_z<0):
                break
            else:
                pass
            index = bmpHeight * 4 * col
            row = databuf[index:index + bmpHeight * 4]
            dotstar.write(bytearray([0x00, 0x00, 0x00, 0x00]))
            dotstar.write(row)
            dotstar.write(bytearray([0x00, 0x00, 0x00, 0x00]))
            #index += bmpHeight * 4
            if(abs(gyro_z)<0.001): gyro_z = 0.001
            time.sleep(abs(PIXEL_DELAY/gyro_z))


    # clear it out
    dotstar.write(bytearray([0x00, 0x00, 0x00, 0x00]))
    for r in range(bmpHeight * 5):
        dotstar.write(bytearray([0xFF, 0x00, 0x00, 0x00]))
    dotstar.write(bytearray([0xff, 0xff, 0xff, 0xff]))
    gc.collect()

    if not REPEAT:
        break

    time.sleep(IMAGE_DELAY)
