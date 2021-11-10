# coding: utf-8

import RPi.GPIO as GPIO             
import time                         
import sys                        
import math



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

def Y_servo_angle(Y_angle):
    duty = 2.5 + (12.0 - 2.5) * (Y_angle + 90) / 180   
    Servo.ChangeDutyCycle(duty)     


#########################################################
#メイン関数
def main():
    while True:
        try:

            X_servo_angle(90)
            time.sleep(0.3)
            X_servo_angle(85)
            time.sleep(0.3)




        except KeyboardInterrupt:          
            Servo.stop()                
            GPIO.cleanup()                
            sys.exit()                  


if __name__ == "__main__":
    main()

