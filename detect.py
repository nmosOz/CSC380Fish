import cv2
import os

from get_background import get_background
from fishDetection import detectAndDisplay

#Cascade file for fish 
fish_cascade = cv2.CascadeClassifier("C:/Users/natha/OneDrive/Desktop/CSC380/fishCascadeV7.xml")
coords = [0 for i in range(4)]


def detect(videoFile):
    #start time
    startTime = 0 
    #end time
    endTime = 0
    #Read the video file
    cap = cv2.VideoCapture("C:/Users/natha/OneDrive/Desktop/CSC380/inputs/" + videoFile)
    #get the video frame height and width
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    path = "C:/Users/natha/OneDrive/Desktop/CSC380/outputs/"
    save_name = "C:/Users/natha/OneDrive/Desktop/CSC380/outputs/" + videoFile

    print(save_name)
    # define codec and create VideoWriter object
    out = cv2.VideoWriter(
        save_name,
        cv2.VideoWriter_fourcc(*'vp80'), 10.0, 
        (frame_width, frame_height))

    os.chdir(path)
    #get the background model
    background = get_background(videoFile)
    #Convert the background to grayscale
    background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)

    #Keep track of frame count
    frame_count = 0
    #Number of frames for differencing
    consecutive_frame = 4

    #
    fileName = 'savedImg.jpg'
    num_imgs = 0


    #Loop over frames to detect moving objects
    while(cap.isOpened()):
        ret, frame = cap.read()

        if ret == True:

            height, width, layers = frame.shape
            new_h = int(height)
            new_w = int(width)
            frame = cv2.resize(frame, (new_w, new_h))

            #print(frame_count)
            frame_count += 1
            orig_frame = frame.copy()

            #Convert the frame to grayscale again
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if frame_count % consecutive_frame == 0 or frame_count == 1:
                frame_diff_list = []
                
            # find the difference between current frame and base frame

            frame_diff = cv2.absdiff(gray, background)
            # thresholding to convert the frame to binary

            ret, thres = cv2.threshold(frame_diff, 35, 500, cv2.THRESH_BINARY)

            # dilate the frame a bit to get some more white area...
            # ... makes the detection of contours a bit easier
            dilate_frame = cv2.dilate(thres, None, iterations=2)
            # append the final result into the `frame_diff_list`
            frame_diff_list.append(dilate_frame)

            # if we have reached `consecutive_frame` number of frames
            if len(frame_diff_list) == consecutive_frame:
                # add all the frames in the `frame_diff_list`
                sum_frames = sum(frame_diff_list)

            # find the contours around the white segmented areas
                contours, hierarchy = cv2.findContours(sum_frames, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # draw the contours, not strictly necessary
                for i, cnt in enumerate(contours):
                    cv2.drawContours(frame, contours, i, (0, 0, 255), 3)
                for contour in contours:

                    # continue through the loop if contour area is less than 500...
                    # ... helps in removing noise detection
                    if cv2.contourArea(contour) < 500:
                        #print("box too small")
                        continue
                    # get the xmin, ymin, width, and height coordinates from the contours

                    (x, y, w, h) = cv2.boundingRect(contour)

                    # draw the bounding boxes 
                    img = cv2.rectangle(orig_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                    #If the length of the array containing the previous coordinates is 0, add the coordinates
                    if len(coords) == 0:
                        coords[0] = x
                        coords[1] = y
                    #If the new x and y coordinates are w/in 5 pixels of the last ones, continue 
                    if coords[0] - 15 <= x <= coords[0] + 15 or coords[1] - 15 <= y <= coords[1] + 15:
                        startTime = 0
                        continue
                    #See if the object is moving left 
                    elif x < coords[0] + 20 and coords[1] - 40 <= y <= coords[1] + 40:
                        if startTime == 0:
                            print('movement started')
                            startTime = (int)(cap.get(cv2.CAP_PROP_POS_MSEC))
                        print("object moving left")   
                    #See if the object is moving right
                    elif x > coords[0] - 20 and coords[1] - 40 <= y <= coords[1] + 40:
                        if startTime == 0:
                            print('movement started')
                            startTime = (int)(cap.get(cv2.CAP_PROP_POS_MSEC))
                        print("Object moving to the right")
                    #IF there is nothing moving
                    else: 
                        #print('else')
                        endTime = (int)(cap.get(cv2.CAP_PROP_POS_MSEC))

                    print(x, coords[0])
                    print(y, coords[1])
                    print("start")
                    print(startTime)
                    print("End time")
                    print(endTime)
                    
                    
                    #Update with new coordinates
                    coords[0] = x
                    coords[1] = y

     
                    #img = cv2.rectangle(orig_frame, (0, 0), (0, 0), (0, 255, 0), 0)
        
                    ROI = img[y:y+h, x:x+w]

                    #Call the detect and display functions
                    #print("Calling detect and display") 
                    
                    if(ROI.size == 0):
                        print("frame messed up")
                        continue
                    #detectAndDisplay(ROI)

                    ##cv2.imwrite("saved_img_{}.jpg".format(num_imgs) , ROI)
                    ##num_imgs += 1

                cv2.imshow('Detected Objects', orig_frame)
                out.write(orig_frame)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
        else:
            print('finished processing video')
            break

    #os.remove(videoFile)
    out.release()
    cap.release()
    cv2.destroyAllWindows()

def movement(startTime, cap):
    #While the fish is still moving 
    endTime = cap.get(cv2.CAP_PROP_POS_MSEC)

    return endTime

#Command to execute the code
#python detect.py --input input/video_1.mp4 -c 4
