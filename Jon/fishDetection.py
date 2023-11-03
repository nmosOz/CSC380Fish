from __future__ import print_function
import cv2 as cv
import argparse
#import vlc
# JON ADDED
import csv


face = False
# JON ADDED, this is where the CSV files get written to
csv_directory = 'C:\\Users\\wuwal\\Desktop\\CSVTest\\'


# JON ADDED, writes the CSV record. Takes directory (of where the CSV files go), the name of the video
# being analyzed, the timestamp in the video OpenCV is at (via cap.get(cv.CAP_PROP_POS_MSEC)),
# and the array of bounding boxes (fish) as arguments.
def makecsv(directory, vidname, times, fish):
    # Converts the 'time in milliseconds' taken from OpenCV's analyses
    seconds = (times / 1000) % 60
    seconds = str(seconds)
    minutes = (times / (1000 * 60)) % 60
    minutes = str(minutes)
    # Parse the video name to get the date and hour
    parsed_info = vidname.splt("@")
    # Writes the CSV file; if it doesn't find a CSV file to write to it'll make a new one automatically!
    with open(directory+vidname, 'a', newline='') as file:
        writer = csv.writer(file)
        # Writes the row, "Species", "Date", "Time Spotted", "Timestamp", "Number of fish seen"
        writer.writerow(["Goby", parsed_info[0], parsed_info[1]+":"+minutes+":"+seconds, minutes+":"+seconds,
                         len(fish)+1])


def detectAndDisplay(frame, video_name):
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY +1)
    frame_gray = cv.equalizeHist(frame_gray)
    #-- Detect fish
    #fish = fish_cascade.detectMultiScale(frame_gray)
    #fish = fish_cascade.detectMultiScale(frame_gray, scaleFactor=1.0485258, minNeighbors=6, minSize=(100,100), rejectOutputLevels = True)
    #detection_result =fish_cascade.detectMultiScale3(frame_gray, scaleFactor=1.0485258, minNeighbors=6, minSize=(30,30), outputRejectLevels = 1)
    #[faces, neighbours, weights] = fish_cascade.detectMultiScale3(frame_gray, scaleFactor=1.3, minNeighbors=5 ,flags=cv.CASCADE_SCALE_IMAGE , minSize=(10,10), outputRejectLevels = True)
    #detection_result, rejectLevels, levelWeights =fish_cascade.detectMultiScale3(img, scaleFactor=1.0485258, minNeighbors=6,outputRejectLevels = 1)
    fish, rejectLevels, levelWeights =fish_cascade.detectMultiScale3(frame_gray, scaleFactor=1.25, minNeighbors=6,outputRejectLevels = 1)

    #print(rejectLevels)
    #print(levelWeights)

   # print(levelWeights[6])
   # print(detection_result)
    #fish_cascade.detectMultiScale

    count = 0
    count2 = 0
    lgth = len(levelWeights)
    lgth1 = len(fish)

   # print(lgth)
    print(lgth1)
    if lgth1 != 0:
        time = cap.get(cv.CAP_PROP_POS_MSEC)
        makecsv(csv_directory, video_name, time, fish)

    #print(fish)
        
        #print(fish_cords)
    i =0
    for (x,y,w,h) in fish:
        
        
            #    if(levelWeights[i] <5 and levelWeights[i] > 2.25):
                #if(levelWeights[i] > 3):


                    center = (x + w//2, y + h//2)
                    frame = cv.rectangle(frame, (x, y), (x + h, y + w), (0, 255, 0), 5)
                    fish_cords = [x,y]
            #    i = i+1 
       

       

 

    

    cv.imshow('Capture - fish detection', frame)
   

     
parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.')
parser.add_argument('--fish_cascade', help='Path to fish cascade.', default="C:\\Users\\prudo\\Desktop\\school\\fall 2023\\software\\fishCascadeV6.xml")
# parser.add_argument('--eyes_cascade', help='Path to eyes cascade.', default='data/haarcascades/haarcascade_eye_tree_eyeglasses.xml')
parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
args = parser.parse_args()



fish_cascade = cv.CascadeClassifier("D:\PyharmProjects\CSC380Fish-main\FishCascadeV6.xml")







#-- 2. Read the video stream
# camera_device = args.camera
# cap = cv.VideoCapture(0)

# JON ADDED (set the video name to a variable, then parse it for date and time)
video_name = '10_31_23@23'
# upload video to program
cap = cv.VideoCapture(video_name)



if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)
while True:
    ret, frame = cap.read()    
    frame = cv.resize(frame, None, fx=.5, fy=.5, interpolation=cv.INTER_AREA)

    if frame is None:
        print('--(!) No captured frame -- Break!')
        
        #p.stop()
        break
    detectAndDisplay(frame, video_name)
    #cv.imshow('Capture - fish detection', frame)

  #  p.play()
    if cv.waitKey(10) == 27:
      #  p.stop()
        break

#upload a image

#img = cv.imread("fish3.jpg", cv.IMREAD_COLOR)
#img = cv.imread("fish2.jpg", cv.IMREAD_COLOR)
#img = cv.imread("fishpic.jpg", cv.IMREAD_COLOR)

#img = cv.resize(img, None, fx=1, fy=1, interpolation=cv.INTER_AREA)

# cv.imshow("fish3.jpg", img)
# detectAndDisplay(img)

cv.waitKey(0)
cv.destroyAllWindows()