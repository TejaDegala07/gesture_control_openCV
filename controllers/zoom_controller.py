import pyautogui
import time
from config import settings

class ZoomController:
    """Handles OS zoom using Ctrl + '+' and Ctrl + '-'."""
    def __init__(self):
        self.prev_dist = None
        self.last_zoom_time = 0.0

    def reset(self):
        """Resets the tracking state."""
        self.prev_dist = None
        self.last_zoom_time = 0.0

    def zoom(self, current_dist):
        """
        Calculates distance change and zooms using pyautogui.
        Returns the action string ("ZOOM IN", "ZOOM OUT", "IDLE") and delta.
        """
        if self.prev_dist is None:
            self.prev_dist = current_dist
            return "IDLE", 0.0

        delta = current_dist - self.prev_dist
        action = "IDLE"
        
        current_time = time.monotonic()
        
        if current_time - self.last_zoom_time >= settings.ZOOM_COOLDOWN:
            if delta > settings.ZOOM_THRESHOLD:
                pyautogui.hotkey('ctrl', '+')
                action = "ZOOM IN"
                self.last_zoom_time = current_time
            elif delta < -settings.ZOOM_THRESHOLD:
                pyautogui.hotkey('ctrl', '-')
                action = "ZOOM OUT"
                self.last_zoom_time = current_time
                
        # Update previous distance for next frame
        self.prev_dist = current_dist
        
        return action, delta
