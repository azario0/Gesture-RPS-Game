
---

# Gesture Controlled Rock, Paper, Scissors Game

This repository contains a Python-based Rock, Paper, Scissors game that uses your webcam and hand gestures to play. The game leverages OpenCV for video capture and Google's MediaPipe library for real-time hand tracking and gesture recognition.



## Features

- **Real-time Hand Gesture Recognition:** Play the game by showing your hand to the camera.
- **Gesture Detection:** Detects Rock, Paper, and Scissors gestures.
- **Interactive Gameplay:** Play against a computer opponent with randomized choices.
- **Score Tracking:** Keeps track of the player and computer scores.
- **User-Friendly Interface:** On-screen instructions and game status updates.

## Technologies Used

- **Python:** The core programming language for the game logic.
- **OpenCV:** Used for capturing video from the webcam and displaying the game interface.
- **MediaPipe:** A cross-platform framework by Google for building multimodal applied machine learning pipelines. It is used here for hand tracking and landmark detection.
- **NumPy:** A fundamental package for scientific computing with Python.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You will need to have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/azario0/Gesture-RPS-Game.git
    cd Gesture-RPS-Game
    ```

2.  **Install the required packages:**
    ```sh
    pip install opencv-python mediapipe numpy
    ```

### How to Play

1.  **Run the application:**
    ```sh
    python app.py
    ```

2.  A window will open showing your webcam feed.

3.  Press the **SPACE** bar to start a new round.

4.  After the countdown, make one of the following gestures with your hand in front of the camera:
    *   **Rock:** A closed fist.
    *   **Paper:** An open hand with all fingers extended.
    *   **Scissors:** Two extended fingers (index and middle).

5.  The game will detect your gesture, the computer will make its choice, and the winner of the round will be displayed.

6.  Press the **'q'** key to quit the game at any time.

## How It Works

The application captures video from your webcam. For each frame, it uses the MediaPipe Hands solution to detect and track the landmarks of your hand.

A custom function, `detect_gesture`, analyzes the positions of these landmarks to determine if you are making a Rock, Paper, or Scissors gesture. This is primarily done by counting the number of extended fingers.

The game logic then compares your detected gesture against a randomly chosen gesture for the computer to determine the winner of the round. All game information, including scores and instructions, is overlaid on the video feed using OpenCV's drawing functions.