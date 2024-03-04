# CSC380Fish
This is the finished repository for Team Fish from the Fall 2023 CSC380 class.

# Fish Movement Detection Program
This program was designed using OpenCV to be able to detect movement in Round Gobies and be able to correctly identify that any movement in the tank is a goby.

## Program Description
This program would automatically record videos using a simple webcam attached to an Intel NUC. The NUC would, every 30 minutes, send a video to a remote server for the Watchdog to be able to see and call the detect.py class to analyze the video.
After analyzing the video for fish activity the program would then write the contents out to a file in XML format for the user to read. The XML report would contain the video timestamp, amount of fish in the frame, and the time of day.

## Authors 
 - [@Fritz Frigin](https://github.com/ffrigin)
 - [@Nathan Moses](https://github.com/nmosOz)
 - [@Aydan Price](https://github.com/TheGreatAydan)
 - [@Kieran Rudolph](https://github.com/krudy712)
 - [@Jonathan Waller](https://github.com/JWaller4)
