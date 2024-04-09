#!/usr/bin/env python3

import cv2
import numpy as np
import time
import mss
import os
import pyautogui



def record_screen():
    # Set the output video dimensions and frame rate. Using half of screen
    screen_width, screen_height = pyautogui.size()
    output_width, output_height = screen_width // 2, screen_height // 2
    fps = 30


    # Define the monitor to capture 
    # Starting coordenates
    top = 500
    left = 500
    # Lenght
    width = screen_width-top
    height = screen_height-left
    monitor_to_capture = {"top": top, "left": left, "width": width, "height": height}  
    # Example for part of primary monitor. It depends on the setup used

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('monitor_recording.avi', fourcc, fps, (output_width, output_height))


    with mss.mss() as sct:
        
        # Capture a screenshot of the specified monitor
        screenshot = sct.grab(monitor_to_capture)

        # Convert the screenshot to a format usable by OpenCV
        frame = np.array(screenshot)

        # Resize the frame to the desired output dimensions
        frame = cv2.resize(frame, (output_width, output_height))

        # Write the frame to the output video
        out.write(frame)

        # Display the recording in a window (optional)
        cv2.imshow('Live Monitor Recording', frame)

        # Pause for a short duration to control frame rate
        time.sleep(1 / fps)
