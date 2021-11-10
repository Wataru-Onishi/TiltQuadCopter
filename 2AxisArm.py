# coding: utf-8

import RPi.GPIO as GPIO             
import time                         
import sys                        
import smbus
import math


########################################################
#MPU6050の設定と関数
DEV_ADDR = 0x68

ACCEL_XOUT = 0x3b
ACCEL_YOUT = 0x3d
ACCEL_ZOUT = 0x3f
TEMP_OUT = 0x41
GYRO_XOUT = 0x43
GYRO_YOUT = 0x45
GYRO_ZOUT = 0x47

PWR_MGMT_1 = 0x6b
PWR_MGMT_2 = 0x6c  

bus = smbus.SMBus(1)
bus.write_byte_data(DEV_ADDR, PWR_MGMT_1, 0)

def read_word(adr):
    high = bus.read_byte_data(DEV_ADDR, adr)
    low = bus.read_byte_data(DEV_ADDR, adr+1)
    val = (high << 8) + low
    return val

def read_word_sensor(adr):
    val = read_word(adr)
    if (val >= 0x8000):         # minus
        return -((65535 - val) + 1)
    else:                       # plus
        return val

def getGyro():
    x = read_word_sensor(GYRO_XOUT)/ 131.0
    y = read_word_sensor(GYRO_YOUT)/ 131.0
    z = read_word_sensor(GYRO_ZOUT)/ 131.0
    return [x, y, z]

def getAccel():
    x = read_word_sensor(ACCEL_XOUT)/ 16384.0
    y= read_word_sensor(ACCEL_YOUT)/ 16384.0
    z= read_word_sensor(ACCEL_ZOUT)/ 16384.0
    return [x, y, z]

########################################################
#サーボモータの設定と関数
#ポート番号の定義
X_Servo_pin = 23                      
Y_Servo_pin = 24                     

#GPIOの設定
GPIO.setmode(GPIO.BCM)              
GPIO.setup(X_Servo_pin, GPIO.OUT)  
GPIO.setup(Y_Servo_pin, GPIO.OUT)  

#PWMの設定
#サーボモータSG90の周波数は50[Hz]
Servo = GPIO.PWM(X_Servo_pin, 50)    
Servo = GPIO.PWM(Y_Servo_pin, 50)     

Servo.start(0)                     


def X_servo_angle(X_angle):
    duty = 2.5 + (12.0 - 2.5) * (X_angle + 90) / 180   
    Servo.ChangeDutyCycle(duty)     
    # time.sleep(0.3)     

def Y_servo_angle(Y_angle):
    duty = 2.5 + (12.0 - 2.5) * (Y_angle + 90) / 180   
    Servo.ChangeDutyCycle(duty)     
    # time.sleep(0.3)     



#########################################################
#メイン関数
def main():
    while True:
        try:
            ax, ay, az = getAccel()

            roll = -math.asin(ay/math.sqrt((az**2)+(ay**2))) * 57.324
            pitch = -math.asin(ax/math.sqrt((az**2)+(ax**2))) * 57.324
            r_roll = round(roll)
            r_pitch = round(pitch)

            X_servo_angle(r_roll)


            print('{:4.3f}, {:4.3f},' .format(roll, pitch))



        except KeyboardInterrupt:          
            Servo.stop()                
            GPIO.cleanup()                
            sys.exit()                  


if __name__ == "__main__":
    main()




