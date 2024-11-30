# Raspberry Pi Room Scanner Using Computer Vision

![Project Banner](./assets/project-banner.svg)

![Real-Time Detection](https://img.shields.io/badge/Real%20Time-Detection-blue)
![Raspberry Pi Compatible](https://img.shields.io/badge/Raspberry%20Pi-Compatible-red)
![Voice Assisted](https://img.shields.io/badge/Voice-Assisted-green)

## Description

This project transforms a Raspberry Pi into an intelligent room scanning device that verbally describes detected objects in its environment. Built upon the [Object Detection Educator](https://github.com/faycalki/object-detection-educator) framework, this implementation focuses on creating a portable, button-activated device that provides real-time audio feedback about its surroundings, making it particularly useful for educational purposes or as an assistive technology.

## Features

- **Real-Time Detection**: Instant object detection using YOLOv10 optimized for Raspberry Pi
- **Voice Feedback**: Automatic verbal description of detected objects
- **Hardware Integration**: 
  - Push-button activation for on-demand scanning
  - LED status indicators
  - Integrated audio output
- **Portable Design**: Self-contained system powered by Raspberry Pi
- **Multi-language Support**: Inherits support for 243 languages from the parent project

## Hardware Requirements

### Core Components
- Raspberry Pi 3+ (2GB+ RAM recommended)
- Raspberry Pi Camera Module V2 or better
- Push button (momentary switch)
- 2 LEDs (status indicators)
- Speaker/headphones (3.5mm or USB)
- Jumper wires
- Breadboard
- Power supply (5V/3A recommended)

### Circuit Diagram

![Circuit Diagram](./assets/circuit_diagram_full.jpeg)


## Credits

### Hardware Design
- Faycal Kilali
- Ryan Budd
- Yuezun Shan

### Software Development
- Faycal Kilali (Lead Developer)
- Ryan Budd (Contributor)

### Other citations
Open-source ultralytics package: [YOLOv10 GitHub Repository](https://github.com/THU-MIG/yolov10)
 
Wang, Ao, Chen, Hui, Liu, Lihao, Chen, Kai, Lin, Zijia, Han, Jungong, & Ding, Guiguang. (2024). *YOLOv10: Real-Time End-to-End Object Detection*. arXiv preprint arXiv:2405.14458.

## Installation

Python 3.9 is required.

1. Clone the repository:
    ```bash
    git clone https://github.com/faycalki/room-scanner-rpi.git
    cd pi-room-scanner
    ```

2. Set up Python virtual environment:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Enable Raspberry Pi camera and GPIO:
    ```bash
    sudo raspi-config
    # Enable Camera under Interface Options
    ```

4. Configure audio output:
    ```bash
    # This will be based on what kind of hardware you use for the audio. Refer to the documentation of your hardware.
    ```

## Usage

### Basic Operation

1. Power on the Raspberry Pi
2. Wait for the red LED to indicate system ready (power is on for the system)
3. Press the button to trigger a room scan (blue LED will trigger)
4. Listen to the voice description of detected objects


