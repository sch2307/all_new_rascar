#########################################################################
# Date: 2018/09/07
# file name: GPIO_PWM_LED_Example.py
# Purpose: this code has been generated for contorl LED Module
# if program is run then LED will blink!
#########################################################################

# coding=utf-8
"""
LED를 제어하기 위해 RPi.GPIO 모듈을 GPIO로 import 합니다.
sleep 함수를 사용하기 위해서 time 모듈을 import 합니다.
"""
import time
import RPi.GPIO as GPIO

# Raspberry Pi 의 37번 핀 번호를 의미합니다.
led_pinR = 37

# Raspberry Pi 의 핀 순서를 사용하도록 설정합니다.
GPIO.setmode(GPIO.BOARD)

"""
led_pin을 GPIO 출력으로 설정합니다. 이를 통해 led_pin으로
True 혹은 False를 쓸 수 있게 됩니다.
"""
GPIO.setup(led_pinR, GPIO.OUT)

# 1s = 1000ms
try:
    while True:
        time.sleep(0.01)
        for sec in range(0, 101, 1):
            """
            for 문을 통해 증가하는 초를 밀리초 단위로
            변환하여 지연시간을 준다.
            """
            milisec = sec * 0.0001
            """
            100Hz의 주파수로 점멸하는 LED의 밝기를 
            조절하기위해 상하비를 조절한다.
            """
            GPIO.output(led_pinR, True)
            time.sleep(milisec)
            GPIO.output(led_pinR, False)
            time.sleep(0.01 - milisec)

        for sec in range(100, -1, -1):
            milisec = sec * 0.0001
            GPIO.output(led_pinR, True)
            time.sleep(milisec)
            GPIO.output(led_pinR, False)
            time.sleep(0.01 - milisec)


except KeyboardInterrupt:
    GPIO.cleanup()

"""
control + c 키를 눌러서 KeyboardInterrupt를 발생시키면
GPIO.cleanup()을 호출하여 GPIO를 초기 상태로 돌려놓습니다.
"""
