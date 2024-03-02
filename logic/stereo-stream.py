from picamera2 import Picamera2
import cv2
import numpy as np
import threading
import queue

# Fixed separator width in pixels to simulate the width of an average human nose
separator_width = 40  # Adjust this value based on your VR headset or preference
shift_amount = 5  # Number of pixels to shift for the pseudo-3D effect

def shift_image(image, pixels):
    if pixels == 0:
        return image
    elif pixels > 0:
        return np.hstack((image[:, pixels:], np.zeros((image.shape[0], pixels, 3), dtype=image.dtype)))
    else:
        return np.hstack((np.zeros((image.shape[0], -pixels, 3), dtype=image.dtype), image[:, :pixels]))

def frame_capture_worker(picamera2, frame_queue):
    while True:
        frame = picamera2.capture_array()
        if frame.shape[2] == 4:  # Convert RGBA to RGB if necessary
            frame = frame[:, :, :3]
        frame_queue.put(frame)

def main():
    picamera2 = Picamera2()
    # Further increased resolution to 480x360
    camera_config = picamera2.create_preview_configuration(main={"size": (480, 360)})
    picamera2.configure(camera_config)
    picamera2.start()

    cv2.namedWindow('VR View', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('VR View', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    frame_queue = queue.Queue(maxsize=2)  # Use a small maxsize to prevent lag
    capture_thread = threading.Thread(target=frame_capture_worker, args=(picamera2, frame_queue))
    capture_thread.daemon = True
    capture_thread.start()

    try:
        while True:
            if not frame_queue.empty():
                frame = frame_queue.get()

                # Shift images for pseudo-3D effect
                left_image = shift_image(frame, -shift_amount)
                right_image = shift_image(frame, shift_amount)

                separator = np.zeros((360, separator_width, 3), dtype=np.uint8)
                vr_frame = np.hstack((left_image, separator, right_image))

                cv2.imshow('VR View', vr_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        picamera2.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
