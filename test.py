import cv2
from matplotlib import pyplot as plt
import numpy as np
import time

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

template = cv2.imread('template.png')
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

# Get dimensions of the template
template_height, template_width = template_gray.shape[::-1]

cap = cv2.VideoCapture('Video_80_05mm_1m_IR.mp4')
frame_rate = int(cap.get(cv2.CAP_PROP_FPS))

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
        threshold = 0.6
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
    #print(np.argmax(correspondence))

    y, x = np.unravel_index(np.argmax(correspondence), correspondence.shape)

    th=190
    if correspondence[y,x] > th:
        cv2.imwrite('Fuga 1.png', frame_gray)
        # Draw a cross
        cross_size = 10
        line_color = (0, 0, 255)  # Red color for the cross
        line_width = 2
        text = "Fuga Detetada"  # Text you want to add
        font = cv2.FONT_HERSHEY_DUPLEX
        font_scale = 0.5
        font_color = (255, 255, 255)  # White color for text
        text_thickness = 1
        text_padding = 5  # Padding between cross and text



        cv2.line(frame_gray, (x - cross_size, y), (x + cross_size, y), line_color, line_width)
        cv2.line(frame_gray, (x, y - cross_size), (x, y + cross_size), line_color, line_width)
        text_size = cv2.getTextSize(text, font, font_scale, text_thickness)[0]
        text_x = x - text_size[0] // 2
        text_y = y + cross_size + text_size[1] + text_padding
        cv2.putText(frame_gray, text, (text_x, text_y), font, font_scale, font_color, text_thickness)

        # cv2.imshow('Fuga detetada', frame_gray)
        cv2.imwrite('Fuga 1_legenda.png', frame_gray)
    
    # Display the correspondence
    cv2.imshow('Frame', frame_gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    i=i+1

    # Pause to control frame rate
    # time.sleep(1/(frame_rate*4))
cap.release()
cv2.destroyAllWindows()