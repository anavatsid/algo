import cv2
import numpy as np


def check_camera_idx():

    all_camera_idx_available = []

    for camera_idx in range(16):
        cap = cv2.VideoCapture(camera_idx, cv2.CAP_DSHOW)
        if cap.isOpened():
            print(f'\tCamera index available: {camera_idx}')
            all_camera_idx_available.append(camera_idx)
        cap.release()
        cv2.destroyAllWindows()

    print(f"{all_camera_idx_available=}")

    return all_camera_idx_available
