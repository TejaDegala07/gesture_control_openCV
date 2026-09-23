import time
import cv2

class FPSCounter:
    """Calculates and displays Frames Per Second (FPS)."""
    def __init__(self):
        self.pTime = 0
        self.cTime = 0
        self.fps = 0

    def update(self):
        """Updates the FPS calculation."""
        self.cTime = time.time()
        if self.cTime - self.pTime > 0:
            self.fps = 1 / (self.cTime - self.pTime)
        self.pTime = self.cTime
        return int(self.fps)

    def draw(self, img, fps, pos=(10, 50), color=(255, 0, 0), scale=2, thickness=2):
        """Draws the FPS on the given image."""
        cv2.putText(img, f'FPS: {fps}', pos, cv2.FONT_HERSHEY_PLAIN, scale, color, thickness)
        return img
