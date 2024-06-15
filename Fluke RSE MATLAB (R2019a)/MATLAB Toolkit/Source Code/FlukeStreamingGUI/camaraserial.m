ToolkitFunctions.LoadAssemblies();
CameraSerial = ToolkitFunctions.DiscoverDevices;
CameraSerial=CameraSerial{1};
%CameraSerial = TiX580-23110010;
if ToolkitFunctions.SelectDevice(CameraSerial) == 1
    disp('Camera Successfully Opened');
end
cameraStream=ToolkitFunctions.StartStream();
while 1
    [TempArray, IRImage] = ToolkitFunctions.GetData('Celsius');
end


