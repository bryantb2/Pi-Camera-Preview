import cv2
import asyncio
import numpy as np
import time
from picamera2 import Picamera2

async def main():    
    screenWidth = 480
    screenHeight = 360
    
    picamera2 = Picamera2()
    
    camera_config = picamera2.create_preview_configuration(main={"size": (screenWidth, screenHeight)})
    picamera2.configure(camera_config)

    picamera2.start()

    space_between = int(screenWidth * 0.125)
    canvas_width = screenWidth + space_between
    resized_width = screenWidth // 2
    resized_height = screenHeight // 2
    circular_mask_diameter = min(resized_width, resized_height) // 2
    circular_mask = np.zeros((resized_height, resized_width, 3), dtype=np.uint8)
    cv2.circle(circular_mask, (resized_width // 2, resized_height // 2), circular_mask_diameter, (255, 255, 255), -1)

    target_time_per_frame = 1.0 / 30.0  # 30 FPS target

    while True:
        start_time = time.time()

        frame = picamera2.capture_array()
        if frame.shape[2] == 4:
            frame = frame[:, :, :3]
        resized_image = cv2.resize(frame, (resized_width, resized_height))

        stereoscopic_image = np.zeros((resized_height, canvas_width, 3), dtype=np.uint8)

        for i, angle in enumerate([-5, 5]):
            matrix = cv2.getRotationMatrix2D((resized_width // 2, resized_height // 2), angle, 1.0)
            rotated = cv2.warpAffine(resized_image, matrix, (resized_width, resized_height), flags=cv2.INTER_LINEAR)
            masked = cv2.bitwise_and(rotated, circular_mask)
            offset = i * (resized_width + space_between)
            stereoscopic_image[:, offset:offset+resized_width] = masked

        cv2.imshow('Stereoscopic Simulation', stereoscopic_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        end_time = time.time()
        process_time = end_time - start_time

        # Frame rate control
        if process_time < target_time_per_frame:
            time.sleep(target_time_per_frame - process_time)

    picamera2.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(main())
