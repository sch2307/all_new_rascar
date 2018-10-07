#########################################################################
# Date: 2018/07/12
# file name: trackingModule.py
# Purpose: this code has been generated for the five-way tracking sensor
#          to perform the decision of direction
#########################################################################

# =======================================================================
# import GPIO library and time module
# =======================================================================
import RPi.GPIO as GPIO
import time


class SEN040134_Tracking(object):
    # =======================================================================
    #  channel initializing
    # =======================================================================

    def __init__(self, channel):
        # =======================================================================
        # set up GPIO mode as BOARD
        # =======================================================================
        GPIO.setmode(GPIO.BOARD)

        # =======================================================================
        # because the connections between 5-way tracking sensor and Raspberry Pi has been
        # established, the GPIO pins of Raspberry Pi
        # such as leftmostled, leftlessled, centerled, rightlessled, and rightmostled
        # should be clearly declared whether their roles of pins
        # are output pin or input pin
        # since the 5-way tracking sensor data has been detected and
        # used as the input data, leftmostled, leftlessled, centerled, rightlessled, and rightmostled
        # should be clearly declared as input
        #
        # =======================================================================

        self.gpio_channel = channel

        for i in range(0, 5):
            GPIO.setup(self.gpio_channel[i], GPIO.IN)

    # =======================================================================
    # GPIO.input(leftmostled) method gives the data obtained from leftmostled
    # gpio_channel >> 0 returns (1) : leftmostled detects white playground
    # gpio_channel >> 0 returns (0) : leftmostled detects black line
    #
    # GPIO.input(leftlessled) method gives the data obtained from leftlessled
    # gpio_channel >> 1  returns (1) : leftlessled detects white playground
    # gpio_channel >> 1  returns (0) : leftlessled detects black line
    #
    # GPIO.input(centerled) method gives the data obtained from centerled
    # gpio_channel >> 2  returns (1) : centerled detects white playground
    # gpio_channel >> 2  returns (0) : centerled detects black line
    #
    # GPIO.input(rightlessled) method gives the data obtained from rightlessled
    # gpio_channel >> 3  returns (1) : rightlessled detects white playground
    # gpio_channel >> 3  returns (0) : rightlessled detects black line
    #
    # GPIO.input(rightmostled) method gives the data obtained from rightmostled
    # gpio_channel >> 4  returns (1) : rightmostled detects white playground
    # gpio_channel >> 4  returns (0) : rightmostled detects black line
    #
    # =======================================================================
    def read_digital(self):
        digital_list = []
        for i in range(0, 5):
            temp = GPIO.input(self.gpio_channel[i])
            digital_list.append(0 if temp == 1 else 1)
        return digital_list

    def is_in_line(self):
        lt_status = self.read_digital()
        if 1 in lt_status:
            return True
        else:
            return False

    def is_equal_status(self, status):
        lt_status = self.read_digital()
        if lt_status == status:
            return True
        else:
            return False

    def is_center(self):
        lt_status = self.read_digital()
        if lt_status[2] == 1:
            return True
        else:
            return False
