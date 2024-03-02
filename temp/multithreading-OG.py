from picamera2 import Picamera2
import cv2
import numpy as np
from threading import Thread
import queue

def capture_frames(picamera2, frame_queue):
    while True:
        frame = picamera2.capture_array()
        if frame is not None:
            frame_queue.put(frame)
        else:
            break

def process_and_display_frames(frame_queue):
    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()
            # Process the frame (resize, rotate, apply mask, etc.)
            # For demonstration, this step is simplified
            processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Simplified processing step
            cv2.imshow('Processed Frame', processed_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

def main():
    picamera2 = Picamera2()
    camera_config = picamera2.create_preview_configuration(main={"size": (480, 360)})
    picamera2.configure(camera_config)
    picamera2.start()

    frame_queue = queue.Queue(maxsize=10)  # Adjust maxsize as appropriate

    # Thread for capturing frames
    capture_thread = Thread(target=capture_frames, args=(picamera2, frame_queue))
    capture_thread.start()

    # Main thread for processing and displaying
    process_and_display_frames(frame_queue)

    capture_thread.join()
    picamera2.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
