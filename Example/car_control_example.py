from SR02 import SR02_Supersonic as Supersonic_Sensor

import front_wheels
import rear_wheels
import time

if __name__ == '__main__':
    try:
        # Example Of Front Servo Motor Control
        steering = front_wheels.Front_Wheels(db='config')
        steering.center_alignment()
        time.sleep(1)
        
        # Example Of Real Motor Control
        accelerator = rear_wheels.Rear_Wheels(db='config')
        accelerator.ready()
        accelerator.go_forward(50)
        time.sleep(1)
        accelerator.stop()
        time.sleep(1)
        accelerator.go_backward(50)
        time.sleep(1)

        accelerator.stop()
        accelerator.power_down()
        
        # Example of Ultrasonic Sensor
        distance_detector = Supersonic_Sensor.Supersonic_Sensor(35)

        for i in range(10):
            distance = distance_detector.get_distance()
            print("Distance is ", distance)
            time.sleep(1)
        
    except KeyboardInterrupt:
        accelerator.stop()
        accelerator.power_down()