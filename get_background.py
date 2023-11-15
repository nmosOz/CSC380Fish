import numpy as np
import cv2

def get_background(file_path):
    cap = cv2.VideoCapture("C:/Users/natha/OneDrive/Desktop/CSC380/inputs/" + file_path)
    print(file_path)
    #Randomly select 50 frames for the median
    frame_indices = cap.get(cv2.CAP_PROP_FRAME_COUNT) * np.random.uniform(size=50)
    
    #Store the frames in an array
    frames = []
    for idx in frame_indices:
        #set the frame id to read that particular frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        height, width, layers = frame.shape
        new_h = int(height / 2)
        new_w = int(width / 2)
        frame = cv2.resize(frame, (new_w, new_h))
        frames.append(frame)
    
    #Calculate median
    median_frame = np.median(frames, axis=0).astype(np.uint8)

    return median_frame
