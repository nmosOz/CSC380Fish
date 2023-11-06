import cv2


from get_background import get_background


def detect(videoFile):
    #Read the video file
    cap = cv2.VideoCapture("C:/Users/natha/OneDrive/Desktop/CSC380/inputs/" + videoFile)
    #get the video frame height and width
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    save_name = "C:/Users/natha/OneDrive/Desktop/CSC380/outputs/" + videoFile

    print(save_name)
    # define codec and create VideoWriter object
    out = cv2.VideoWriter(
        save_name,
        cv2.VideoWriter_fourcc(*'mp4v'), 10.0, 
        (frame_width, frame_height))

    #get the background model
    background = get_background(videoFile)
    #Convert the background to grayscale
    background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)

    #Keep track of frame count
    frame_count = 0
    #Number of frames for differencing
    consecutive_frame = 4

    #Loop over frames to detect moving objects
    while(cap.isOpened()):
        ret, frame = cap.read()

        if ret == True:

            height, width, layers = frame.shape
            new_h = int(height / 2)
            new_w = int(width / 2)
            frame = cv2.resize(frame, (new_w, new_h))

            print(frame_count)
            frame_count += 1
            orig_frame = frame.copy()

            #Convert the frame to grayscale again
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if frame_count % consecutive_frame == 0 or frame_count == 1:
                frame_diff_list = []
                
            # find the difference between current frame and base frame

            frame_diff = cv2.absdiff(gray, background)
            # thresholding to convert the frame to binary

            ret, thres = cv2.threshold(frame_diff, 80, 400, cv2.THRESH_BINARY)

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
                    if cv2.contourArea(contour) < 1000:
                        continue
                    # get the xmin, ymin, width, and height coordinates from the contours

                    (x, y, w, h) = cv2.boundingRect(contour)
                    # draw the bounding boxes
                    cv2.rectangle(orig_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
                cv2.imshow('Detected Objects', orig_frame)
                out.write(orig_frame)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
        else:
            print('finished processing video')
            break

    out.release()
    cap.release()
    cv2.destroyAllWindows()

#Command to execute the code
#python detect.py --input input/video_1.mp4 -c 4

