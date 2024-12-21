import RPi.GPIO as GPIO
import cv2
#import libcamera
#from picamera2 import PiCamera2
#import picamera
import os


class GPIOHandler:
    def __init__(self, button_pin=17):
        # Set up GPIO mode
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Pin definition
        self.BUTTON_PIN = button_pin

        # Setup pin as input
        GPIO.setup(self.BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Initialize the camera with dynamic index detection
        #self.camera = cv2.VideoCapture(1)  # Specify the correct path
        #self.camera = cv2
        #self.camera.release()
        #self.camera = None
        for index in range(50):  # TODO: Improve detection
          #  if (index == 14):
           #     continue
            temp_camera = cv2.VideoCapture(index)
            if temp_camera.isOpened():
                self.camera = temp_camera
                print(f"Camera initialized at index {index}")
                break
            temp_camera.release()


        if self.camera is None:
            raise RuntimeError("No available cameras found!")

        # Set the directory for uploads
        self.upload_directory = './uploads'
        if not os.path.exists(self.upload_directory):
            os.makedirs(self.upload_directory)

    def is_button_pressed(self):
        """Return True if button is pressed (LOW due to pull-up)"""
        return GPIO.input(self.BUTTON_PIN)

    def take_picture(self):
        #self.camera = cv2.VideoCapture(0)
        """Capture an image and save it to the specified path"""
        ret, frame = self.camera.read()
        if ret:
                image_path = os.path.join(self.upload_directory, 'current.png')
                cv2.imwrite(image_path, frame)
                print(f"Image captured and saved to {image_path}")
        else:
	        print("failed to capture image")
        # Release camera
        #self.camera.release()

    def cleanup(self):
        """Clean up GPIO and camera on shutdown"""
        self.camera.release()
        GPIO.cleanup()

# Example usage
if __name__ == "__main__":
    try:
        gpio = GPIOHandler(button_pin=17)  # Replace 17 with your pin number

        print("Press the button (Ctrl+C to exit)...")
        while True:
            if gpio.is_button_pressed():
                gpio_handler.take_picture()  # Take a picture when the button is pressed

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        gpio.cleanup()
