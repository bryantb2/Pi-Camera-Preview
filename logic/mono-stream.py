# Simplified image processing with raw video stream as two side-by-side images

import cv2
import asyncio
import numpy as np
from picamera2 import Picamera2

async def main():
    picamera2 = Picamera2()

    # Use a lower resolution to reduce processing load, if acceptable for your application.
    # This reduces the amount of data to process.
    camera_config = picamera2.create_preview_configuration(main={"size": (640, 480)})
    picamera2.configure(camera_config)

    picamera2.start()

    while True:
        frame = picamera2.capture_array()

        # If the frame is RGBA, convert to RGB by discarding the alpha channel.
        # This check is moved inside the conditional to avoid unnecessary processing.
        if frame.shape[2] == 4:
            frame = frame[:, :, :3]

        # Directly resize the image to half in both dimensions for PIP effect
        # and to reduce the size of the data being processed.
        resized_image = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        # Initialize a blank canvas with the same dimensions as the original frame.
        # This is moved outside the loop as its size depends on the resized image, not the frame.
        background = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)

        # Calculate positions only once if they don't change.
        # Assuming fixed positions for PIP windows.
        h1, w1 = resized_image.shape[:2]
        pip_h, pip_w = 0, 0  # Top-left corner for the first PIP
        pip_ha, pip_wa = 0, w1  # Top-left corner for the second PIP

        # Place the two resized frames side by side on the background.
        background[pip_h:pip_h + h1, pip_w:pip_w + w1] = resized_image
        background[pip_ha:pip_ha + h1, pip_wa:pip_wa + w1] = resized_image

        cv2.imshow('image', background)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    picamera2.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(main())
