import matlab.engine
import numpy as np
import scipy.io
from PIL import Image
import matplotlib.pyplot as plt
import cv2
import pickle

# Start MATLAB engine
eng = matlab.engine.start_matlab()

eng.ToolkitFunctions.LoadAssemblies(nargout=0)
print("Assemblies Loaded.")
CameraSerial=eng.ToolkitFunctions.DiscoverDevices()
CameraSerial=CameraSerial[0]

if eng.ToolkitFunctions.SelectDevice(CameraSerial) == True:
    print(CameraSerial+': Camera Successfully Opened.')

cameraStream=eng.ToolkitFunctions.StartStream()
plt.ion()  # Turn on interactive mode

fig, ax = plt.subplots()
im = None  # Placeholder for the image object

try:
    while True:
        # Get the IR image from the camera
        IRImage = eng.ToolkitFunctions.GetData('Celsius')

        # Convert the MATLAB data to a NumPy array
        IRImage_np = np.array(IRImage._data).reshape(IRImage.size, order='F')
        IRImage_np = cv2.cvtColor(IRImage_np, cv2.COLOR_RGB2BGR)
       
        cv2.imshow("Thermal Image",IRImage_np)
        cv2.waitKey(0)

        

finally:
    # Stop the camera stream and quit the MATLAB engine
    eng.ToolkitFunctions.StopStream()
    eng.quit()

plt.ioff()  # Turn off interactive mode
plt.close()  # Close the figure window