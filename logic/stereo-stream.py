# Advanced image processing WITH rotation for faked depth perception

import cv2
import asyncio
import numpy as np
import sys 
from picamera2 import Picamera2


async def main():
    
    # Check if the correct number of arguments are provided
    if len(sys.argv) != 3:
        print("Usage: script.py screenWidth screenHeight")
        return
    
    # Parse screen width and height from command line arguments
    screenWidth = int(sys.argv[1])
    screenHeight = int(sys.argv[2])
    
    # Initialize Picamera2
    picamera2 = Picamera2()
    
    # TODO: force enable continuous autofocus

    # Configure camera resolution
    camera_config = picamera2.create_preview_configuration(main={"size": (screenWidth, screenHeight)})
    picamera2.configure(camera_config)

    picamera2.start()
    
    # Create a fullscreen window
    cv2.namedWindow("Stereoscopic Simulation", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Stereoscopic Simulation", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        # Capture frame-by-frame
        frame = picamera2.capture_array()
        
        # Ensure the frame is in RGB
        if frame.shape[2] == 4:
            frame = frame[:, :, :3]

        # Resize the image for both left and right images
        resized_image = cv2.resize(frame, (int(frame.shape[1] / 2), int(frame.shape[0] / 2)))

        # Create a blank canvas for the combined stereoscopic image
        h, w = resized_image.shape[:2]
        stereoscopic_image = np.zeros((h, w * 2, 3), dtype=np.uint8)

        # Prepare the rotation for each side
        center_left = (w // 4, h // 2)
        center_right = (w // 4, h // 2)
        angle_left = -5  # Rotate left image to the left
        angle_right = 5  # Rotate right image to the right
        scale = 1.0

        # Get the rotation matrices for each rotation
        matrix_left = cv2.getRotationMatrix2D(center_left, angle_left, scale)
        matrix_right = cv2.getRotationMatrix2D(center_right, angle_right, scale)

        # Apply the affine transformation (rotation) to create the left and right images
        rotated_left = cv2.warpAffine(resized_image, matrix_left, (w, h), flags=cv2.INTER_LINEAR)
        rotated_right = cv2.warpAffine(resized_image, matrix_right, (w, h), flags=cv2.INTER_LINEAR)

        # Place the rotated images side by side
        stereoscopic_image[:, :w] = rotated_left
        stereoscopic_image[:, w:] = rotated_right

        cv2.imshow('Stereoscopic Simulation', stereoscopic_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    picamera2.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(main())

