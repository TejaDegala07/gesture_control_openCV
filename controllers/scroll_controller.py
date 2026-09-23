import pyautogui
from config import settings

class ScrollController:
    """Handles OS mouse scrolling."""
    def __init__(self):
        self.prev_y = None
        self.smoothed_delta = 0.0

    def reset(self):
        """Resets the tracking state."""
        self.prev_y = None
        self.smoothed_delta = 0.0

    def scroll(self, current_y):
        """
        Calculates vertical movement and scrolls using pyautogui.
        Returns the action string ("SCROLL UP", "SCROLL DOWN", "SCROLL IDLE").
        """
        if self.prev_y is None:
            self.prev_y = current_y
            return "SCROLL IDLE"

        # Calculate delta
        # Normalized coordinates: y increases downwards.
        # Moving hand UP means current_y < prev_y (delta is positive)
        # Moving hand DOWN means current_y > prev_y (delta is negative)
        raw_delta = self.prev_y - current_y

        if abs(raw_delta) < settings.SCROLL_DEAD_ZONE:
            # We don't update prev_y here so that very slow movements
            # can eventually accumulate and trigger a scroll, or we can update 
            # it to strictly ignore slow movements. 
            # The requirements say "Very small movements should produce no scrolling"
            # so we just return IDLE.
            self.prev_y = current_y
            return "SCROLL IDLE"

        # Smoothing
        self.smoothed_delta = self.smoothed_delta + (raw_delta - self.smoothed_delta) / settings.SCROLL_SMOOTHING
        
        # PyAutoGUI scroll amount (positive = up, negative = down)
        scroll_amount = int(self.smoothed_delta * settings.SCROLL_SENSITIVITY)
        
        action = "SCROLL IDLE"
        if abs(scroll_amount) > 0:
            pyautogui.scroll(scroll_amount)
            if scroll_amount > 0:
                action = "SCROLL UP"
            else:
                action = "SCROLL DOWN"
            
            # Reset delta to prevent continuous scrolling without movement
            self.smoothed_delta = 0.0
            
        self.prev_y = current_y
        return action
