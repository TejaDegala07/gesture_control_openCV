import pyautogui
import math
from config import settings

class MouseController:
    """Handles OS mouse cursor movement with smoothing and clamping."""
    def __init__(self):
        # Disable pyautogui failsafe as ESC will handle emergency stop
        pyautogui.FAILSAFE = False
        
        # Get screen dimensions
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Keep track of previous coordinates for smoothing
        self.prev_x = 0
        self.prev_y = 0

    def move(self, normalized_x, normalized_y):
        """
        Moves the mouse to normalized (x, y) with smoothing and deadzone.
        normalized_x and normalized_y are from MediaPipe (0.0 to 1.0).
        """
        # Map normalized camera coordinates to screen space
        target_x = normalized_x * self.screen_width * settings.MOUSE_SENSITIVITY
        target_y = normalized_y * self.screen_height * settings.MOUSE_SENSITIVITY
        
        # Calculate distance moved
        dist = math.hypot(target_x - self.prev_x, target_y - self.prev_y)
        
        # Apply Dead Zone: Ignore tiny hand movements to stop jitter
        if dist < settings.DEAD_ZONE:
            return
            
        # Apply Smoothing (Exponential Moving Average)
        curr_x = self.prev_x + (target_x - self.prev_x) / settings.SMOOTHING_FACTOR
        curr_y = self.prev_y + (target_y - self.prev_y) / settings.SMOOTHING_FACTOR
        
        # Clamp coordinates to screen boundaries
        curr_x = max(0, min(self.screen_width - 1, curr_x))
        curr_y = max(0, min(self.screen_height - 1, curr_y))
        
        # Execute OS mouse move
        pyautogui.moveTo(int(curr_x), int(curr_y))
        
        # Update previous coordinates
        self.prev_x = curr_x
        self.prev_y = curr_y

    def click(self):
        """Executes a single left mouse click."""
        pyautogui.click()
