from L298N import L298N
from PCA9685 import PCA9685
import filedb


class Rear_Wheels(object):
    """ Back wheels control class """

    """ Initialize motor pin """
    Motor_IN1 = 11
    Motor_IN2 = 12
    Motor_IN3 = 13
    Motor_IN4 = 15

    PWM_A = 4 # servo driver IC CH4
    PWM_B = 5 # servo driver IC CH5

    _DEBUG = False
    _DEBUG_INFO = 'DEBUG "rear_wheels.py":'

    def __init__(self, bus_number=1, db="config"):
        """ Init the direction channel and pwm channel """

        self.db = filedb.fileDB(db=db)

        self.forward_A = int(self.db.get("forward_A", default_value=1))
        self.forward_B = int(self.db.get("forward_B", default_value=0))

        self.left_wheel = L298N.Motor(self.Motor_IN1, self.Motor_IN2, offset=self.forward_A, is_left=True)
        self.right_wheel = L298N.Motor(self.Motor_IN3, self.Motor_IN4, offset=self.forward_B, is_left=False)

        # PWM Setup
        self.pwm = PCA9685.PWM(bus_number=bus_number)

        def _set_a_pwm(value):
            pulse_wide = self.pwm.map(value, 0, 100, 0, 4095)
            self.pwm.write(self.PWM_A, 0, int(pulse_wide))

        def _set_b_pwm(value):
            pulse_wide = self.pwm.map(value, 0, 100, 0, 4095)
            self.pwm.write(self.PWM_B, 0, int(pulse_wide))

        self.left_wheel.pwm  = _set_a_pwm
        self.right_wheel.pwm = _set_b_pwm

        self._speed = 0

        self.debug = int(self.db.get("debug", default_value=0))
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Set left wheel to IN1 #%d, IN2 #%d PWM channel to %d' % (self.Motor_IN1, self.Motor_IN2, self.PWM_A))
            print(self._DEBUG_INFO, 'Set right wheel to IN3 #%d, IN4 #%d PWM channel to %d' % (self.Motor_IN3, self.Motor_IN3, self.PWM_B))

    def stop(self):
        """ Stop both wheels """
        self.left_wheel.stop()
        self.right_wheel.stop()
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Stop')

    def power_down(self):
        """ Down has motor power """
        self.left_wheel.power_down()
        self.right_wheel.power_down()
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Down has motor power')

    def go_forward(self, speed_value):
        """ Move both wheels forward with speed """
        # Setup motor speed
        self._speed = speed_value
        self.speed = self._speed

        self.left_wheel.forward()
        self.right_wheel.forward()
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Running forward with speed')

    def go_backward(self, speed_value):
        """ Move both wheels backward with speed """
        # Setup motor speed
        self._speed = speed_value
        self.speed = self._speed

        self.left_wheel.backward()
        self.right_wheel.backward()
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Running backward with speed')

    @property
    def speed(self, speed):
        return self._speed

    @speed.setter
    def speed(self, speed):
        self._speed = speed
        """ Set moving speeds """
        self.left_wheel.speed = self._speed
        self.right_wheel.speed = self._speed
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Set speed to', self._speed)

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
            self.left_wheel.debug = True
            self.right_wheel.debug = True
            self.pwm.debug = True
        else:
            self.left_wheel.debug = False
            self.right_wheel.debug = False
            self.pwm.debug = False

    def ready(self):
        """ Get the back wheels to the ready position. (stop) """
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Turn to "Ready" position')
        self.left_wheel.offset = self.forward_A
        self.right_wheel.offset = self.forward_B
        self.stop()

    def calibration(self):
        """ Get the front wheels to the calibration position. """
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Turn to "Calibration" position')
        self.go_forward(50)
        self.cali_forward_A = self.forward_A
        self.cali_forward_B = self.forward_B

    def cali_left(self):
        """ Reverse the left wheels forward direction in calibration """
        self.cali_forward_A = not self.cali_forward_A
        self.left_wheel.offset = self.cali_forward_A
        self.go_forward(50)

    def cali_right(self):
        """ Reverse the right wheels forward direction in calibration """
        self.cali_forward_B = not self.cali_forward_B
        self.right_wheel.offset = self.cali_forward_B
        self.go_forward(50)

    @property
    def _get_cali_forward_A(self):
        """ Return forward_A variables """
        return self.cali_forward_A

    @property
    def _get_cali_forward_B(self):
        """ Return forward_B variables """
        return self.cali_forward_B