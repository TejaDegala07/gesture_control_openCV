import math

class GestureDetector:
    """Handles finger state detection and gesture classification."""
    def __init__(self):
        # Tip landmarks for fingers: Thumb, Index, Middle, Ring, Pinky
        self.tip_ids = [4, 8, 12, 16, 20]

    def _calculate_distance(self, p1, p2):
        """Calculates Euclidean distance between two normalized landmarks."""
        return math.hypot(p1.x - p2.x, p1.y - p2.y)

    def get_finger_states(self, hand_landmarks):
        """
        Returns a dictionary indicating if each finger is 'UP' or 'DOWN'.
        Uses relative landmark positions.
        """
        states = {
            "Thumb": "DOWN",
            "Index": "DOWN",
            "Middle": "DOWN",
            "Ring": "DOWN",
            "Pinky": "DOWN"
        }
        
        # Index, Middle, Ring, Pinky: Compare tip y to PIP joint y (tip_id - 2)
        # If tip is higher (smaller y), it's UP
        if hand_landmarks[self.tip_ids[1]].y < hand_landmarks[self.tip_ids[1] - 2].y:
            states["Index"] = "UP"
            
        if hand_landmarks[self.tip_ids[2]].y < hand_landmarks[self.tip_ids[2] - 2].y:
            states["Middle"] = "UP"
            
        if hand_landmarks[self.tip_ids[3]].y < hand_landmarks[self.tip_ids[3] - 2].y:
            states["Ring"] = "UP"
            
        if hand_landmarks[self.tip_ids[4]].y < hand_landmarks[self.tip_ids[4] - 2].y:
            states["Pinky"] = "UP"
            
        # Thumb: Instead of simple y comparison, check if thumb tip is further 
        # from the pinky MCP (17) in the x-axis than the thumb IP (3).
        # This works reasonably well regardless of hand orientation.
        thumb_tip = hand_landmarks[4]
        thumb_ip = hand_landmarks[3]
        pinky_mcp = hand_landmarks[17]
        
        # Distance from thumb joints to the opposite side of the hand
        dist_tip = self._calculate_distance(thumb_tip, pinky_mcp)
        dist_ip = self._calculate_distance(thumb_ip, pinky_mcp)
        
        if dist_tip > dist_ip:
             states["Thumb"] = "UP"
             
        return states

    def detect_gesture(self, hand_landmarks, finger_states):
        """
        Classifies the gesture based on finger states and distances.
        Supported: INDEX, INDEX_MIDDLE, FIST, OPEN_PALM, PINCH, THUMB_ONLY, PINKY_ONLY, UNKNOWN
        """
        fingers_up_count = sum(1 for state in finger_states.values() if state == "UP")
        
        thumb_up = finger_states["Thumb"] == "UP"
        index_up = finger_states["Index"] == "UP"
        middle_up = finger_states["Middle"] == "UP"
        ring_up = finger_states["Ring"] == "UP"
        pinky_up = finger_states["Pinky"] == "UP"
        
        # Basic gesture logic based on active fingers
        if fingers_up_count == 5:
            return "OPEN_PALM"
            
        if fingers_up_count == 0:
            return "FIST"
            
        if fingers_up_count == 1 and index_up:
            return "INDEX"
            
        if fingers_up_count == 1 and thumb_up:
            return "THUMB_ONLY"
            
        if fingers_up_count == 1 and pinky_up:
            return "PINKY_ONLY"
            
        if fingers_up_count == 2 and index_up and middle_up:
            return "INDEX_MIDDLE"
            
        if fingers_up_count == 2 and index_up and thumb_up:
            return "INDEX_THUMB"
            
        return "UNKNOWN"
