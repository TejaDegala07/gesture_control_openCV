import cv2

# Define the connections between landmarks (MediaPipe hand skeleton)
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),        # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),        # Index
    (5, 9), (9, 10), (10, 11), (11, 12),   # Middle
    (9, 13), (13, 14), (14, 15), (15, 16), # Ring
    (13, 17), (0, 17), (17, 18), (18, 19), (19, 20) # Pinky
]

def draw_landmarks(img, hand_landmarks_list):
    """
    Draws the 21 hand landmarks and their connections manually using OpenCV.
    This avoids dependencies on old MediaPipe protobuf formats.
    """
    h, w, _ = img.shape
    
    for hand_landmarks in hand_landmarks_list:
        # Convert normalized coordinates to pixel coordinates
        landmarks_px = []
        for landmark in hand_landmarks:
            cx, cy = int(landmark.x * w), int(landmark.y * h)
            landmarks_px.append((cx, cy))
            
        # Draw connections (lines)
        for connection in HAND_CONNECTIONS:
            start_idx, end_idx = connection
            start_pt = landmarks_px[start_idx]
            end_pt = landmarks_px[end_idx]
            cv2.line(img, start_pt, end_pt, (0, 255, 0), 2)
            
        # Draw landmarks (circles)
        for cx, cy in landmarks_px:
            cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)
            
    return img
