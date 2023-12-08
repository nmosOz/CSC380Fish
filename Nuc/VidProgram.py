import cv2 as cv
import time
import os
from time import sleep
from datetime import datetime
import subprocess

# Gets the length of the videos in minutes
Tm = 30

# Gets the number of videos recorded, anything below 0 is infinite
Ln = -1

# Determines if the TimeCheck() function should be applied
TC = True

# The origin path of the video files
OPath = os.getcwd() + "/"

# The server's login, password, and path
SerLog = "aprice3@pi.cs.oswego.edu"
SerPass = "7Lifezgray"
SerPath = "Desktop/Website/static/fish_videos"
SerPath = SerLog + ":" + SerPath

# This function is because the room is black from 7pm - 7am (Doesn't record during that time because the camera has no night-vision feature)
def TimeCheck():
   if int(datetime.now().strftime("%H")) >= 19:
      T = 25200+(24-int(datetime.now().strftime("%H")))*3600 - (int(datetime.now().strftime("%M")))*60 - int(datetime.now().strftime("%S"))
      sleep(T)
   elif int(datetime.now().strftime("%H")) < 7:
      T = (7-int(datetime.now().strftime("%H")))*3600 - (int(datetime.now().strftime("%M")))*60 - int(datetime.now().strftime("%S"))
      sleep(T)
   return

# Compresses the videos and sends them to the website (Parallel to the main method)
def VidMagic(Time):
   # Splits the video's name depending on its length
   TimeR = ""
   if (Tm>=(3599.9)):
      TimeR = Time.split(":")[0]
   elif ((Tm<(3599.9)) and (Tm>=(59.9))):
      TimeR = Time.split(":")[0] + ":" + Time.split(":")[1]
   else:
      TimeR = Time
   Time = OPath + Time + "t.mp4"
   print(Time)
   TimeR = OPath + TimeR + ".mp4"
   print(TimeR)
   
   # Compresses the video
   subprocess.run(["ffmpeg", "-i", Time, "-vcodec", "libx264", TimeR])
   
   # Sends the video to the Oswego servers
   subprocess.run(["sshpass", "-p", SerPass, "scp", TimeR, SerPath])
   
   #Deletes both the temporary and new video from the NUC
   subprocess.run(["rm", Time])
   subprocess.run(["rm", TimeR])

# Main function
def Rec(Ln):
   if TC:
      TimeCheck()
   cap = cv.VideoCapture(0)
   Time = datetime.now().strftime("%m_%d_%y@%H:%M:%S")
   
   # Creates a video writer, * THE PATH SPECIFIED IS TEMPORARY
   result = cv.VideoWriter(OPath + Time + "t.mp4", cv.VideoWriter_fourcc(*'mp4v'), 30, (int(cap.get(3)),int(cap.get(4))))
  
   # Gets the time before any frames are written to the video
   start_time = time.time()
   
   # Writes the video to a temporary file, to be sent to the servers later
   while (True):
      ret, frame = cap.read()
      if ret == True:
          result.write(frame)
          cv.imshow("Video",frame)
          if cv.waitKey(1) == ord('q'):
             break
          if ((time.time() - start_time)>=Tm):
             break
      
   # Releases the temporary video and gets ready for a new loop
   cv.destroyAllWindows()
   cap.release()
    
   # Forks the video, compressing, sending, and deleting the video while creating a new loop (Works with different lengths of videos)
   Fork = os.fork()
   if Fork == 0:
      TimeT = Time
      VidMagic(TimeT)
      os._exit(0)

Tm = Tm * 60 - .1

# Runs the program
while (Ln!=0):
   Rec(Ln)
   Ln -= 1
