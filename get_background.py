import numpy as np
import cv2

def get_background(file_path):
    cap = cv2.VideoCapture(file_path)

    #Randomly select 50 frames for the median
    