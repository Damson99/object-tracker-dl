import cv2

from handler.Handler import Handler


class FileHandler(Handler):
    def __init__(self, video_path):
        self._cap = cv2.VideoCapture(video_path)

    def is_opened(self) -> bool:
        return self._cap.isOpened()

    def get_center_point(self) -> tuple[int, int]:
        screen_width, screen_height = (int(self._cap.get(x))
                                       for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT))
        return screen_width // 2, screen_height // 2

    def read(self) -> tuple:
        return self._cap.read()

    def release(self):
        self._cap.release()
