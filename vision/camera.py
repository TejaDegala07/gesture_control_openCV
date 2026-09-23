import cv2
import sys
import os

# Ensure config is importable by adding parent dir to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings

class Camera:
    """Handles webcam initialization and frame capture."""
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, settings.CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, settings.CAMERA_HEIGHT)

    def get_frame(self):
        """Reads a frame from the webcam, mirrors it, and returns success status."""
        success, img = self.cap.read()
        if not success:
            return False, None
        
        # Mirror the camera feed for natural interaction
        img = cv2.flip(img, 1)
        return True, img

    def release(self):
        """Releases the camera resource."""
        self.cap.release()
