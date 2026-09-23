# GestureOS

GestureOS is a Python-based computer vision application that allows you to control your system's mouse and perform various UI actions using real-time hand gestures. Powered by OpenCV and MediaPipe, GestureOS translates your hand movements into system commands seamlessly.

## Features

- **Mouse Movement**: Point your index finger to move the mouse cursor around the screen.
- **Clicking**: Form a fist to perform a left mouse click.
- **Scrolling**: Pinch and move your index and middle fingers to scroll vertically.
- **Zooming**: Change the distance between your thumb and index fingers to zoom in and out.
- **Global Control Toggle**: Easily toggle gesture controls on or off anytime using `Ctrl+Shift+G`.

## Requirements

Ensure you have the required dependencies installed (see `requirements.txt`). This project relies on:
- OpenCV (`opencv-python`)
- MediaPipe (`mediapipe`)
- PyAutoGUI (`pyautogui`)
- Keyboard (`keyboard`)
- NumPy (`numpy`)

## Getting Started

1. Clone the repository.
2. Install the necessary dependencies: `pip install -r requirements.txt`.
3. Run the main script: `python main.py`
4. Use `Ctrl+Shift+G` to toggle cursor control on and start gesturing! Press `ESC` to exit the application.
