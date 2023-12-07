# Import necessary libraries
import cv2
import numpy as np
import pydirectinput as pdi
import mss
import time

# This function will take in the screenshot, process it, find the lines and determine the input
def open_cv(game_area): 
    # Intialize a variable to use to determine input
    steering_angle = 0

    with mss.mss() as sct:
        screencap = sct.grab(game_area)
    
    # Convert screencap to a numpy array and process it to detect line visibility
    screencap_np = np.array(screencap)
    screencap_gray = cv2.cvtColor(screencap_np, cv2.COLOR_RGB2GRAY)
    screencap_blur = cv2.GaussianBlur(screencap_gray, (5, 5), 0)
    screencap_canny = cv2.Canny(screencap_blur, threshold1=100, threshold2=300)

    # Use the houghlinesp algorithm to detect lines from our processed image

    lines = cv2.HoughLinesP(screencap_canny, 1, np.pi/180, threshold=100, minLineLength=150, maxLineGap=15)
    line_image = np.zeros_like(screencap_canny)

    # Initialize lists to store the left and right lines
    left_line_x = []
    right_line_x = []

    # Grab the wanted region of the screencap 
    y1 = line_image.shape[0]
    y2 = int(y1 * 0.6)

    # Check for detected lines
    if lines is not None:
        # Iterate through every line and calculate the slop for the lines
        for line in lines:
            for x1, y1, x2, y2 in line:
                slope = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else float('inf')
                # Assign line to the left if slope is negative
                if slope < 0:
                    left_line_x.extend([x1, x2])
                # Assign line to the right if slope is positive
                else:
                    right_line_x.extend([x1, x2])
                cv2.line(line_image, (x1, int(y1)), (x2, int(y2)), (255, 0, 0), 5)
    # Grab the average of the left lines and the right lines
    left_x_avg = np.mean(left_line_x) if left_line_x else 0
    right_x_avg = np.mean(right_line_x) if right_line_x else line_image.shape[1]

    # Find the center of the 2 lines
    mid_x = (left_x_avg + right_x_avg) / 2

    # Define the placement of the car
    car_pos = line_image.shape[1] / 2  

    # Define deviation to find steering angle
    deviation = car_pos - mid_x

    # Define steering angle to determine inputs
    steering_angle = deviation / line_image.shape[1] * 100  


    # Check steering angle to determine the input
    # High steering angle = more time pressed down
    if 7 > steering_angle > 2:
        pdi.keyDown('left')
        pdi.keyDown('w')
        pdi.keyUp('left')
        pdi.keyUp('w')
    elif -7 < steering_angle < -2:
        pdi.keyDown('right')
        pdi.keyDown('w')
        pdi.keyUp('right')
        pdi.keyUp('w')
    elif -2 <= steering_angle <= 2:
        pdi.keyDown('w')
        time.sleep(0.1)
        pdi.keyUp('w')
        key_input = 2
    elif steering_angle < -7:
        pdi.keyDown('w')
        pdi.keyDown('right')
        time.sleep(0.1)
        pdi.keyUp('w')
        pdi.keyUp('right')
    elif 7 <= steering_angle:
        pdi.keyDown('w')
        pdi.keyDown('left')
        time.sleep(0.1)
        pdi.keyUp('w')
        pdi.keyUp('left')
    else:
        pdi.keyDown('w')
        time.sleep(.1)
        pdi.keyUp('w')  
        
if __name__ == "__main__":
    # The game is placed in the top left corner of the screen
    game_area = {"left": 0, "top": 270, "width": 970, "height": 200}
    time.sleep(2)
    while True:
        time.sleep(.1)
        screen_capture = open_cv(game_area)
