import cv2
import mediapipe as mp
import random
import time
import numpy as np

class RockPaperScissorsGame:
    def __init__(self):
        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Game variables
        self.player_score = 0
        self.computer_score = 0
        self.current_gesture = "None"
        self.computer_choice = ""
        self.game_result = ""
        self.countdown = 0
        self.game_state = "waiting"  # waiting, countdown, playing, result
        self.last_game_time = 0
        
        # Gesture choices
        self.choices = ["Rock", "Paper", "Scissors"]
        
    def count_extended_fingers(self, landmarks):
        """Count extended fingers based on landmark positions"""
        # Finger tip and pip landmark indices
        finger_tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
        finger_pips = [3, 6, 10, 14, 18]
        
        extended_fingers = 0
        
        # Check thumb (different logic - compare x coordinates)
        if landmarks[4].x > landmarks[3].x:  # Right hand
            extended_fingers += 1
        elif landmarks[4].x < landmarks[3].x:  # Left hand
            extended_fingers += 1
            
        # Check other fingers (compare y coordinates)
        for i in range(1, 5):
            if landmarks[finger_tips[i]].y < landmarks[finger_pips[i]].y:
                extended_fingers += 1
                
        return extended_fingers
    
    def detect_gesture(self, landmarks):
        """Detect Rock, Paper, or Scissors gesture"""
        # Finger tip and pip landmark indices
        finger_tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
        finger_pips = [3, 6, 10, 14, 18]
        
        extended_fingers = []
        
        # Check thumb (compare x coordinates)
        if landmarks[4].x > landmarks[3].x:  # Thumb extended
            extended_fingers.append(0)
            
        # Check other fingers (compare y coordinates)
        for i in range(1, 5):
            if landmarks[finger_tips[i]].y < landmarks[finger_pips[i]].y:
                extended_fingers.append(i)
        
        num_extended = len(extended_fingers)
        
        # Rock: No fingers or only thumb extended
        if num_extended == 0 or (num_extended == 1 and 0 in extended_fingers):
            return "Rock"
        
        # Paper: All 5 fingers extended
        elif num_extended >= 4:  # More flexible detection
            return "Paper"
        
        # Scissors: Only index (1) and middle (2) fingers extended
        elif num_extended == 2 and 1 in extended_fingers and 2 in extended_fingers:
            return "Scissors"
        
        return "None"
    
    def determine_winner(self, player, computer):
        """Determine the winner of the game"""
        if player == computer:
            return "Tie"
        elif (player == "Rock" and computer == "Scissors") or \
             (player == "Paper" and computer == "Rock") or \
             (player == "Scissors" and computer == "Paper"):
            return "Player"
        else:
            return "Computer"
    
    def draw_text(self, img, text, position, color=(255, 255, 255), font_scale=1, thickness=2):
        """Draw text on image with background"""
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_x, text_y = position
        
        # Draw background rectangle
        cv2.rectangle(img, (text_x - 10, text_y - text_size[1] - 10), 
                     (text_x + text_size[0] + 10, text_y + 10), (0, 0, 0), -1)
        
        # Draw text
        cv2.putText(img, text, position, font, font_scale, color, thickness)
    
    def run_game(self):
        """Main game loop"""
        cap = cv2.VideoCapture(0)
        
        print("Rock Paper Scissors Game with MediaPipe!")
        print("Show your hand gesture to the camera:")
        print("- Rock: Make a fist")
        print("- Paper: Show open palm")
        print("- Scissors: Show peace sign")
        print("Press SPACE to start a new game, 'q' to quit")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            h, w, c = frame.shape
            
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process the frame
            results = self.hands.process(rgb_frame)
            
            # Draw hand landmarks
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
                    # Detect gesture
                    self.current_gesture = self.detect_gesture(hand_landmarks.landmark)
            else:
                self.current_gesture = "None"
            
            # Game logic
            current_time = time.time()
            
            if self.game_state == "waiting":
                self.draw_text(frame, "Press SPACE to play!", (50, 50), (0, 255, 0), 1, 2)
                
            elif self.game_state == "countdown":
                time_left = 3 - (current_time - self.countdown_start)
                if time_left > 0:
                    self.draw_text(frame, f"Get Ready: {int(time_left) + 1}", (50, 50), (0, 255, 255), 2, 3)
                else:
                    # Game starts
                    self.computer_choice = random.choice(self.choices)
                    self.game_state = "playing"
                    self.game_start_time = current_time
                    
            elif self.game_state == "playing":
                time_left = 2 - (current_time - self.game_start_time)
                if time_left > 0:
                    self.draw_text(frame, f"Show your gesture: {time_left:.1f}s", (50, 50), (255, 0, 0), 1, 2)
                else:
                    # Determine result
                    if self.current_gesture != "None":
                        winner = self.determine_winner(self.current_gesture, self.computer_choice)
                        if winner == "Player":
                            self.player_score += 1
                            self.game_result = "You Win!"
                        elif winner == "Computer":
                            self.computer_score += 1
                            self.game_result = "Computer Wins!"
                        else:
                            self.game_result = "It's a Tie!"
                    else:
                        self.game_result = "No gesture detected!"
                    
                    self.game_state = "result"
                    self.result_start_time = current_time
                    
            elif self.game_state == "result":
                if current_time - self.result_start_time < 3:
                    # Show results
                    self.draw_text(frame, f"You: {self.current_gesture}", (50, 100), (255, 255, 255), 1, 2)
                    self.draw_text(frame, f"Computer: {self.computer_choice}", (50, 140), (255, 255, 255), 1, 2)
                    self.draw_text(frame, self.game_result, (50, 180), (0, 255, 0) if "Win" in self.game_result else (0, 0, 255), 1, 2)
                else:
                    self.game_state = "waiting"
            
            # Always show current gesture and scores
            self.draw_text(frame, f"Current Gesture: {self.current_gesture}", (50, h - 120), (255, 255, 0))
            self.draw_text(frame, f"Player: {self.player_score} | Computer: {self.computer_score}", (50, h - 80))
            self.draw_text(frame, "Press SPACE for new game, 'q' to quit", (50, h - 40), (200, 200, 200), 0.7)
            
            # Display the frame
            cv2.imshow('Rock Paper Scissors', frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord(' ') and self.game_state == "waiting":
                self.game_state = "countdown"
                self.countdown_start = current_time
        
        # Clean up
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        game = RockPaperScissorsGame()
        game.run_game()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have installed the required packages:")
        print("pip install opencv-python mediapipe numpy")