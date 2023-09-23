import cv2
import math
import numpy as np
##import neopixel
#import board
#from gpiozero import DistanceSensor

class MAVI1:
    led_count:int = None 
    led_brightness:float = None # 0-1

    threshold:float = None

    field_of_view_angle:int = None

    angle_center_cone_angle:float = None #0-1

    target_img = None

    video_capture = None


    angle_offset:tuple = None

    led_strip = None
    ultrasonic_sensor = None
    gyro_sensor = None

    def __init__(self, led_count:int, led_brightness:float=1, threshold:float=0.6, target_file:str="target.jpg", angle_offset:tuple=(0,0), field_of_view_angle:int=90):
        self.led_count = led_count
        self.led_brightness = led_brightness
        self.threshold = threshold
        self.target_img = cv2.imread(target_file, cv2.IMREAD_GRAYSCALE)
        self.field_of_view_angle = field_of_view_angle
        self.angle_offset = angle_offset
        self.video_capture = cv2.VideoCapture(0)
        #setup_gpio()



    def get_angle_x(self):
        return (0 + self.angle_offset[0]) % 360

    def get_angle_y(self):
        return (0 + self.angle_offset[1]) % 360
    
    def get_angles(self):
        return (self.get_angle_x(), self.get_angle_y())

    def get_distance(self):
        return ultrasonic_sensor.distance
    
    def get_target(self):
        ret, frame = self.video_capture.read()

        scales = np.linspace(0.2, 1.0, 20)[::-1]

        if ret:
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            frame_size = (frame_gray.shape[1], frame_gray.shape[0])

            for scale in scales:
                # Resize the object according to the scale
                resized_obj = cv2.resize(self.target_img, (int(self.target_img.shape[1] * scale), int(self.target_img.shape[0] * scale)))

                # Use matchTemplate to find the object in the frame
                result = cv2.matchTemplate(frame_gray, resized_obj, cv2.TM_CCOEFF_NORMED)

                loc = np.where( result >= self.threshold)

                for position in zip(*loc[::-1]):
                    cv2.circle(frame, position, 5, (0, 255, 255), 2)
                    return [(position[0] / frame_size[0] * 100, 100 - (position[1] / frame_size[1] * 100)), True, frame]
        return [(0, 0), False, frame]

    
    def calculate_target_angles_from_img_position(self, position:tuple):
        angle_x = self.get_angle_x() - self.field_of_view_angle / 2 + self.field_of_view_angle * position[0] / 100
        angle_y = self.get_angle_y() - self.field_of_view_angle / 2 + self.field_of_view_angle * position[1] / 100

        angle_x = angle_x % 360
        angle_y = angle_y % 360

        return (angle_x, angle_y)

    def calculate_target_delta(self, current_angles:tuple, target_angles:tuple):
        delta_x = (target_angles[0] - current_angles[0]) % 360
        delta_y = (target_angles[1] - current_angles[1]) % 360

        return (delta_x, delta_y)

    def calculate_led_address_x1_plane(self, angle_x:float):
        angle_x = angle_x % 360
        address = angle_x / 360 * self.led_count
        return int(address)

    def calculate_led_address_sphere(self, delta_angles:tuple):
        delta_x, delta_y = delta_angles[0] / 360, delta_angles[1] / 360

        rad = math.acos(delta_y / math.sqrt(delta_x*delta_x + delta_y*delta_y))

        alpha = 360 - math.degrees(rad)

        if delta_x < 0:
            alpha = 360 - alpha

        print(alpha)

        address = (alpha / 360) * self.led_count
        print(address)
        return int(address)

    def write_led(self, address:int, color:tuple):
        return
        if address > self.led_count:
            return False
        else:
            self.strip[address] = color
            return True
        
    def write_leds(self, addresses:list, color:tuple):
        return
        for address in addresses:
            if not self.write_led(address, color):
                return False
        return True

    def write_led_strip(self, color):
        return
        self.strip.fill(color)
        return True
    
    


    def setup_gpio(self):
        self.led_strip = neopixel.NeoPixel(board.D18, 30, self.led_brightness)  #LED-Strip: LED Pin 30
        self.ultrasonic_sensor = DistanceSensor(echo=17, trigger=4)                  #Ultrasonic-Sensor: ECHO Pin 17; Trigger Pin 4
        return True
