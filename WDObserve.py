import cv2
import os
import time
import shutil
import numpy as np
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Function to get the background frame from the video
def get_background(file_path):
    cap = cv2.VideoCapture(file_path)
    # Randomly select 50 frames for the median
    frame_list = []
    for _ in range(50):
        ret, frame = cap.read()
        if ret:
            frame_list.append(frame)
    cap.release()
    return np.median(frame_list, axis=0).astype(np.uint8)

# Set the source directory to monitor
source_directory = '/home/fritz/TestingOpenCV/New'

# Set the destination directory for processing
processing_directory = '/home/fritz/TestingOpenCV/Process'

# Set the finished directory
finished_directory = '/home/fritz/TestingOpenCV/Finished'

# Define a custom event handler for file changes
class VideoFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        try:
            if event.src_path.endswith(".mp4"):
                # Copy the file to the processing directory
                shutil.copy(event.src_path, os.path.join(processing_directory, os.path.basename(event.src_path)))

                # Copy the file to the backup directory
                shutil.copy(event.src_path, os.path.join(finished_directory, os.path.basename(event.src_path)))

                # Process the file using OpenCV
                process_video(event.src_path, os.path.join(processing_directory, os.path.basename(event.src_path)))

                # Remove the file from the source directory after processing
                os.remove(event.src_path)

        except Exception as e:
            print(f"Exception in on_created: {str(e)}")

def process_video(file_path, save_name):
    cap = cv2.VideoCapture(file_path)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    out = cv2.VideoWriter(save_name, cv2.VideoWriter_fourcc(*'mp4v'), 10, (frame_width, frame_height))

    background = get_background(file_path)
    background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)

    frame_count = 0
    consecutive_frame = 2  # Set the default value

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame_count += 1
            orig_frame = frame.copy()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if frame_count % consecutive_frame == 0 or frame_count == 1:
                frame_diff_list = []

            frame_diff = cv2.absdiff(gray, background)
            ret, thres = cv2.threshold(frame_diff, 50, 255, cv2.THRESH_BINARY)
            dilate_frame = cv2.dilate(thres, None, iterations=2)
            frame_diff_list.append(dilate_frame)

            if len(frame_diff_list) == consecutive_frame:
                sum_frames = sum(frame_diff_list)

                contours, hierarchy = cv2.findContours(sum_frames, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for i, cnt in enumerate(contours):
                    cv2.drawContours(frame, contours, i, (0, 0, 255), 3)

                for contour in contours:
                    if cv2.contourArea(contour) < 500:
                        continue
                    (x, y, w, h) = cv2.boundingRect(contour)
                    cv2.rectangle(orig_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # cv2.imshow('Detected Objects', orig_frame)
                out.write(orig_frame)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    event_handler = VideoFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=source_directory, recursive=False)
    print(source_directory)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()