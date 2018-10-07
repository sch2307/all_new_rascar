#!/usr/bin/env python
import time
import RPi.GPIO as GPIO


class Supersonic_Sensor(object):
    timeout = 0.1

    def __init__(self, channel):
        self.channel = channel
        GPIO.setmode(GPIO.BOARD)

    def get_distance(self):
        pulse_end = 0
        pulse_start = 0
        GPIO.setup(self.channel, GPIO.OUT)
        GPIO.output(self.channel, False)
        time.sleep(0.01)
        GPIO.output(self.channel, True)
        time.sleep(0.00001)
        GPIO.output(self.channel, False)
        GPIO.setup(self.channel, GPIO.IN)

        timeout_start = time.time()
        while GPIO.input(self.channel) == 0:
            pulse_start = time.time()
            if pulse_start - timeout_start > self.timeout:
                return -1
        while GPIO.input(self.channel) == 1:
            pulse_end = time.time()
            if pulse_start - timeout_start > self.timeout:
                return -1

        if pulse_start != 0 and pulse_end != 0:
            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 100 * 343.0 / 2
            distance = int(distance)
            # print 'start = %s'%pulse_start,
            # print 'end = %s'%pulse_end
            if distance >= 0:
                return distance
            else:
                return -1
        else:
            # print 'start = %s'%pulse_start,
            # print 'end = %s'%pulse_end
            return -1
