import os
import shutil
import time
from detect import detect
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# Set the source directory to monitor for new video files
source_directory = '/home/fritz/TestingOpenCV/New' #CHANGE !!!!

# Set the destination directory for processing video files
processing_directory = '/home/fritz/TestingOpenCV/Process'#CHANGE ME !!!!!

# Set the finished directory for completed video files
finished_directory = '/home/fritz/TestingOpenCV/Finished'#CHANGE ME !!!!!

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
                detect(event.src_path, os.path.join(processing_directory, os.path.basename(event.src_path))) #CHANGE ME !!!!!

                # Remove the original file from the source directory after processing
                os.remove(event.src_path)

        except Exception as e:
            print(f"Exception in on_created: {str(e)}")

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
            #Get the contents of the source directory
            videos_to_process = os.listdir(source_directory)
            #Make sure it actually has something in it
            if len(videos_to_process) == 0:
                #If it does not, continue
                continue
            #else, loop through the array to process videos
            else:
                for video in videos_to_process:
                    detect(video)
            time.sleep(1)

    except KeyboardInterrupt:
        # If the script is interrupted (e.g., with Ctrl+C), stop the observer
        observer.stop()

    # Wait for the observer to finish its work
    observer.join()
