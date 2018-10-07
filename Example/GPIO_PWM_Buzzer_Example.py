#########################################################################
# Date: 2018/09/07
# file name: GPIO_PWM_Buzzer_Example.py
# Purpose: this code has been generated for control Buzzer Module
# if program is run then buzzer will make sound!
#########################################################################

# coding=utf-8
"""
Buzzer 를 제어하기 위해 RPi.GPIO 모듈을 GPIO로 import 합니다.
sleep 함수를 사용하기 위해서 time 모듈을 import 합니다.
"""
import time
import RPi.GPIO as GPIO

# Raspberry Pi의 핀 번호를 의미합니다.
buzzer_pin = 8

# Raspberry Pi의 핀 순서를 사용하도록 설정합니다.
GPIO.setmode(GPIO.BOARD)

"""
음계별 표준 주파수
[ 도, 레, 미, 파, 솔, 라, 시, 도]
"""
scale = [261.6, 293.6, 329.6, 349.2, 391.9, 440.0, 493.8, 523.2]

"""
buzzer_pin 을 GPIO 출력으로 설정합니다. 이를 통해 led_pin으로
True 혹은 False를 쓸 수 있게 됩니다.
"""
GPIO.setup(buzzer_pin, GPIO.OUT)

try:
    p = GPIO.PWM(buzzer_pin, 100)
    p.start(5)     # start the PWM on 5% duty cycle

    for i in range(8):
        print (i + 1)
        p.ChangeFrequency(scale[i])
        time.sleep(0.5)

    p.stop()  # stop the PWM output

finally:
    GPIO.cleanup()
