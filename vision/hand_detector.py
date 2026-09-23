import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings
from vision.landmarks import draw_landmarks

class HandDetector:
    """Detects hands using the new MediaPipe Hand Landmarker API."""
    def __init__(self):
        # Ensure the model file exists, it was downloaded to the project root
        if not os.path.exists(settings.MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {settings.MODEL_PATH}. "
                                    f"Please download it from MediaPipe documentation.")

        base_options = python.BaseOptions(model_asset_path=settings.MODEL_PATH)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=settings.MAX_HANDS,
            min_hand_detection_confidence=settings.DETECTION_CONFIDENCE,
            min_hand_presence_confidence=settings.PRESENCE_CONFIDENCE,
            min_tracking_confidence=settings.TRACKING_CONFIDENCE
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

    def find_hands(self, img, draw=True):
        """
        Detects hands in the image and optionally draws landmarks.
        Returns the image and a boolean indicating if a hand was detected.
        """
        # Convert the BGR image to RGB and create an mp.Image
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
        
        # We need a timestamp for VIDEO mode, which must be strictly increasing.
        # time.time() * 1000 provides current time in milliseconds.
        timestamp_ms = int(time.time() * 1000)
        
        # Detect hands
        self.results = self.detector.detect_for_video(mp_image, timestamp_ms)
        
        hand_detected = False
        
        # If hands are found in the frame
        if self.results.hand_landmarks:
            hand_detected = True
            if draw:
                img = draw_landmarks(img, self.results.hand_landmarks)
                    
        return img, hand_detected
