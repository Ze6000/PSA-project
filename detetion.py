#!/usr/bin/env python3

import matplotlib.pyplot as plt
import cv2
import numpy as np
import time
import mss
import os
import pyautogui


def remove_small_segments(image, min_area):
    # Find connected components and their statistics
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(image, connectivity=8)
    mask = np.zeros_like(labels, dtype=np.uint8)

    # Iterate through components and filter based on area
    for label in range(1, num_labels):  # Skip background component (label 0)
        area = stats[label, cv2.CC_STAT_AREA]
        if area >= min_area:
            mask[labels == label] = 255  # Keep segment if area is greater than or equal to min_area

    return mask

# Set the output video dimensions and frame rate. Using half of screen
screen_width, screen_height = pyautogui.size()
output_width, output_height = int(screen_width // 2), int(screen_height // 2)
fps = 30

# Define the monitor to capture (right now is full screen)
# Starting coordenates
top = 450
left = 890
# Lenght
width=590-top
height=1039-left
#width = screen_width-top
#height = screen_height-left
monitor_to_capture = {"top": top, "left": left, "width": width, "height": height}  
# Example for part of secondary monitor. It depends on the setup used


template = cv2.imread('template2.png')
#cv2.imshow('Template', template)
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
# Get dimensions of the template
template_height, template_width = template_gray.shape[::-1]



i=0
with mss.mss() as sct:
    while True:
        # Capture a screenshot of the specified monitor
        screenshot = sct.grab(monitor_to_capture)

        # Convert the screenshot to a format usable by OpenCV
        frame = np.array(screenshot)

        # Resize the frame to the desired output dimensions
        frame = cv2.resize(frame, (output_width, output_height))

        # Write the frame to the output video
        # out.write(frame)

        # Display the recording in a window (optional)
        cv2.imshow('Live Monitor Recording', frame)

        # Convert the frame to grayscale
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if i==0:
            # Perform template matching
            result = cv2.matchTemplate(frame_gray, template_gray, cv2.TM_CCOEFF_NORMED )

            # Define a threshold to find matches
            threshold = 0.4
            locations = np.where(result >= threshold)

            # Create a mask with the same dimensions as the main image
            mask = np.zeros_like(frame_gray)

            # Mark the detected regions in the mask
            for loc in zip(*locations[::-1]):
                cv2.rectangle(mask, loc, (loc[0] + template_width, loc[1] + template_height), 255, -1)

        correspondence = cv2.bitwise_and(frame_gray, mask)

        #specific_value = 160
        #increment_value = 40
        #correspondence = adjust_image_values(correspondence, specific_value, increment_value)qq
        
        _, mask2 = cv2.threshold(correspondence, 160, 255, cv2.THRESH_BINARY_INV)

        mask2 = cv2.bitwise_and(mask, mask2)
        
        kernel = np.ones((3, 3), np.uint8)  # Can be adjusted as needed
    
        # Apply erosion
        mask2 = cv2.erode(mask2, kernel, iterations=2)

        min_area = 800  # This value must be ajusted according to component requirement

        # Remove small segments
        mask2 = remove_small_segments(mask2, min_area)

        # Apply dilation
        mask2 = cv2.dilate(mask2, kernel, iterations=3)

        correspondence = cv2.bitwise_and(frame_gray, mask2)
        #print(np.argmax(correspondence))

        y, x = np.unravel_index(np.argmax(correspondence), correspondence.shape)

        th=163
        if correspondence[y,x] > th:
            cv2.imwrite('Fuga 1.png', frame_gray)

            line_color = (0, 0, 255)  # Red color 
            text = "Fuga Detetada"  
            font = cv2.FONT_HERSHEY_DUPLEX
            font_scale = 0.5
            font_color = (255, 255, 255)  # White color for text
            text_thickness = 1
            text_padding = 5  
            top_left = (x - 10, y - 10)
            bottom_right = (x + 10, y + 10)

            cv2.rectangle(frame_gray, top_left, bottom_right, line_color)

            text_size = cv2.getTextSize(text, font, font_scale, text_thickness)[0]
            text_x = x - text_size[0] // 2
            text_y = y + 10 + text_size[1] + text_padding
            cv2.putText(frame_gray, text, (text_x, text_y), font, font_scale, font_color, text_thickness)

            # cv2.imshow('Fuga detetada', frame_gray)
            cv2.imwrite('Fuga 1_legenda.png', frame_gray)
        
        # Display the correspondence
        cv2.imshow('Frame', frame_gray)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # Pause to control frame rate
        time.sleep(1 / fps)

        i=i+1
        
        # Delete the recording file after each iteration to save storage space
        if os.path.exists('monitor_recording.avi'):
            os.remove('monitor_recording.avi')

cv2.destroyAllWindows()