import time
import random
import board
import busio

IMU_SCL = board.GP17
IMU_SDA = board.GP16
IMU_INT1 = board.GP12
IMU_INT2 = board.GP13
IMU_I2C_ADDR = 0x6A

i2c = busio.I2C(IMU_SCL, IMU_SDA)  # SCL, SDA




CTRL1_XL = 0x10
CTRL2_G = 0x11
CTRL3_C = 0x12
CTRL4_C = 0x13
CTRL5_C = 0x14
CTRL6_C = 0x15

OUT_TEMP_L = 0x20
OUT_TEMP_H = 0x21

OUTX_L_G = 0x22
OUTX_H_G = 0x23

OUTX_L_XL = 0x28
OUTX_H_XL = 0x29


def i2c_read_reg(i2cbus, addr, reg, result):
  while not i2cbus.try_lock():
    pass
  try:
    i2cbus.writeto_then_readfrom(addr, bytes([reg]), result)
    return result
  finally:
    i2cbus.unlock()
    return None

def i2c_write_reg(i2cbus, addr, reg, data):
  while not i2cbus.try_lock():
    pass
  try:
    buf = bytearray(1)
    buf[0] = reg
    buf.extend(data)
    i2cbus.writeto(addr, buf)
  finally:
    i2cbus.unlock()

def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is

data = bytearray(1)

data[0] = 0b00111100
i2c_write_reg(i2c, IMU_I2C_ADDR, CTRL1_XL, data)

data[0] = 0b00111000
i2c_write_reg(i2c, IMU_I2C_ADDR, CTRL2_G, data)


while True:
    x_lowbyte = bytearray(1)
    i2c_read_reg(i2c, IMU_I2C_ADDR, OUTX_L_XL, x_lowbyte)
    x_highbyte = bytearray(1)
    i2c_read_reg(i2c, IMU_I2C_ADDR, OUTX_H_XL, x_highbyte)
    x = twos_comp(x_highbyte[0]*256 + x_lowbyte[0], 16)

    pitch_lowbyte = bytearray(1)
    i2c_read_reg(i2c, IMU_I2C_ADDR, OUTX_L_G, pitch_lowbyte)
    pitch_highbyte = bytearray(1)
    i2c_read_reg(i2c, IMU_I2C_ADDR, OUTX_H_G, pitch_highbyte)
    pitch = twos_comp(pitch_highbyte[0]*256 + pitch_lowbyte[0], 16)

    temp_lowbyte = bytearray(1)
    i2c_read_reg(i2c, IMU_I2C_ADDR, OUT_TEMP_L, temp_lowbyte)
    temp_highbyte = bytearray(1)
    i2c_read_reg(i2c, IMU_I2C_ADDR, OUT_TEMP_H, temp_highbyte)
    temp = 25 + twos_comp(temp_highbyte[0]*256 + temp_lowbyte[0], 16) /256



    print((x,pitch,temp))
    time.sleep(0.1)










