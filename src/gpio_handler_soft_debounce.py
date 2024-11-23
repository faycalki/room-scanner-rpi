# Author: Faycal Kilali
# Purpose: Soft debounce of interface
import RPi.GPIO as GPIO
import time
from threading import Thread, Event


class GPIOHandler:
    def __init__(self, button_pin=17, led_status_pin=27, led_busy_pin=22):
        # Set up GPIO mode
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Pin definitions
        self.BUTTON_PIN = button_pin
        self.LED_STATUS_PIN = led_status_pin  # Green LED for system status
        self.LED_BUSY_PIN = led_busy_pin  # Red LED for busy status

        # Setup pins
        GPIO.setup(self.BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.LED_STATUS_PIN, GPIO.OUT)
        GPIO.setup(self.LED_BUSY_PIN, GPIO.OUT)

        # Initialize LEDs
        GPIO.output(self.LED_STATUS_PIN, GPIO.LOW)
        GPIO.output(self.LED_BUSY_PIN, GPIO.LOW)

        # Button press handling
        self.button_pressed = Event()
        self.stop_thread = Event()
        self.button_thread = Thread(target=self._button_monitor)
        self.button_thread.daemon = True

    def start(self):
        """Start the GPIO handler and indicate system is ready"""
        self.button_thread.start()
        GPIO.output(self.LED_STATUS_PIN, GPIO.HIGH)  # System ready
        print("GPIO Handler started. System ready.")

    def stop(self):
        """Clean up GPIO on shutdown"""
        self.stop_thread.set()
        self.button_thread.join()
        GPIO.cleanup()
        print("GPIO Handler stopped.")

    def _button_monitor(self):
        """Monitor button presses in a separate thread"""
        # Debounce time in seconds
        DEBOUNCE_TIME = 0.3
        last_press_time = 0

        while not self.stop_thread.is_set():
            # Button is pressed when input is LOW (pull-up resistor)
            if not GPIO.input(self.BUTTON_PIN):
                current_time = time.time()
                # Check if enough time has passed since last press
                if (current_time - last_press_time) > DEBOUNCE_TIME:
                    print("Button pressed!")
                    self.button_pressed.set()
                    last_press_time = current_time
            time.sleep(0.1)  # Reduce CPU usage

    def wait_for_press(self):
        """Wait for button press and return True when pressed"""
        self.button_pressed.wait()
        self.button_pressed.clear()
        return True

    def set_busy(self, is_busy):
        """Set the busy LED status"""
        GPIO.output(self.LED_BUSY_PIN, GPIO.HIGH if is_busy else GPIO.LOW)

    def blink_status(self, duration=0.2, times=3):
        """Blink the status LED"""
        for _ in range(times):
            GPIO.output(self.LED_STATUS_PIN, GPIO.LOW)
            time.sleep(duration)
            GPIO.output(self.LED_STATUS_PIN, GPIO.HIGH)
            time.sleep(duration)


# Example usage
if __name__ == "__main__":
    try:
        # Initialize GPIO handler
        gpio_handler = GPIOHandler()
        gpio_handler.start()

        print("Press the button to test (Ctrl+C to exit)...")

        while True:
            # Wait for button press
            if gpio_handler.wait_for_press():
                print("Processing...")
                gpio_handler.set_busy(True)  # Turn on busy LED

                # Simulate processing
                time.sleep(2)

                gpio_handler.set_busy(False)  # Turn off busy LED
                gpio_handler.blink_status()  # Blink status LED to indicate completion
                print("Done!")

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        gpio_handler.stop()