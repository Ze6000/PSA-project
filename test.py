#!/usr/bin/env python3


import cv2
from matplotlib import pyplot as plt
import numpy as np
import time
import os

def remove_small_segments(image, min_area):
    # Find connected components and their statistics
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(image, connectivity=8)

    # Initialize mask to keep track of segments to keep
    mask = np.zeros_like(labels, dtype=np.uint8)

    # Iterate through components and filter based on area
    for label in range(1, num_labels):  # Skip background component (label 0)
        area = stats[label, cv2.CC_STAT_AREA]
        if area >= min_area:
            mask[labels == label] = 255  # Keep segment if area is greater than or equal to min_area

    return mask

folder = "Files for processing"

# Create full paths for the image and video files
template_path = os.path.join(folder, "template.png")
video_path = os.path.join(folder, "varias_fugas.mp4")


template = cv2.imread(template_path)
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

# Get dimensions of the template
template_height, template_width = template_gray.shape[::-1]

# cap = cv2.VideoCapture("Video_80_05mm_1m_IR.mp4")
cap = cv2.VideoCapture(video_path)
frame_rate = int(cap.get(cv2.CAP_PROP_FPS))

n_leaks=0
coord_leaks= []
i=0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    # Convert the frame to grayscale
    
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if i==0:
        # Perform template matching
        result = cv2.matchTemplate(frame_gray, template_gray, cv2.TM_CCOEFF_NORMED )

        # Define a threshold to find matches
        threshold = 0.66
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
    
    kernel = np.ones((3, 3), np.uint8)  # You can adjust the size of the kernel as needed
 
    # Apply erosion
    mask2 = cv2.erode(mask2, kernel, iterations=2)

    min_area = 800  # Adjust this value according to your requirement

    # Remove small segments
    mask2 = remove_small_segments(mask2, min_area)

    # Apply dilation
    mask2 = cv2.dilate(mask2, kernel, iterations=3)

    
    correspondence = cv2.bitwise_and(frame_gray, mask2)
    # y, x = np.unravel_index(np.argmax(correspondence), correspondence.shape)

    
    # Define the parameters for mean shift segmentation
    spatial_radius = 5
    color_radius = 10
    min_density = 100

    # Perform mean shift segmentation
    frame_rgb = cv2.cvtColor(correspondence, cv2.COLOR_GRAY2RGB)
    segmented_image = cv2.pyrMeanShiftFiltering(frame_rgb, spatial_radius, color_radius, min_density)

    # Convert the segmented image to grayscale
    segmented_gray = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2GRAY)
    y, x = np.unravel_index(np.argmax(segmented_gray), segmented_gray.shape)


    th=180
    if segmented_gray[y,x] > th and [y,x] not in coord_leaks:
        n_leaks = n_leaks + 1
        
        # Saving the leak without caption
        filename = f"Fuga_{n_leaks}.png"
        save_folder = "Leaks"
        full_path = os.path.join(save_folder, filename)
        cv2.imwrite(full_path, frame_gray)

        line_color = (0, 0, 255)  # Red color 
        text = "Fuga Detetada"  # Text you want to add
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

        
        filename = f"Fuga_{n_leaks}_legenda.png"
        full_path = os.path.join(save_folder, filename)
        cv2.imwrite(full_path, frame_gray)
        
        # Erase a square area around a specific point
        # Iterate through the area and set pixels to black
        if n_leaks > 0:
            for dx in range(-10, 10 + 1):
                for dy in range(-10, 10 + 1):
                    # Determine the new coordinates
                    X = x + dx
                    Y = y + dy
                    
                    # Check if the new coordinates are within the bounds of the image
                    if 0 <= X < mask2.shape[1] and 0 <= Y < mask2.shape[0]:
                        # Add those coordinates to the list of leaks
                        coord_leaks.append([Y,X])
    
    
    # Display the correspondence
    cv2.imshow("Frame", frame_gray)
    # cv2.imshow('Mask', mask)
    cv2.imshow("Mask2", mask2)
    

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    i=i+1

    # Pause to control frame rate
    # time.sleep(1/(frame_rate*4))

cap.release()
cv2.destroyAllWindows()