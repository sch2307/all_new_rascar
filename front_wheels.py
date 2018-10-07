#!/usr/bin/env python
from PCA9685 import Servo
import filedb


class Front_Wheels(object):
    """ Front wheels control class """
    FRONT_WHEEL_CHANNEL = 0

    _DEBUG = False
    _DEBUG_INFO = 'DEBUG "front_wheels.py":'

    def __init__(self, db="config", bus_number=1, channel=FRONT_WHEEL_CHANNEL):
        """ setup channels and basic stuff """
        self.db = filedb.fileDB(db=db)
        self._channel = channel
        self._straight_angle = 90
        self.turning_max = 20
        self._turning_offset = int(self.db.get('turning_offset', default_value=0))

        self.wheel = Servo.Servo(self._channel, bus_number=bus_number, offset=self.turning_offset)
        self.debug = int(self.db.get("debug", default_value=0))
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Front wheel PWM channel:', self._channel)
            print(self._DEBUG_INFO, 'Front wheel offset value:', self.turning_offset)

        self._angle = {"left": self._min_angle, "straight": self._straight_angle, "right": self._max_angle}
        if self._DEBUG:
            print(self._DEBUG_INFO, 'left angle: {}, straight angle: {}, right angle: {}'
                  .format(self._angle["left"], self._angle["straight"], self._angle["right"]))

    def turn_left(self, angle):
        """ Turn the front wheels left """
        """ Available angle : 0 ~ 89 degrees """
        if self._DEBUG:
            print(self._DEBUG_INFO, "Turn left")
        if 0 <= angle < 90: # max angle
            if angle < self._angle["left"]:
                angle = self._angle["left"]
            self.wheel.write(angle)
        else:
            print('[ERROR-400] You have exceeded the turn angle range to the left : {}'.format(angle))

    def center_alignment(self):
        """ Turn the front wheels back straight """
        if self._DEBUG:
            print(self._DEBUG_INFO, "Turn straight")
        self.wheel.write(self._angle["straight"])

    def turn_right(self, angle):
        """ Turn the front wheels right """
        """ Available angle : 91 ~ 179 degrees """
        if self._DEBUG:
            print(self._DEBUG_INFO, "Turn right")
        if 90 < angle < 180: # max angle
            if angle > self._angle["right"]:
                angle = self._angle["right"]
            self.wheel.write(angle)
        else:
            print('[ERROR-400] You have exceeded the turn angle range to the right : {}'.format(angle))

    def turn(self, angle):
        """ Turn the front wheels to the giving angle """
        if self._DEBUG:
            print(self._DEBUG_INFO, "Turn to", angle)
        if angle < self._angle["left"]:
            angle = self._angle["left"]
        if angle > self._angle["right"]:
            angle = self._angle["right"]
        self.wheel.write(angle)

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, chn):
        self._channel = chn

    @property
    def turning_max(self):
        return self._turning_max

    @turning_max.setter
    def turning_max(self, angle):
        self._turning_max = angle
        self._min_angle = self._straight_angle - angle
        self._max_angle = self._straight_angle + angle
        self._angle = {"left": self._min_angle, "straight": self._straight_angle, "right": self._max_angle}

    @property
    def turning_offset(self):
        return self._turning_offset

    @turning_offset.setter
    def turning_offset(self, value):
        if not isinstance(value, int):
            raise TypeError('"turning_offset" must be "int"')
        self._turning_offset = value
        self.db.set('turning_offset', value)
        self.wheel.offset = value
        self.center_alignment()

    @property
    def debug(self):
        return self._DEBUG

    @debug.setter
    def debug(self, debug):
        """ Set if debug information shows """
        if debug in (True, False):
            self._DEBUG = debug
        else:
            raise ValueError('debug must be "True" (Set debug on) or "False" (Set debug off), not "{0}"'.format(debug))

        if self._DEBUG:
            print(self._DEBUG_INFO, "Set debug on")
            print(self._DEBUG_INFO, "Set wheel debug on")
            self.wheel.debug = True
        else:
            self.wheel.debug = False

    def ready(self):
        """ Get the front wheels to the ready position. """
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Turn to "Ready" position')
        self.wheel.offset = self.turning_offset
        self.center_alignment()

    def calibration(self):
        """ Get the front wheels to the calibration position. """
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Turn to "Calibration" position')
        self.center_alignment()
        self.cali_turning_offset = self.turning_offset

    def cali_left(self):
        """ Calibrate the wheels to left """
        self.cali_turning_offset -= 10
        self.wheel.offset = self.cali_turning_offset
        self.center_alignment()

    def cali_right(self):
        """ Calibrate the wheels to right """
        self.cali_turning_offset += 10
        self.wheel.offset = self.cali_turning_offset
        self.center_alignment()
        
    def cali_accurate_left(self):
        """ Accurate Calibrate the wheels to left """
        self.cali_turning_offset -= 1
        self.wheel.offset = self.cali_turning_offset
        self.center_alignment()

    def cali_accurate_right(self):
        """ Accurate Calibrate the wheels to right """
        self.cali_turning_offset += 1
        self.wheel.offset = self.cali_turning_offset
        self.center_alignment()

    def return_cali_offset(self):
        """ Return the calibration value """
        return self.cali_turning_offset
