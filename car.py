#########################################################################
# Date: 2018/10/02
# file name: car.py
# Purpose: this code has been generated for the 4 wheels drive body
# this code is used for the student only
#########################################################################


# =======================================================================
# import GPIO library and time module
# =======================================================================
import RPi.GPIO as GPIO

# =======================================================================
# import ALL method in the SEN040134 Tracking Module
# =======================================================================
from SEN040134 import SEN040134_Tracking as Tracking_Sensor

# =======================================================================
# import ALL method in the TCS34725 RGB Module
# =======================================================================
from TCS34725 import TCS34725_RGB as RGB_Sensor

# =======================================================================
# import ALL method in the SR02 Ultrasonic Module
# =======================================================================
from SR02 import SR02_Supersonic as Supersonic_Sensor

# =======================================================================
# import ALL method in the PCA9685 Module
# =======================================================================
from PCA9685 import PCA9685 as PWM_Controller

# =======================================================================
# import ALL method in the rear/front Motor Module
# =======================================================================
import rear_wheels
import front_wheels

# =======================================================================
#  set GPIO warnings as false
# =======================================================================
GPIO.setwarnings(False)


class Car(object):

    """ Initialize Speed Value """
    SLOWEST = 20
    SLOWER = 25
    SLOW = 35
    NORMAL = 40
    FAST = 65
    FASTER = 80
    FASTEST = 100

    def __init__(self, carName):
        try:
            # ================================================================
            # ULTRASONIC MODULE DRIVER INITIALIZE
            # ================================================================
            self.distance_detector = Supersonic_Sensor.Supersonic_Sensor(35)

            # ================================================================
            # TRACKING MODULE DRIVER INITIALIZE
            # ================================================================
            self.line_detector = Tracking_Sensor.SEN040134_Tracking([16, 18, 22, 40, 32])

            # ================================================================
            # RGB MODULE DRIVER INITIALIZE
            # ================================================================
            self.color_getter = RGB_Sensor.TCS34725()
            if self.color_getter.get_exception_occur():
                print("[ERRNO-101] There is a problem with RGB_Sensor(TCS34725)")

            # ================================================================
            # DISABLE RGB MODULE INTERRUPTION
            # ================================================================
            self.color_getter.set_interrupt(False)

            # ================================================================
            # PCA9685(PWM 16-ch Extension Board) MODULE WAKEUP
            # ================================================================
            self.carEngine = PWM_Controller.PWM()
            self.carEngine.startup()

            # ================================================================
            # FRONT WHEEL DRIVER SETUP
            # ================================================================
            self.steering = front_wheels.Front_Wheels(db='config')
            self.steering.ready()

            # ================================================================
            # REAR WHEEL DRIVER SETUP
            # ==================================================6==============
            self.accelerator = rear_wheels.Rear_Wheels(db='config')
            self.accelerator.ready()

            # ================================================================
            # SET LIMIT OF TURNING DEGREE
            # ===============================================================
            self.steering.turning_max = 35

            # ================================================================
            # SET FRONT WHEEL CENTOR ALLIGNMENT
            # ================================================================
            self.steering.center_alignment()

            # ================================================================
            # SET APPOINTED OF CAR NAME
            # ================================================================
            self.car_name = carName

        except Exception as e:
            print("CONTACT TO Kookmin Univ. Teaching Assistant")
            print("Learn more : " + e)

    def drive_parking(self):
        # front wheels center alignment
        self.steering.center_alignment()

        # power down both wheels
        self.accelerator.stop()
        self.accelerator.power_down()

        # GPIO clean up
        GPIO.cleanup()