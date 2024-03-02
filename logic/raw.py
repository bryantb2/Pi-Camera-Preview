import cv2
import asyncio
import numpy as np
from picamera2 import Picamera2

async def main():
    # Initialize Picamera2
    picamera2 = Picamera2()

    # Configure camera resolution
    camera_config = picamera2.create_preview_configuration(main={"size": (480, 360)})
    picamera2.configure(camera_config)

    picamera2.start()

    while True:
        # Capture frame-by-frame
        frame = picamera2.capture_array()
        
        # Ensure the frame is in RGB format
        if frame.shape[2] == 4:
            frame = frame[:, :, :3]

        h, w = frame.shape[:2]
        # Resize the captured frame
        resized_frame = cv2.resize(frame, (int(w / 2), int(h / 2)))
        h1, w1 = resized_frame.shape[:2]

        # Rotate the left image a few degrees to the left
        M_left = cv2.getRotationMatrix2D((w1 / 2, h1 / 2), angle=-5, scale=1)
        rotated_left = cv2.warpAffine(resized_frame, M_left, (w1, h1))

        # Rotate the right image a few degrees to the right
        M_right = cv2.getRotationMatrix2D((w1 / 2, h1 / 2), angle=5, scale=1)
        rotated_right = cv2.warpAffine(resized_frame, M_right, (w1, h1))

        # Prepare a blank canvas/background
        background = np.zeros((h1, w, 3), dtype=np.uint8)

        # Set the rotated images side by side on the background
        background[:, :w1] = rotated_left  # Left side
        background[:, w1:w1*2] = rotated_right  # Right side

        cv2.imshow('Stereoscopic Simulation', background)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    picamera2.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(main())