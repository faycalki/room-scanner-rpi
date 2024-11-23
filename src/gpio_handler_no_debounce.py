import RPi.GPIO as GPIO


class GPIOHandler:
    def __init__(self, button_pin=17):
        # Set up GPIO mode
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Pin definition
        self.BUTTON_PIN = button_pin

        # Setup pin as input
        GPIO.setup(self.BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def is_button_pressed(self):
        """Return True if button is pressed (LOW due to pull-up)"""
        return not GPIO.input(self.BUTTON_PIN)

    def cleanup(self):
        """Clean up GPIO on shutdown"""
        GPIO.cleanup()


# Example usage
if __name__ == "__main__":
    try:
        gpio = GPIOHandler(button_pin=17)  # Replace 17 with your pin k

        print("Press the button (Ctrl+C to exit)...")
        while True:
            if gpio.is_button_pressed():
                print("Button pressed!")

    except KeyboardInterrupt:
        print("\nExiting...")
        gpio.cleanup()