#########################################################################
# Date: 2018/09/07
# file name: GPIO_Button_Example.py
# Purpose: This code has been generated for control Button Module
# if Button is Pressed then console print '0' else console print '1'
#########################################################################

# coding=utf-8
import RPi.GPIO as GPIO
import time

# Raspberry Pi 3번 핀을 버튼 입력으로 사용합니다.
button_pin = 3

# Raspberry Pi 보드의 핀 순서를 사용합니다.
GPIO.setmode(GPIO.BOARD)

# button_pin을 GPIO 입력으로 설정합니다.
GPIO.setup(button_pin, GPIO.IN)

try:
    '''
    계속 반복해서 button_pin의 상태를 읽어 
    buttonInput 변수에 저장합니다.
    '''
    before_input = 0
    while True:
        """
        button_pin 값을 읽어 buttonInput 에 저장합니다.
        """
        button_input = GPIO.input(button_pin)
        if (button_input != before_input):
            print(button_input)
        before_input = button_input


except KeyboardInterrupt:
    GPIO.cleanup()

"""
KeyboardInterrupt가 발생하면 핀 설정 상태를 초기화 합니다.
"""
