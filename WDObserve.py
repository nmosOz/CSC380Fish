# Import necessary libraries
import cv2
import os
import time
import shutil
import numpy as np
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# Function to get the background frame from the video
def get_background(file_path):
    # Open the video file
    cap = cv2.VideoCapture(file_path)

    # Randomly select 50 frames for the median
    frame_list = []
    for _ in range(50):
        ret, frame = cap.read()
        if ret:
            frame_list.append(frame)
    cap.release()

    # Calculate the median frame from the selected frames
    return np.median(frame_list, axis=0).astype(np.uint8)


# Set the source directory to monitor for new video files
source_directory = '/home/fritz/TestingOpenCV/New'

# Set the destination directory for processing video files
processing_directory = '/home/fritz/TestingOpenCV/Process'

# Set the finished directory for completed video files
finished_directory = '/home/fritz/TestingOpenCV/Finished'


# Define a custom event handler for file changes
class VideoFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        try:
            if event.src_path.endswith(".mp4"):
                # Copy the newly created video file to the processing directory
                shutil.copy(event.src_path, os.path.join(processing_directory, os.path.basename(event.src_path)))

                # Copy the file to the backup directory
                shutil.copy(event.src_path, os.path.join(finished_directory, os.path.basename(event.src_path)))

                # Process the video file using OpenCV
                process_video(event.src_path, os.path.join(processing_directory, os.path.basename(event.src_path)))

                # Remove the original file from the source directory after processing
                os.remove(event.src_path)

        except Exception as e:
            print(f"Exception in on_created: {str(e)}")


# Function to process a video file
def process_video(file_path, save_name):
    cap = cv2.VideoCapture(file_path)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    out = cv2.VideoWriter(save_name, cv2.VideoWriter_fourcc(*'mp4v'), 10, (frame_width, frame_height))

    # Get the background frame from the video
    background = get_background(file_path)
    background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)

    frame_count = 0
    consecutive_frame = 2  # Set the default value

    while cap.isOpened():
        # Read the next frame from the video
        ret, frame = cap.read()

        if ret:
            # Increment the count of frames processed
            frame_count += 1

            # Create a copy of the current frame for further analysis
            orig_frame = frame.copy()

            # Convert the frame to grayscale for easier analysis
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Check if it's time to start fresh with a new set of frames
            if frame_count % consecutive_frame == 0 or frame_count == 1:
                frame_diff_list = []

            # Calculate the difference between the current frame and the background
            frame_diff = cv2.absdiff(gray, background)

            # Highlight significant changes by applying a binary threshold
            ret, thres = cv2.threshold(frame_diff, 50, 255, cv2.THRESH_BINARY)

            # Emphasize and expand the highlighted changes
            dilate_frame = cv2.dilate(thres, None, iterations=2)

            # Keep track of the processed frames
            frame_diff_list.append(dilate_frame)

            # Check if we have enough frames to analyze for changes
            if len(frame_diff_list) == consecutive_frame:
                # Accumulate the changes from multiple frames
                sum_frames = sum(frame_diff_list)

                # Detect and identify areas of change in the video frame
                contours, hierarchy = cv2.findContours(sum_frames, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # Mark the areas of change with red contours
                for i, cnt in enumerate(contours):
                    cv2.drawContours(frame, contours, i, (0, 0, 255), 3)

                # Identify and draw green boxes around significant changes
                for contour in contours:
                    if cv2.contourArea(contour) < 500:
                        continue
                    (x, y, w, h) = cv2.boundingRect(contour)
                    cv2.rectangle(orig_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Write the processed frame to the output video
                out.write(orig_frame)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Create a custom event handler for file changes
    event_handler = VideoFileHandler()

    # Create an observer to monitor the source directory for new files
    observer = Observer()

    # Set up the observer to watch the source directory for file creation events (non-recursively)
    observer.schedule(event_handler, path=source_directory, recursive=False)

    # Print the source directory being monitored
    print(source_directory)

    # Start the observer to begin monitoring for file changes
    observer.start()

    try:
        # Keep the script running and periodically check for changes
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # If the script is interrupted (e.g., with Ctrl+C), stop the observer
        observer.stop()

    # Wait for the observer to finish its work
    observer.join()

