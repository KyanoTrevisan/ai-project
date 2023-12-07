# Import necessary libraries
import cv2
import numpy as np
import mss
import time
import keyboard
import os
import csv

# Function to capture and save screen
def capture_and_save_screen(game_area, file_path):
    with mss.mss() as sct:
        # Capture the screen at the specified game area
        screencap = sct.grab(game_area)
        screencap = np.array(screencap)

        # Save the captured image
        cv2.imwrite(file_path, screencap)

    return screencap, file_path

# Function to log key presses with image file name
def log_key_press(key, file_path, log_file):
    with open(log_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([file_path, key])

if __name__ == "__main__":
    game_area = {"left": 0, "top": 270, "width": 970, "height": 200}
    img_directory = "screenshots"
    log_file = "key_log.csv"

    # Create directories if they don't exist
    if not os.path.exists(img_directory):
        os.makedirs(img_directory)

    # Initialize csv file for logging
    if not os.path.exists(log_file):
        with open(log_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["image", "key"])

    time.sleep(5)
    img_count = 0

    while True:
        img_count += 1
        file_path = os.path.join(img_directory, f"image_{img_count}.png")

        # Capture the screen and save it
        screen_capture, saved_file_path = capture_and_save_screen(game_area, file_path)

        # Display the captured screen
        cv2.imshow("Game Screen", screen_capture)

        # Check for arrow key presses and log them
        key_pressed = None
        if keyboard.is_pressed('d'):
            key_pressed = 'up&right'
        elif keyboard.is_pressed('a'):
            key_pressed = 'up&left'
        elif keyboard.is_pressed('w'):
            key_pressed = 'up'    
        
        if key_pressed:
            print(key_pressed)
            log_key_press(key_pressed, saved_file_path, log_file)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the OpenCV window
    cv2.destroyAllWindows()