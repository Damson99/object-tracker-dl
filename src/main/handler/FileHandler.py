import cv2
import numpy

from main.handler.Handler import Handler


class FileHandler(Handler):
    def __init__(self, video_path):
        self._cap = cv2.VideoCapture(video_path)

    def is_opened(self) -> bool:
        return self._cap.isOpened()

    def get_center_point(self) -> tuple[int, int]:
        screen_height, screen_width = (int(self._cap.get(x))
                                       for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT))
        return int(screen_height / 2), int(screen_width / 2)

    def read(self) -> tuple[bool, numpy.ndarray]:
        return self._cap.read()

    def release(self):
        self._cap.release()

    def move(self, angle: int, deep_distance: int):
        pass
