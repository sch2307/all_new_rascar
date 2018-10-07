#########################################################################
# Date: 2018/08/07
# file name: GPIO_Button_LED_Example.py
# Purpose: this code has been generated for control Button & LED Module
# if Button is pressed then Led will blink by using PWM Contorl
#########################################################################

# coding=utf-8
import time
import RPi.GPIO as GPIO

# Raspberry Pi 3번 핀을 버튼 입력으로 사용합니다.
# 37번 핀을 LED 출력으로 사용합니다.
button_pin = 3
led_pinR = 37

# Raspberry Pi 핀 순서를 사용하도록 설정합니다.
GPIO.setmode(GPIO.BOARD)

# button_pin을 GPIO 입력으로 설정합니다.
# led_pin을 GPIO 출력으로 설정합니다.
GPIO.setup(button_pin, GPIO.IN)
GPIO.setup(led_pinR, GPIO.OUT)

# led_pin을 100Hz의 주파수로 제어하는 PWM 객체를 생성합니다.
pwm = GPIO.PWM(led_pinR, 100)
# dutycycle 은 0으로 설정하고 제어를 시작합니다.
pwm.start(0)

try:
    '''
    계속 반복해서 button_pin의 상태를 읽어 
    buttonInput 변수에 저장합니다.
    '''

    while True:
        """
        button_pin 값을 읽어 buttonInput 에 저장합니다.
        """
        button_input = GPIO.input(button_pin)


        # 버튼이 눌려져 있는 상태인지 계속해서 확인하는 이벤트 루프
        if not button_input:
            print("Button Pressed")

            for t_high in range(0, 101, 1):
                """
                ChangeDutyCycle()을 호출하여 PWM 파형의 HIGH 구간을 
                t_high 만큼으로 설정한다. 인자는 0.0~100.0 사이의 값을
                받을 수 있다.
                """
                pwm.ChangeDutyCycle(t_high)
                time.sleep(0.01)  # 10ms

            for t_high in range(100, -1, -1):
                pwm.ChangeDutyCycle(t_high)
                time.sleep(0.01)


except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()

"""
KeyboardInterrupt가 발생하면 핀 설정 상태를 초기화 합니다.
"""
