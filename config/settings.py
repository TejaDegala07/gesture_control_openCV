import os

# Camera settings
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
FPS_CAP = 60

# MediaPipe settings
MAX_HANDS = 1
DETECTION_CONFIDENCE = 0.7
TRACKING_CONFIDENCE = 0.7
PRESENCE_CONFIDENCE = 0.7

# Model paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'hand_landmarker.task')

# Mouse Control Settings
CONTROL_ENABLED = False
SMOOTHING_FACTOR = 5.0
MOUSE_SENSITIVITY = 1.0
DEAD_ZONE = 3.0

# Scroll Control Settings
SCROLL_SENSITIVITY = 2000.0
SCROLL_DEAD_ZONE = 0.015
SCROLL_SMOOTHING = 2.0

# Zoom Control Settings
ZOOM_THRESHOLD = 0.015
ZOOM_COOLDOWN = 0.25
