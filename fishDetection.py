from __future__ import print_function
import cv2 as cv



 

    

#     cv.imshow('Capture - fish detection', frame)

previous_bounding_boxes = []

#the higher this is the more confident the detection will be but if its to high you stop getting any detection. you shouldnt go any higher then 5
confidence_level = 0

#the amount of frames the programs averages between
frame_average_amount = 6

path_to_cascade = "C:\\Users\\prudo\\Desktop\\school\\fall 2023\\software\\fishCascadeV12.xml"

def detectAndDisplay(frame):
    fish_cascade = cv.CascadeClassifier(path_to_cascade)

    lgth1 =0
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)

    fish, rejectLevels, levelWeights = fish_cascade.detectMultiScale3(frame_gray, scaleFactor=1.2, minNeighbors=7, outputRejectLevels=1)

    filtered_fish = [f for i, f in enumerate(fish) if levelWeights[i] >confidence_level ]

    previous_bounding_boxes.append(filtered_fish)





    if len(previous_bounding_boxes) > frame_average_amount:
        previous_bounding_boxes.pop(0)

    if previous_bounding_boxes:
        avg_fish = [tuple(map(int, sum(x) / len(x))) for x in zip(*previous_bounding_boxes)]


        for (x, y, w, h) in avg_fish:
           
            lgth1 = len(avg_fish) 
            frame = cv.rectangle(frame, (x, y), (x + w, y + h), (255, 15, 17), 5)


    cv.imshow('Capture - fish detection', frame)
    return lgth1







#-- 2. Read the live video stream
#camera_device = args.camera
#cap = cv.VideoCapture(0)


# upload video to program
#cap = cv.VideoCapture('kieranFish3.mov')
#cap = cv.VideoCapture('kieranFish4.mp4')
#cap = cv.VideoCapture('kieranFish8.mp4')

#cap = cv.VideoCapture('kieranFish10.mp4')
cap =  cv.VideoCapture('kieranFish11.mp4')

#cap = cv.VideoCapture('testFish.mp4')



if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)
while True:
    ret, frame = cap.read()    
    #frame = cv.resize(frame, None, fx=.5, fy=.5, interpolation=cv.INTER_AREA)

    if frame is None:
        print('--(!) No captured frame -- Break!')
        
        #p.stop()
        break
    print(detectAndDisplay(frame))
    #cv.imshow('Capture - fish detection', frame)

  #  p.play()
    if cv.waitKey(10) == 27:
      #  p.stop()
        break

#upload a image
# img = cv.imread("fish3.jpg", cv.IMREAD_COLOR)
# img = cv.imread("fish2.jpg", cv.IMREAD_COLOR)
# img = cv.imread("fishpic.jpg", cv.IMREAD_COLOR)
# img = cv.resize(img, None, fx=1, fy=1 interpolation=cv.INTER_AREA)
# cv.imshow("fish3.jpg", img)
# detectAndDisplay(img)

cv.waitKey(0)
cv.destroyAllWindows()