import cv2
import sys
import os

# Add the project root to sys.path to allow absolute imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from vision.camera import Camera
from vision.hand_detector import HandDetector
from gestures.gesture_detector import GestureDetector
from controllers.mouse_controller import MouseController
from controllers.scroll_controller import ScrollController
from controllers.zoom_controller import ZoomController
from config import settings
from utils.fps import FPSCounter
import keyboard
import math

def main():
    # Initialize components
    camera = Camera()
    detector = HandDetector()
    gesture_detector = GestureDetector()
    mouse_controller = MouseController()
    scroll_controller = ScrollController()
    zoom_controller = ZoomController()
    fps_counter = FPSCounter()
    
    # Use a list to allow modification inside the callback
    control_state = [settings.CONTROL_ENABLED]
    
    def toggle_control():
        control_state[0] = not control_state[0]
        
    # Register reliable global hotkey for Windows
    keyboard.add_hotkey('ctrl+shift+g', toggle_control)

    prev_gesture = "UNKNOWN"

    print("Starting GestureOS Day 3...")
    print("Press Ctrl+Shift+G to toggle cursor control.")
    print("Press ESC to exit.")

    while True:
        # 1. Get image from camera
        success, img = camera.get_frame()
        if not success:
            print("Failed to capture frame from camera.")
            break

        # 2. Detect hands and draw landmarks
        img, hand_detected = detector.find_hands(img, draw=True)

        # 3. Process Gestures and Display Status
        cursor_active = "INACTIVE"
        current_gesture = "UNKNOWN"
        
        # Debug variables for ZOOM
        debug_dist = 0.0
        debug_prev_dist = 0.0
        debug_delta = 0.0
        debug_action = "IDLE"
        
        if hand_detected and detector.results.hand_landmarks:
            # Get the first hand's landmarks
            first_hand_landmarks = detector.results.hand_landmarks[0]
            
            # Get finger states
            finger_states = gesture_detector.get_finger_states(first_hand_landmarks)
            
            # Get gesture classification
            current_gesture = gesture_detector.detect_gesture(first_hand_landmarks, finger_states)
            
            # Mouse Control Logic
            action_status = ""
            
            if control_state[0]:
                if current_gesture == "INDEX":
                    index_tip = first_hand_landmarks[8]
                    # Pass normalized x and y
                    mouse_controller.move(index_tip.x, index_tip.y)
                    cursor_active = "ACTIVE"
                    scroll_controller.reset()
                elif current_gesture == "INDEX_MIDDLE":
                    # For scroll tracking, use average y of index and middle tips
                    index_tip = first_hand_landmarks[8]
                    middle_tip = first_hand_landmarks[12]
                    avg_y = (index_tip.y + middle_tip.y) / 2.0
                    
                    if prev_gesture != "INDEX_MIDDLE":
                        scroll_controller.reset()
                        
                    scroll_action = scroll_controller.scroll(avg_y)
                    action_status = scroll_action if scroll_action != "SCROLL IDLE" else "IDLE"
                    
                elif current_gesture == "INDEX_THUMB":
                    # For zoom tracking, use distance between thumb and index tips
                    thumb_tip = first_hand_landmarks[4]
                    index_tip = first_hand_landmarks[8]
                    dist = math.hypot(thumb_tip.x - index_tip.x, thumb_tip.y - index_tip.y)
                    
                    if prev_gesture != "INDEX_THUMB":
                        zoom_controller.reset()
                        
                    zoom_action, debug_delta = zoom_controller.zoom(dist)
                    
                    debug_dist = dist
                    debug_action = zoom_action if zoom_action != "IDLE" else "IDLE"
                    
                    if zoom_action != "IDLE":
                        action_status = zoom_action
                        debug_action = zoom_action
                    else:
                        action_status = "IDLE"
                        debug_action = "IDLE"
                        
                elif current_gesture == "FIST" and prev_gesture != "FIST":
                    # Single left click on transition to FIST
                    mouse_controller.click()
                    cursor_active = "CLICK"
                    scroll_controller.reset()
                    zoom_controller.reset()
                else:
                    if prev_gesture == "INDEX_MIDDLE":
                        scroll_controller.reset()
                    if prev_gesture == "INDEX_THUMB":
                        zoom_controller.reset()
                    
            prev_gesture = current_gesture
            
        # Draw UI Overlay
        # MODE: NORMAL
        # CONTROL: ON/OFF
        y_overlay = 90
        cv2.putText(img, "MODE: NORMAL", (10, y_overlay), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        y_overlay += 30
        
        control_str = "ON" if control_state[0] else "OFF"
        control_color = (0, 255, 0) if control_state[0] else (0, 0, 255)
        cv2.putText(img, f"CONTROL: {control_str}", (10, y_overlay), cv2.FONT_HERSHEY_SIMPLEX, 0.7, control_color, 2)
        y_overlay += 30
        
        if current_gesture == "INDEX_MIDDLE":
            cv2.putText(img, f"GESTURE: {current_gesture}", (10, y_overlay), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            y_overlay += 30
            cv2.putText(img, f"ACTION: {action_status}", (10, y_overlay), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
        elif current_gesture == "INDEX_THUMB":
            cv2.putText(img, f"Gesture: {current_gesture}", (10, y_overlay), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            y_overlay += 30
            cv2.putText(img, f"Distance: {debug_dist:.3f}", (10, y_overlay), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
            y_overlay += 30
            cv2.putText(img, f"Delta: {debug_delta:+.3f}", (10, y_overlay), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
            y_overlay += 30
            cv2.putText(img, f"Action: {debug_action}", (10, y_overlay), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
        else:
            cv2.putText(img, f"GESTURE: {current_gesture}", (10, y_overlay), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            y_overlay += 30
            cursor_color = (0, 255, 0) if cursor_active == "ACTIVE" else (0, 0, 255)
            cv2.putText(img, f"CURSOR: {cursor_active}", (10, y_overlay), cv2.FONT_HERSHEY_SIMPLEX, 0.7, cursor_color, 2)

        # 4. Calculate and display FPS
        fps = fps_counter.update()
        img = fps_counter.draw(img, fps)

        # 5. Show the image
        cv2.imshow("GestureOS", img)

        # 6. Wait for key press (ESC to exit cleanly)
        key = cv2.waitKeyEx(1)
        if key == 27: # ESC key
            break

    # Clean up resources
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
