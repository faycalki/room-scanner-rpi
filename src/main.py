# Author: Faycal Kilali
# Version: 0.5

import requests
import os
from audio import synthesize_audio
from gpio_handler_no_debounce import GPIOHandler  # Import the GPIOHandler class

def calculate_position(bbox, image_width, image_height):
    """
    Determines the position of the object relative to the image center.

    :param bbox: Bounding box as [x_min, y_min, x_max, y_max].
    :param image_width: Width of the image.
    :param image_height: Height of the image.
    :return: String describing the position (e.g., "to the left", "in the center").
    """
    x_center = (bbox[0] + bbox[2]) / 2
    y_center = (bbox[1] + bbox[3]) / 2

    # Relative horizontal positioning
    horizontal = (
        "to the left of the camera" if x_center < image_width / 3 else
        "to the right of the camera" if x_center > 2 * image_width / 3 else
        "in front of the camera"
    )

    # Relative vertical positioning
    vertical = (
        "towards the top of the view" if y_center < image_height / 3 else
        "towards the bottom of the view" if y_center > 2 * image_height / 3 else
        "at the center of the view"
    )

    return f"{horizontal} and {vertical}"

def process_image(filename, language):
    """Process the image and send it to the server for detections."""
    backend_url = "http://localhost:5000"

    try:
        with open(filename, 'rb') as file:
            image_bytes = file.read()
            files = {'file': ('current.png', image_bytes, 'image/jpeg')}

            # Send request for detections
            response = requests.post(
                f"{backend_url}/get_detections",
                files=files,
                data={'auto_select': 'true', 'min_confidence': '0.25', 'model_size': 'n', 'target_language': language}
            )

            if response.status_code == 200:
                detections_data = response.json()
                detections_hashmap = {}

                # Collect detections with bounding boxes
                for detection in detections_data.get("detections", []):
                    object_name = detection.get("translated_name", "unknown")
                    bbox = detection.get("bounding_box", [0, 0, 0, 0])
                    image_width = detections_data.get("image_width", 1)
                    image_height = detections_data.get("image_height", 1)

                    position = calculate_position(bbox, image_width, image_height)
                    if object_name in detections_hashmap:
                        detections_hashmap[object_name].append(position)
                    else:
                        detections_hashmap[object_name] = [position]

                # Construct professional-sounding output
                output_string = "Summary of inferences: "
                for key, positions in detections_hashmap.items():
                    count = len(positions)
                    instances = "instance" if count == 1 else "instances"
                    position_descriptions = ", ".join(positions)

                    if count == 1:
                        output_string += f"1 {key} located {position_descriptions}. "
                    else:
                        output_string += f"{count} {key}s located {position_descriptions}. "

                print(output_string)
                synthesize_audio(output_string, language)
            else:
                print(f"Error in detections request: {response.text}")

    except FileNotFoundError:
        print(f"Error: The file {filename} does not exist.")
    except requests.RequestException as e:
        print(f"Error: Failed to connect to the server. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main(language="en"):
    gpio = GPIOHandler(button_pin=17)  # Initialize GPIOHandler

    print("Press the button to take a picture (Ctrl+C to exit)...")
    try:
        while True:
            if gpio.is_button_pressed():
                gpio.take_picture()  # Take a picture when the button is pressed
                process_image(os.path.join(gpio.upload_directory, 'current.png'), language)  # Process the image
                time.sleep(1)  # Debounce delay to prevent multiple captures

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        gpio.cleanup()  # Clean up GPIO and camera on exit

if __name__ == "__main__":
    main()
