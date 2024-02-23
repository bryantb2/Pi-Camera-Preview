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
    
    # Configure camera resolution
    camera_config = picamera2.create_preview_configuration(main={"size": (screenWidth, screenHeight)})
    picamera2.configure(camera_config)

    picamera2.start()

    # Pre-calculate values outside the loop
    space_between = int(screenWidth * 0.125)  # Adjust based on the desired spacing relative to screen width
    canvas_width = screenWidth + space_between
    resized_width = screenWidth // 2
    resized_height = screenHeight // 2
    circular_mask_diameter = min(resized_width, resized_height) // 2
    circular_mask = np.zeros((resized_height, resized_width, 3), dtype=np.uint8)
    cv2.circle(circular_mask, (resized_width // 2, resized_height // 2), circular_mask_diameter, (255, 255, 255), -1)

    while True:
        frame = picamera2.capture_array()
        
        # Ensure the frame is in RGB
        if frame.shape[2] == 4:
            frame = frame[:, :, :3]

        # Resize the image once for both eyes
        resized_image = cv2.resize(frame, (resized_width, resized_height))

        # Create a blank canvas for the combined stereoscopic image
        stereoscopic_image = np.zeros((resized_height, canvas_width, 3), dtype=np.uint8)

        # Rotate and mask the image for both sides
        for i, angle in enumerate([-5, 5]):  # Left and right angles
            matrix = cv2.getRotationMatrix2D((resized_width // 2, resized_height // 2), angle, 1.0)
            rotated = cv2.warpAffine(resized_image, matrix, (resized_width, resized_height), flags=cv2.INTER_LINEAR)
            masked = cv2.bitwise_and(rotated, circular_mask)
            
            # Place the masked images on the canvas
            offset = i * (resized_width + space_between)
            stereoscopic_image[:, offset:offset+resized_width] = masked

        cv2.imshow('Stereoscopic Simulation', stereoscopic_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    picamera2.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(main())
