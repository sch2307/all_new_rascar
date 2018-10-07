import RPi.GPIO as GPIO


class Motor(object):
    """ Motor driver class
        Set direction_channel to the GPIO channel which connect to MA,
        Set motor_B to the GPIO channel which connect to MB,
        Both GPIO channel use BCM numbering;
        Set pwm_channel to the PWM channel which connect to PWMA,
        Set pwm_B to the PWM channel which connect to PWMB;
        PWM channel using PCA9685, Set pwm_address to your address, if is not 0x40
        Set debug to True to print out debug informations.
    """
    _DEBUG = False
    _DEBUG_INFO = 'DEBUG "L298N.py":'

    def __init__(self, forward_direction_channel, backward_direction_channel, pwm=None, offset=True, is_left=False):
        """Init a motor on giving dir. channel and PWM channel."""
        if self._DEBUG:
            print(self._DEBUG_INFO, "Debug on")
        self.forward_direction_channel = forward_direction_channel
        self.backward_direction_channel = backward_direction_channel
        self._pwm = pwm

        self._offset = offset
        
        self.forward_offset = self._offset
        self.backward_offset = not self.forward_offset
       
        self._speed = 0
        self._is_left = is_left

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD) # Number GPIOs by its physical location

        if self._DEBUG:
            print(self._DEBUG_INFO, 'setup motor forward direction channel at', forward_direction_channel)
            print(self._DEBUG_INFO, 'setup motor backward direction channel at', backward_direction_channel)
            print(self._DEBUG_INFO, 'setup motor pwm channel as', self._pwm)

        GPIO.setup(self.forward_direction_channel, GPIO.OUT)
        GPIO.setup(self.backward_direction_channel, GPIO.OUT)

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        """ Set Speed with given value """
        if speed not in range(0, 101):
            raise ValueError('speed ranges from 0 to 100, not "{0}"'.format(speed))
        if not callable(self._pwm):
            raise ValueError('pwm is not callable, please set Motor.pwm to a pwm control function '
                             'with only 1 variable speed')

        if self._DEBUG:
            print(self._DEBUG_INFO, 'Set speed to: ', speed)
        self._speed = speed
        self._pwm(self._speed)

    def forward(self):
        """ Set the motor direction to forward """
        if self.forward_offset == self._is_left:
            GPIO.output(self.forward_direction_channel, GPIO.HIGH)
            GPIO.output(self.backward_direction_channel, GPIO.LOW)
        else:
            GPIO.output(self.forward_direction_channel, GPIO.LOW)
            GPIO.output(self.backward_direction_channel, GPIO.HIGH)

        self.speed = self._speed
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Motor moving forward (%s)' % str(self.forward_offset))

    def backward(self):
        """ Set the motor direction to backward """
        if self.backward_offset != self._is_left:
            GPIO.output(self.forward_direction_channel, GPIO.LOW)
            GPIO.output(self.backward_direction_channel, GPIO.HIGH)
        else:
            GPIO.output(self.forward_direction_channel, GPIO.HIGH)
            GPIO.output(self.backward_direction_channel, GPIO.LOW)
        
        self.speed = self._speed
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Motor moving backward (%s)' % str(self.backward_offset))

    def stop(self):
        """ Stop the motor by giving a 0 speed """
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Motor stop')
        self.speed = 0

    def power_down(self):
        """ Down the motor power """
        GPIO.output(self.forward_direction_channel, GPIO.LOW)
        GPIO.output(self.backward_direction_channel, GPIO.LOW)
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Motor power has down')

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        """ Set offset for much user-friendly """
        if value not in (True, False):
            raise ValueError('offset value must be Bool value, not"{0}"'.format(value))
        self.forward_offset = value
        self.backward_offset = not self.forward_offset
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Set offset to %d' % self._offset)

    @property
    def debug(self, debug):
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

    @property
    def pwm(self):
        return self._pwm

    @pwm.setter
    def pwm(self, pwm):
        if self._DEBUG:
            print(self._DEBUG_INFO, 'pwm set')
        self._pwm = pwm