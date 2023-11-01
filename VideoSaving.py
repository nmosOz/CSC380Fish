import cv2 as cv
import time
from datetime import datetime
import paramiko

def Rec(Ln):
    while Ln!=0:
        cap = cv.VideoCapture(0)
        if not cap.isOpened:
            print('--(!)Error opening video capture')
            exit(0)
        name = datetime.now().strftime("%m_%d_%y@%H_%M") + ".avi" #11_01_23@06_08 for example
        
        #Creates a video writer to a folder, which creates a new
        #video based off of webcam footage one frame at a time
        result = cv.VideoWriter("C:/Users/aydan/OneDrive/Desktop/Videos/" + name,
                                cv.VideoWriter_fourcc(*'MJPG'),
                                15, (int(cap.get(3)),int(cap.get(4))))
        start_time = time.time()
        while (True):
            ret, frame = cap.read()
            frame = cv.resize(frame, None, fx=.5, fy=.5, interpolation=cv.INTER_AREA)
            ret, frame = cap.read()
            if ret == True:
                result.write(frame)
                if ((time.time() - start_time)>=Tm):
                    Time = time.time() - start_time
                    break
        cv.waitKey(0)
        cv.destroyAllWindows()
        
        #Places the fully-created video into the Unanalyzed folder on my Oswego.edu account
        scp.put("C:/Users/aydan/OneDrive/Desktop/Videos/" + name,"Desktop/Site/Unanalyzed/" + name)
        print ('File ' + name + ' saved with length of ' + str(Time) + ' seconds')
        Ln-=1

#Gets the length of the videos in minutes, and converts it to seconds
Tm = float(input('How long?\n'))*60
print (Tm)

#Gets the number of videos recorded, anything below 0 is infinite
Ln = int(input('How many?\n'))

#Opens an ssh and scp client to my Oswego server
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('pi.cs.oswego.edu', username='''Oswego.edu username''', password='''Oswego.edu password''')
scp = ssh.open_sftp()

Rec(Ln)
scp.close()
ssh.close()

#This is for starting the program at a new hour (not currently used)
'''
#currentTime = datetime.now().strftime("%H")
#while (True): 
#    if (datetime.now().strftime("%H")>currentTime):
#        Rec(Ln)
'''
