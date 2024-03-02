from picamera2 import Picamera2
import cv2
import numpy as np
import time

# Adjustable constant for the distance between the two images (eyes)
eye_separation_multiplier = 0.05  # Adjust this value to increase or decrease the distance

def create_circular_mask(h, w, center=None, radius=None):
    if center is None:
        center = (int(w / 2), int(h / 2))
    if radius is None:
        radius = min(center[0], center[1], w - center[0], h - center[1])
    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y - center[1])**2)
    mask = dist_from_center <= radius
    return mask.astype(np.uint8)

def rotate_image(image, angle, scale=1.0):
    h, w = image.shape[:2]
    center = (int(w / 2), int(h / 2))
    rot_mat = cv2.getRotationMatrix2D(center, angle, scale)
    rotated_image = cv2.warpAffine(image, rot_mat, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0))
    return rotated_image

def apply_mask(image, mask):
    return cv2.bitwise_and(image, image, mask=mask)

def main():
    picamera2 = Picamera2()
    # Decrease the resolution for better performance
    camera_config = picamera2.create_preview_configuration(main={"size": (480, 360)})
    picamera2.configure(camera_config)
    picamera2.start()

    cv2.namedWindow('VR View', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('VR View', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    last_time = time.time()
    frame_period = 1.0 / 24.0  # aiming for 24 fps

    # Adjust mask creation based on the new resolution
    mask = create_circular_mask(360, 480)

    try:
        while True:
            current_time = time.time()
            elapsed = current_time - last_time

            if elapsed > frame_period:
                frame = picamera2.capture_array()
                # Adjust for new resolution: ensure the frame is in RGB format
                if frame.shape[2] == 4:
                    frame = frame[:, :, :3]

                left_image = rotate_image(frame, -5)  # Slightly rotate left image
                right_image = rotate_image(frame, 5)  # Slightly rotate right image

                # Apply the circular mask
                left_masked_image = apply_mask(left_image, mask)
                right_masked_image = apply_mask(right_image, mask)

                separator_width = int(frame.shape[1] * eye_separation_multiplier)
                separator = np.zeros((360, separator_width, 3), dtype=np.uint8)
                vr_frame = np.hstack((left_masked_image, separator, right_masked_image))

                cv2.imshow('VR View', vr_frame)

                last_time = current_time

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        picamera2.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
