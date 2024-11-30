import RPi.GPIO as GPIO
from picamera import PiCamera
import time
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

        # Initialize the camera
        self.camera = PiCamera()

        # Set the directory for uploads
        self.upload_directory = './uploads'
        if not os.path.exists(self.upload_directory):
            os.makedirs(self.upload_directory)

    def is_button_pressed(self):
        """Return True if button is pressed (LOW due to pull-up)"""
        return not GPIO.input(self.BUTTON_PIN)

    def take_picture(self):
        """Capture an image and save it to the specified path"""
        image_path = os.path.join(self.upload_directory, 'current.png')
        self.camera.capture(image_path)
        print(f"Image captured and saved to {image_path}")

    def cleanup(self):
        """Clean up GPIO and camera on shutdown"""
        self.camera.close()
        GPIO.cleanup()


# Example usage
if __name__ == "__main__":
    try:
        gpio = GPIOHandler(button_pin=17)  # Replace 17 with your pin number

        print("Press the button (Ctrl+C to exit)...")
        while True:
            if gpio.is_button_pressed():
                gpio.take_picture()  # Take a picture when the button is pressed
                time.sleep(1)  # Debounce delay to prevent multiple captures, just incase.

    except KeyboardInterrupt:
        print("\nExiting...")
        gpio.cleanup()
