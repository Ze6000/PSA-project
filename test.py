import cv2
import numpy as np
import time
import mss
import os
import pyautogui


# Set the output video dimensions and frame rate. Using half of screen
screen_width, screen_height = pyautogui.size()
output_width, output_height = int(screen_width // 2), int(screen_height // 2)
fps = 30
print(screen_height, screen_width)
# Define the monitor to capture (right now is full screen)
# Starting coordenates
top = 0
left = 0
# Lenght
width = screen_width-top
height = screen_height-left
monitor_to_capture = {"top": top, "left": left, "width": width, "height": height}  
# Example for part of primary monitor. It depends on the setup used

# Define the codec and create VideoWriter object
# Its only necessary if want to save video, now its deleting each frame after using it 
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('monitor_recording.avi', fourcc, fps, (output_width, output_height))


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
        
        #Processing image (only a greyscale to exemplify)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Processed Frame', gray_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Pause to control frame rate
        time.sleep(1 / fps)

        # Delete the recording file after each iteration to save storage space
        if os.path.exists('monitor_recording.avi'):
            os.remove('monitor_recording.avi')
            # print("Recording file deleted.")


# Release the VideoWriter and close all OpenCV windows
# out.release()
cv2.destroyAllWindows()