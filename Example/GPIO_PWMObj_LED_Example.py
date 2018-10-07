#########################################################################
# Date: 2018/09/07
# file name: GPIO_PWMObj_LED_Example.py
# Purpose: this code has been generated for control LED Module By Using
# GPIO's PWM class
# if program is run then LED will blink!
#########################################################################

# coding=utf-8
"""
LED를 제어하기 위해 RPi.GPIO 모듈을 GPIO로 import 합니다.
sleep 함수를 사용하기 위해서 time 모듈을 import 합니다.
"""
import time
import RPi.GPIO as GPIO

# Raspberry Pi 핀의 37 번 핀을 led 출력으로 사용합니다.
led_pinR = 37

# Raspberry Pi 핀 순서를 사용하도록 설정합니다.
GPIO.setmode(GPIO.BOARD)

"""
led_pin을 GPIO 출력으로 설정합니다. 이를 통해 led_pin으로
True 혹은 False를 쓸 수 있게 됩니다.
"""
GPIO.setup(led_pinR, GPIO.OUT)

"""
led_pin 으로 출력되는 주파수를 100Hz로 설정한 PWM 객체를 생성합니다.
이후 PWM 동작을 시작합니다. 

인자로 넘어가는 0은 PWM 한 파형 당 HIGH 구간의 길이를 의미하며
0.0 ~ 100.0 사이의 값을 가질 수 있습니다.
"""
pwm = GPIO.PWM(led_pinR, 100)
pwm.start(0)

try:
    while True:
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
KeyboardInterrupt 가 발생하면 PWM 동작을 멈춥니다.
"""
