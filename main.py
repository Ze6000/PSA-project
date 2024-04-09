#!/usr/bin/env python3
import os
import cv2
from screen_recording import record_screen

# Process the recorded video frames using OpenCV
def process_frames(video_file):
    cap = cv2.VideoCapture(video_file)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Add your OpenCV processing here
        # Example: Convert frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('Processed Frame', gray_frame)
        

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    while True:
        record_screen()  # Start screen recording
        process_frames('monitor_recording.avi')  # Process recorded frames with OpenCV
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # Delete the recording file if it exists
        if os.path.exists('monitor_recording.avi'):
            os.remove('monitor_recording.avi')
            # print("Recording file deleted.")
                

